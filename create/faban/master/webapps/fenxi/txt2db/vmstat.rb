# vmstat spec file
$LOAD_PATH << File.expand_path(File.dirname(__FILE__))
require 'generic_parser'

vmstat = GenericParser.new(ARGV[0], ARGV[1])
vmstat.ignore(/memory/)
vmstat.header(/us sy id/)
vmstat.cycle(/[0-9]+$/)
vmstat.data_type("integer")
vmstat.process

# vmstat headers have "in" as one of the column names. This is a SQL
# reserved name. We rename it to intr
if (i = vmstat.columns.index("in")) then
  vmstat.columns[i] = "intr"
end
# Solaris vmstat has 2 columns with hdr "sy". The first one is syscalls
# and the second one is system time. We rename the first one to "sysc"
if vmstat.columns.select{|e| e == "sy"}.length == 2 then
  vmstat.columns[vmstat.columns.index("sy")] = "sysc"
end

# Solaris vmstat on systems with low number of disks creates columns with the
# -- header. We need to rename the header to some valid disk id.
vmstat.columns.each_with_index{|e,i| vmstat.columns[i]="disk#{i}" if e=~ /--/ }

vmstat.create_table

# The word "TABLE" below will be replaced by the actual tablename.
vmstat.section( :title => "CPU", :type=>"Line", 
  :query => %w|us sy id|)
vmstat.section( :title => "Faults", :type=>"Line", 
  :query => %w|intr sysc cs|)
vmstat.section( :title => "Kernel Threads", :type=>"Line", 
  :query => %w|r b w|)
vmstat.section( :title => "Paging", :type=>"Line", 
  :query => %w|re mf pi po fr de sr|)
vmstat.section( :title => "Free Memory and swap", :type=>"Line", 
  :query => %w|swap free buff cache si so|)
vmstat.section(:title =>"CPU Utilization (USR)", :summarize => "us")
vmstat.section(:title =>"CPU Utilization (SYS)", :summarize => "sy")
vmstat.section(:title =>"CPU Utilization (Total)", :summarize => "us + sy")

vmstat.close