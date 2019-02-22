defmodule Parser.Parser do
  import SweetXml

  def main(args) do
    args |> parse_args |> parse_all_directories!
  end

  defp parse_args(args) do
    {options, _, _} = OptionParser.parse(args, switches: [input: :string, output: :string])

    options
  end

  def parse_all_directories!(input: input, output: output) do
    IO.puts("Processing #{input} and writing to #{output}...")

    {:ok, to_do} = File.ls(input)

    benchflow_output = "#{output}/benchflow_output.csv"
    summary_output = "#{output}/summary_output.csv"

    File.rm(benchflow_output)
    File.rm(summary_output)
    {:ok, io_benchflow_output} = File.open(benchflow_output, [:write])
    {:ok, io_summary_output} = File.open(summary_output, [:write])

    to_do
    |> Enum.filter(fn item ->
      {:ok, %File.Stat{type: type}} = File.lstat("#{input}/#{item}")
      type == :directory
    end)
    |> Enum.with_index()
    |> Enum.each(fn {id, index} ->
      parse_single_directory!("#{input}/#{id}", io_benchflow_output, io_summary_output, index)
    end)

    File.close(io_benchflow_output)
    File.close(io_summary_output)

    System.halt()
    :ok
  end

  def parse_all_directories!(_options) do
    IO.puts("Parses result directories coming from Faban into a single csv file.")
    IO.puts("")
    IO.puts("PARSER --input=(folder name in which all the experiments are) --output=(folder to write the result of the parsing)")
    IO.puts("")
  end

  def parse_single_directory!(path, io_benchflow_output, io_summary_output, index) do
    IO.puts("Parsing #{path}...")

    {:ok, compose} = File.read("#{path}/definition/docker-compose.yml")

    {:ok,
     %{
       "services" => %{
         "carts" => %{
           "deploy" => %{
             "replicas" => replicas,
             "resources" => %{
               "limits" => %{"cpus" => cpus, "memory" => memory_as_string}
             }
           }
         }
       }
     }} =
      compose
      |> YamlElixir.read_from_string()

    {memory_as_float, "M"} =
      memory_as_string
      |> Float.parse()

    memory = memory_as_float / 1000
    {:ok, run} = File.read("#{path}/definition/run.xml")
    {:ok, summary} = File.read("#{path}/faban/summary.xml")

    pages =
      summary
      |> xpath(~x"//mix/operation/@name"l)

    passed =
      summary
      |> xpath(~x"/benchResults/benchSummary/passed/text()")

    %{scale: scale} =
      run
      |> xmap(scale: ~x"//fa:runConfig/fa:scale/text()")

    if index == 0 do
      IO.write(io_benchflow_output, "ID,Users,Memory,CPU,CartReplicas,Metric")
      Enum.each(pages, fn page -> IO.write(io_benchflow_output, ",#{page}") end)
      IO.write(io_benchflow_output, ",FabanID,Passed\r\n")

      IO.write(io_summary_output, "ID,Users,Memory,CPU,CartReplicas,FabanID,Passed\r\n")
    end

    IO.write(io_summary_output, "#{index + 1},#{scale},#{memory},#{cpus},#{replicas},#{Path.basename(path)},#{passed}\r\n")

    IO.write(io_benchflow_output, "#{index + 1},#{scale},#{memory},#{cpus},#{replicas},Avg (sec)")

    Enum.each(pages, fn page ->
      %{avg: avg} = parse_response_times(path, page, summary)
      IO.write(io_benchflow_output, ",#{avg}")
    end)

    IO.write(io_benchflow_output, ",#{Path.basename(path)},#{passed}\r\n")

    IO.write(io_benchflow_output, "#{index + 1},#{scale},#{memory},#{cpus},#{replicas},SD (sec)")

    Enum.each(pages, fn page ->
      %{sd: sd} = parse_response_times(path, page, summary)
      IO.write(io_benchflow_output, ",#{sd}")
    end)

    IO.write(io_benchflow_output, ",#{Path.basename(path)},#{passed}\r\n")

    IO.write(io_benchflow_output, "#{index + 1},#{scale},#{memory},#{cpus},#{replicas},Mix % (take failure into account)")

    Enum.each(pages, fn page ->
      %{mix: mix} = parse_operation!(path, page, summary)
      IO.write(io_benchflow_output, ",#{mix}")
    end)

    IO.write(io_benchflow_output, ",#{Path.basename(path)},#{passed}\r\n")

    :ok
  end

  def parse_operation!(_path, page, summary) do
    %{summary: successes} =
      summary
      |> xmap(summary: ~x"/benchResults/driverSummary/mix/operation[@name='#{page}']/successes/text()")

    %{summary: failures} =
      summary
      |> xmap(summary: ~x"/benchResults/driverSummary/mix/operation[@name='#{page}']/failures/text()")

    %{summary: mix} =
      summary
      |> xmap(summary: ~x"/benchResults/driverSummary/mix/operation[@name='#{page}']/mix/text()")

    %{successes: successes, failures: failures, mix: mix}
  end

  def parse_response_times(_path, page, summary) do
    %{summary: avg} =
      summary
      |> xmap(summary: ~x"/benchResults/driverSummary/responseTimes/operation[@name='#{page}']/avg/text()")

    %{summary: max} =
      summary
      |> xmap(summary: ~x"/benchResults/driverSummary/responseTimes/operation[@name='#{page}']/max/text()")

    %{summary: sd} =
      summary
      |> xmap(summary: ~x"/benchResults/driverSummary/responseTimes/operation[@name='#{page}']/sd/text()")

    %{avg: avg, max: max, sd: sd}
  end
end
