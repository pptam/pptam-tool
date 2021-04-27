#!/bin/env ruby -w

$LOAD_PATH << File.expand_path(File.dirname(__FILE__))
require 'xanadu'

class App 
  def initialize 
    if ARGV.length != 2 then
      puts("usage: tpccmeta.rb infile outdir") 
      exit
    end 
    @f = File.open(ARGV[0])
    @table= escape_filename(File.basename(ARGV[0]))
    @xh = Xanadu.new(File.basename(ARGV[0]), ARGV[1])
    @typehash = Hash[
      "name"    , "varchar(64)", "value"     , "varchar(256)",
      "groupid" , "integer" ]
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
    parse_etc_system
    parse_tpcso_params
  end

  def parse_etc_system
    while (line = @f.gets) do
      if line =~ /Contents of \/etc\/system/ then
	@f.gets # get rid of one line
        groupid = id = 0
    	cols = %w(name value groupid)
    	@xh.add_create(id, @typehash,cols)
	@xh.add_view("Contents of /etc/system", "table", 1, 
		"select name, value from #{@table}#{id} where groupid = #{groupid}")
	while line = @f.gets do
	  return if line =~ /^$/
	  vals = line.chomp.split[1].split("=")
	  @xh.add_row(id, vals[0], vals[1], groupid)
	end
      end
    end
  end
  def parse_tpcso_params
    while (line = @f.gets) do
      if line =~ /TPCSO PARAMETERS ARE/ then
	# get rid of two lines
	2.times{@f.gets}
        groupid = id = 1
    	cols = %w(name value groupid)
    	@xh.add_create(id, @typehash,cols)
	@xh.add_view("TPCSO PARAMETERS", "table", 1, 
		"select name,value from #{@table}#{id} where groupid = #{groupid}")
	while line = @f.gets do
	  return if line =~ /^$/
	  vals = line.chomp.split(":")
	  @xh.add_row(id, vals[0], vals[1].strip, groupid)
	end
      end
    end
  end

end

App.new.main
