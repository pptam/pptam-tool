# iosum spec file
$LOAD_PATH << File.expand_path(File.dirname(__FILE__))
require 'generic_parser'

iosum = GenericParser.new(ARGV[0], ARGV[1])
iosum.ignore(/Logical|Time/)
iosum.data_type("integer")
iosum.columns = %w|time rio_s wio_s rkb_s wkb_s lrkb_s msecs busyp usr sys dbsy dbsy_50 dsk_tot Mx|
iosum.coltypes = %w|integer integer integer integer integer integer integer integer integer integer integer integer integer varchar(64)|
iosum.data_delimitor(/[ \t]+|\//)
#+s}

iosum.process do |arr| 
  #p arr[0].split(":")
  h,m,s=arr[0].split(":")
  arr[0]=(h.to_i*60+m.to_i)*60 +s.to_i
  arr
end


iosum.create_table

# The word "TABLE" below will be replaced by the actual tablename.
iosum.section( :title => "Aggreate IOs", :type=>"Line", 
  :query => "select time, rio_s, wio_s  from TABLE")
iosum.section( :title => "IO Bandwidth", :type=>"Line", 
  :query => "select time, rkb_s, wkb_s from TABLE")
iosum.section( :title => "Logical rKB/s", :type=>"Line", 
  :query => "select time,lrkb_s from TABLE")
iosum.section( :title => "IO Service Times", :type=>"Line", 
  :query => "select time,msecs from TABLE")
iosum.section( :title => "Disk Busy %", :type=>"Line", 
  :query => "select time,busyp from TABLE")
iosum.section( :title => "CPU Utilization %", :type=>"Line", 
  :query => "select time,usr,sys from TABLE")
iosum.section( :title => "Disk Utilization", :type=>"Line", 
  :query => "select time,dbsy,dbsy_50,dsk_tot from TABLE")

iosum.section(:title =>"Reads per second", :summarize => "rio_s")
iosum.section(:title =>"Writes per second", :summarize => "wio_s")
iosum.section(:title =>"Disk busy %", :summarize => "busyp")
iosum.section(:title =>"Disk busy", :summarize => "dbsy")
iosum.section(:title =>"CPU Utilization (USR)", :summarize => "usr")
iosum.section(:title =>"CPU Utilization (SYS)", :summarize => "sys")
iosum.section(:title =>"CPU Utilization (Total)", :summarize => "usr + sys")
