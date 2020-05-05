#!/bin/env ruby -w

$LOAD_PATH << File.expand_path(File.dirname(__FILE__))
require 'xanadu'

class App 
  # Constructor, do sanity checks
  def initialize 
    if ARGV.length != 2 then
      puts("usage: summary.rb infile outdir") 
      exit
    end 
    @f = File.open(ARGV[0])
    @title = @f.gets
    if not @title =~ /TPCCS Report/ then
      puts "Not a valid TPC-C/TPCSO/OLTPnet summary file"
      exit
    end
    @table= escape_filename(File.basename(ARGV[0]))
	@xh = Xanadu.new(File.basename(ARGV[0]), ARGV[1])
#    @xh = Xanadu.new(@table, ARGV[1])
    @typehash = Hash[
      "METANAME",     "varchar(64)",
      "METAVALUE",    "varchar(64)",
      "TX_TYPE",      "varchar(64)",
      "TX_COUNT",     "integer",
      "TX_MIX",       "float",
      "REQD_MIX",     "varchar(16)",
      "RT_TXN",       "varchar(32)",
      "RT_AVG",       "float",
      "RT_MAX",       "float",
      "RT_90TH",      "float",
      "RT_REQD_90TH", "integer",
      "TH_TXN",       "varchar(32)",
      "TH_AVG",       "float",
      "TH_MAX",       "float",
      "TH_90TH",      "float",
      "TH_REQD_90TH", "integer",
      "REQUIREMENT",  "varchar(64)",
      "NUM",          "float",
      "STATUS",       "varchar(16)",
      "USERS",        "float",
      "REAL_USERS",   "float",

    ]
  end 

  # Main loop
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
    parse_metadata
    parse_txn_mix
    parse_resp_time
    parse_think_time
    parse_misc
    parse_little
  end

  def parse_metadata
    cols = %w(METANAME METAVALUE)
    id = "_META"
    @xh.add_create(id, @typehash, cols)
    display = "table"
    @xh.add_view("Metadata", "table", 1, "select METANAME,METAVALUE from #{@table+ id} ")
    while (line = @f.gets) do
      next if line.chomp =~ /^$/
      next if line.chomp =~ /^-/
      next if line =~ /^Test Data/
      break if line =~ /^TRANSACTION MIX/
      if line =~ /^MQTh/ then
        tpm = line.split(":")[1]
	tpm = tpm.split[0]
        @xh.add_row("_META","Throughput (tpmS)", tpm) 
	next
      end
      
      @xh.add_row(id,line.split(":"))
    end
  end

  def parse_txn_mix
    cols = %w(TX_TYPE TX_COUNT TX_MIX REQD_MIX)
    id ="_TXN_MIX" 
    @xh.add_create(id, @typehash, cols)
    @xh.add_view("Transaction Mix", "table", 1,
      "select TX_TYPE, TX_COUNT, TX_MIX, REQD_MIX from #{@table + id} ")
    while (line = @f.gets) do
      next if line.chomp =~ /^$/
      next if line.chomp =~ /^TYPE/
      next if line.chomp =~ /^-/
      if line =~ /^Total number of transactions/
        @xh.add_row("_META",line.split("=")) 
	next
      end
      if line =~ /^TPC-C Requirement/
        @xh.add_row("_META",line.split(":")) 
	next
      end
      break if line =~ /^RESPONSE TIMES/
      vals = line.split
      vals.each{|v| v.gsub!(/%/, "")}
      @xh.add_row(id,vals)
    end
  end

  def parse_resp_time
    cols = %w(RT_TXN RT_AVG RT_MAX RT_90TH RT_REQD_90TH)
    id="_RT"
    @xh.add_create(id, @typehash, cols)
    @xh.add_view("Response Times", "table", 1,
      "select RT_TXN, RT_AVG, RT_MAX,RT_90TH,RT_REQD_90TH from #{@table + id} ")
    while (line = @f.gets) do
      next if line.chomp =~ /^$/
      if line =~ /^TPC-C Requirement/
        @xh.add_row("_META",line.split("=")) 
	next
      end
      break if line =~ /^THINK/
      break if line =~ /conn/
      @xh.add_row(id,line.split)
    end
  end

  def parse_think_time
    cols = %w(TH_TXN TH_AVG TH_MAX TH_90TH TH_REQD_90TH)
    id="_TH"
    @xh.add_create(id, @typehash, cols)
    @xh.add_view("Think Times", "table", 1,
      "select TH_TXN, TH_AVG, TH_MAX,TH_90TH,TH_REQD_90TH from #{@table + id} ")
    while (line = @f.gets) do
      next if line =~ /^THINK/
      next if line.chomp =~ /^$/
      break if line =~ /^MISC/
      @xh.add_row(id,line.split)
    end
  end

  def parse_misc
    cols = %w(REQUIREMENT NUM STATUS)
    id="_MISC"
    @xh.add_create(id, @typehash, cols)
    @xh.add_view("Misc. TPC-C Requirements", "table", 1,
      "select REQUIREMENT, NUM, STATUS from #{@table + id} ")
    while (line = @f.gets) do
      next if line.chomp =~ /^$/
      next if line.chomp =~ /Retrys/
      break if line =~ /^LITTLE/
      vals = line.split(/  /)
      vals = vals.find_all{|v| v.to_s.length > 0}
      @xh.add_row(id,vals)
    end
  end

  def parse_little
    cols = %w(USERS REAL_USERS)
    id="_LITTLE"
    @xh.add_create(id, @typehash, cols)
    @xh.add_view("Little's Law Verification", "table", 1,
      "select USERS, REAL_USERS from #{@table + id} ")
    @f.gets
    num_users = @f.gets.split("=")[1].chomp
    real_users = @f.gets.split("=")[1].chomp
    @xh.add_row(id,num_users, real_users)
  end

end

App.new.main
