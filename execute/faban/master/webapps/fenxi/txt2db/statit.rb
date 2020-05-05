#!/bin/env ruby -w

$LOAD_PATH << File.expand_path(File.dirname(__FILE__))
require 'xanadu'

class App 
  def initialize 
    if ARGV.length != 2 then
      puts("usage: statit.rb infile outdir") 
      exit
    end 
    puts("statit.rb #{ARGV[0]} #{ARGV[1]}")
    @f = File.open(ARGV[0])
    @table= escape_filename(File.basename(ARGV[0]))
    @xh = Xanadu.new(File.basename(ARGV[0]), ARGV[1])
    @typehash = Hash[
      "metric"    , "varchar(16)", "ttime"     , "real",
      "ptime"     , "decimal(5,2)",       "CPU"       , "varchar(10)",
      "idle"      , "real",       "usr"       , "real",
      "system"    , "real",       "wait"      , "real",
      "total_per" , "real",       "total_s"   , "real",
      "stat"      , "varchar(48)", "value"     , "double",
      "groupid"   , "integer",     "interface" , "varchar(16)",
      "ipkts"     , "integer",     "ierrs"     , "integer",
      "opkts"     , "integer",     "oerrs"     , "integer",
      "colls"     , "integer",     "dfrs"      , "integer",
      "rtryerr"   , "integer",     "disk"      , "varchar(64)",
      "util"      , "real",       "xfers"     , "real",
      "rds"       , "real",       "wrts"      , "real",
      "rdbxfr"    , "real",       "wrbxfr"    , "real",
      "wtqlen"    , "real",        "svqlen"    , "real",
      "svrms"     , "real",	 "name"    , "varchar(64)",
      "mvalue" , "varchar(64)"]
  end 
  def main
    begin
      parse		
    rescue SystemCallError
      $stderr.print "Parse failed: " + $!
      raise
    ensure
      @f.close
      @xh.close
    end
  end
  def parse
    parse_meta_elap_time
    parse_cpu_stats
    parse_multi_create
    parse_net_stats
    parse_disk_stats
  end

  def parse_meta_elap_time
    while (line = @f.gets) do
      if line =~ /Hostid:/ then
        id = 0
    	cols = %w(name mvalue)
    	@xh.add_create(id, @typehash,cols)
	@xh.add_view("Metadata", "table", 1, "select name,mvalue as \"Value\" from #{@table}0 ")
        vals = line.strip.chomp.split
	@xh.add_row(id, vals[0], vals[1])
	@xh.add_row(id, vals[2], vals[3])
	@xh.add_row(id, vals[4], vals[5])
      end
      if line =~ /Elapsed Time Statistics/ then
        id = 1
	cols = %w(metric ttime ptime)
	@xh.add_create(id, @typehash, cols)
        @xh.add_view("Elapsed Time", "table", 1,
		      "select metric,ttime as \"Total Time\", ptime as \"Percent\" from #{@table}1")
        @xh.add_view("CPU Statistics", "pie", 2, 
           "select 1 as A,metric,ptime from #{@table}1")
	5.times do
	  line = @f.gets.strip.chomp
	  if line =~ /Start time/
	    vals = line.split("%")[1].split
	    @xh.add_row(0, vals[0..1].join(" "), vals[2..vals.length].join(" "))
	    vals = line.split("%")[0].split
	    @xh.add_row(0, "Total Time", vals[0])
	  else
	    l = line.split
	    @xh.add_row(id, l[1], l[0],l[3])
	  end
	end
	break
      end
    end
  end
  def parse_cpu_stats
    id = 2
    while (line = @f.gets) do
      if line =~ /^CPU Stats/ then
	cols = %w(CPU idle usr system wait total_per total_s)
	@xh.add_create(id, @typehash, cols)
        @xh.add_view("CPU Statistics", "table", 1, 
           "select CPU,idle as \"Idle%\",usr as \"User%\",system as \"Sys%\",Total_s as \"Total(s)\" from #{@table}2")
	break
      end
    end
    while (l = @f.gets.split) do
      break if l[0] =~ /^Totals/ # IGNORE THIS as this will be done in SQL 
      l.shift	# get rid of l[0]
      @xh.add_row(id, l)
    end
  end
  def parse_multi_create
    id = 3
    cols = %w(stat value groupid)
    @xh.add_create(id, @typehash,cols)
    groupid=0
    while (line = @f.gets) do
      next if line.chomp.length == 0
      break if line =~ /Network Statistics/
      if line =~ /^[ \t]*[0-9]+/ then
	print_multi_create(line, id, groupid - 1)
      else
	@xh.add_view(line.lstrip.chomp, "table", 1,
          "select Stat,value from #{@table}3 where groupid=#{groupid}")
	groupid += 1
      end
    end
  end
  def print_multi_create(l, id, groupid)
    re = Regexp.new(/(\d+[\.]*\d+)(\D+)(\d+[\.]+\d+)(\D+)/)
    md = l.chomp.match(re)
    # it is possible that there is a only one name/value pair
    md = l.chomp.match(/(\d+[\.]*\d+)(\D+)/) if (md.nil?)
    @xh.add_row(id, md[2], md[1],groupid)
    if md.length > 3
    	@xh.add_row(id, md[4], md[3],groupid)
    end
  end
  def parse_net_stats
    id = 4
    cols = %w(interface ipkts ierrs opkts oerrs colls dfrs rtryerr)
    @xh.add_create(id, @typehash,cols)
    @xh.add_view("Network Statistics", "table", 1,
      "select interface,ipkts,ierrs,opkts,oerrs,colls,dfrs,rtryerr from  #{@table}4")
    @f.gets # skip header
    while (line = @f.gets) do
      break if line =~ /Disk I\/O Statistics/ 
      @xh.add_row(id, line.split)
    end
  end
  def parse_disk_stats
    id = 5
    cols = %w(disk util xfers rds wrts rdbxfr wrbxfr wtqlen svqlen svrms)
    @xh.add_create(id, @typehash,cols)
    @xh.add_view("Average Disk Statistics(per disk)", "table", 1, 
      "select 1 as a, count(*) as Disks, avg(util) as util,avg(xfers) as xfers,avg(rds) as rds,avg(wrts) as wrts,avg(rdbxfr)/1024 as \"rKB/op\",avg(wrbxfr)/1024 as \"wKB/op\",avg(wtqlen) as wtqlen,avg(svqlen) as svqlen,avg(svrms) as svrms from  #{@table}5 where substr(disk, 1 ,2) != 'md' and util > 0")
    @xh.add_view("Total Disk Statistics(per second)", "table", 1, 
      "select 1 as a, count(*) as Disks, sum(xfers) as xfers,sum(rds) as rds,sum(wrts) as wrts,sum(rdbxfr)/1024 as \"rKB/op\",sum(wrbxfr) as \"wKB/op\",sum(rds*rdbxfr)/1048576 as \"rMB/s\", sum(wrts*wrbxfr)/1048576 as \"wMB/s\"  from #{@table}5 where substr(disk, 1 ,2) != 'md' and util > 0")
    @xh.add_view("Hot Disks ","table", 1, 
      "select Disk, util, xfers,rds,wrts,rdbxfr/1024 as \"rKB/op\",wrbxfr/1024 as \"wKB/s\",svrms from #{@table}5 where substr(disk, 1 ,2) != 'md' and util > 1 order by util desc limit 5")
    @xh.add_view("Disk Statistics", "table", 1, 
      "select Disk,util,xfers,rds,wrts,rdbxfr,wrbxfr,wtqlen,svqlen,svrms from  #{@table}5")
    @f.gets # skip header
    while (line = @f.gets) do
      @xh.add_row(id, line.split)
    end
  end
end

App.new.main
