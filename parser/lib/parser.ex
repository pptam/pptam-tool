defmodule Parser.Parser do
  import SweetXml

  # Run from command line with iex -S mix run -e "Parser.parse"
  # Build using mix escript.build
  # Run on Windows using escript parser

  def main(args) do
    args |> parse_args |> parse_all_directories!
  end

  defp parse_args(args) do
    {options, _, _} = OptionParser.parse(args, switches: [input: :string, output: :string])
    options
  end

  def parse_all_directories!([input: input, output: output]) do
    IO.puts("Processing #{input} and writing #{output}...")

    {:ok, to_do} = File.ls(prefix)

    File.rm(output)
    {:ok, results} = File.open(output, [:write])

    to_do
    |> Enum.filter(fn item ->
      {:ok, %File.Stat{type: type}} = File.lstat("#{input}/#{item}")
      type == :directory
    end)
    |> Enum.with_index()
    |> Enum.each(fn {id, index} -> parse_single_directory!("#{input}/#{id}", results, index) end)

    File.close(results)

    System.halt()
    :ok
  end

  def parse_all_directories!(_options) do
    IO.puts("Parses result directories coming from Faban into a single csv file.")
    IO.puts("")
    IO.puts("PARSER --input=(folder name in which all the experiments are) --output=(csv file to which to write the result of the parsing)")
    IO.puts("")
  end

  def parse_single_directory!(path, file, index) do
    IO.puts("Parsing #{path}...")

    {:ok, compose} = File.read("#{path}/definition/docker-compose.yml")

    {:ok,
     %{
       "services" => %{
         "carts" => %{
           "deploy" => %{
             "replicas" => replicas,
             "resources" => %{"limits" => %{"cpus" => cpus, "memory" => memory_as_string}}
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
      IO.write(file, "ID,Users,Memory,CPU,CartReplicas,Metric")
      Enum.each(pages, fn page -> IO.write(file, ",#{page}") end)
      IO.write(file, ",FabanID,Passed\r\n")
    end

    IO.write(
      file,
      "#{index + 1},#{scale},#{memory},#{cpus},#{replicas},Avg (sec)"
    )

    Enum.each(pages, fn page ->
      %{avg: avg} = parse_response_times(path, page, summary)
      IO.write(file, ",#{avg}")
    end)

    IO.write(file, ",#{Path.basename(path)},#{passed}")
    IO.write(file, "\r\n")

    IO.write(
      file,
      "#{index + 1},#{scale},#{memory},#{cpus},#{replicas},SD (sec)"
    )

    Enum.each(pages, fn page ->
      %{sd: sd} = parse_response_times(path, page, summary)
      IO.write(file, ",#{sd}")
    end)

    IO.write(file, ",#{Path.basename(path)},#{passed}")
    IO.write(file, "\r\n")

    IO.write(
      file,
      "#{index + 1},#{scale},#{memory},#{cpus},#{replicas},Mix % (take failure into account)"
    )

    Enum.each(pages, fn page ->
      %{mix: mix} = parse_operation!(path, page, summary)
      IO.write(file, ",#{mix}")
    end)

    IO.write(file, ",#{Path.basename(path)},#{passed}")
    IO.write(file, "\r\n")

    :ok
  end

  def parse_operation!(_path, page, summary) do
    %{summary: successes} =
      summary
      |> xmap(
        summary: ~x"/benchResults/driverSummary/mix/operation[@name='#{page}']/successes/text()"
      )

    %{summary: failures} =
      summary
      |> xmap(
        summary: ~x"/benchResults/driverSummary/mix/operation[@name='#{page}']/failures/text()"
      )

    %{summary: mix} =
      summary
      |> xmap(summary: ~x"/benchResults/driverSummary/mix/operation[@name='#{page}']/mix/text()")

    %{successes: successes, failures: failures, mix: mix}
  end

  def parse_response_times(_path, page, summary) do
    %{summary: avg} =
      summary
      |> xmap(
        summary:
          ~x"/benchResults/driverSummary/responseTimes/operation[@name='#{page}']/avg/text()"
      )

    %{summary: max} =
      summary
      |> xmap(
        summary:
          ~x"/benchResults/driverSummary/responseTimes/operation[@name='#{page}']/max/text()"
      )

    %{summary: sd} =
      summary
      |> xmap(
        summary:
          ~x"/benchResults/driverSummary/responseTimes/operation[@name='#{page}']/sd/text()"
      )

    %{avg: avg, max: max, sd: sd}
  end
end
