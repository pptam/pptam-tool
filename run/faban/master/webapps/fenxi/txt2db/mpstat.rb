# mpstat spec file
$LOAD_PATH << File.expand_path(File.dirname(__FILE__))

require 'generic_parser'

mpstat = GenericParser.new(ARGV[0], ARGV[1])
mpstat.header(/^CPU/)
mpstat.cycle(/^CPU/)
mpstat.data_type("integer")
mpstat.process
mpstat.create_table
headers = { "minf" => "Minor Faults",
  "mjf"   => "Major Faults",
  "xcal"  => "Cross calls",
  "intr"  => "Interrups",
  "ithr"  => "Interrup Threads",
  "csw"   => "Context Switches",
  "icsw"  => "Involuntary Context Switches",
  "migr"  => "Thread Migrations",
  "smtx"  => "Mutex Spins",
  "srw"   => "Reader-Writer spins",
  "syscl" => "System calls",
  "usr"   => "User Time",
  "sys"   => "System Time",
  "idl"   => "Idle Time"
}

mpstat.columns.each do |col|
  next unless headers[col]
  mpstat.section( :title => headers[col] + " per CPU", :type=>"Line", 
    :dims => 2, :query => "select Time, CPU, #{col} from TABLE")
  mpstat.section(:title =>headers[col], :summarize => col)
end