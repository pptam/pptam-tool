# #!/bin/env ruby -w

$LOAD_PATH << File.expand_path(File.dirname(__FILE__))
require 'xanadu'

class App 
  def initialize 
    if ARGV.length != 2 then
      puts("usage: uperf.rb infile outdir") 
      exit
    end 
    puts("uperf.rb #{ARGV[0]} #{ARGV[1]}")
    @f = File.open(ARGV[0])
    @table= escape_filename(File.basename(ARGV[0]))
    @xh = Xanadu.new(File.basename(ARGV[0]), ARGV[1])
    @typehash = Hash.new("double")
    %W|txn name mvalue nic opkts ipkts obits ibits|.each do |col|
      @typehash[col] = "varchar(64)"
    end
    %W|hostname etime data throughput operations errors|.each do |col|
      @typehash[col] = "varchar(64)"
    end
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
    while (line = @f.gets) do      
      if line =~ /^Starting/
        id = 0
    	cols = %w(name mvalue)
    	@xh.add_create(id, @typehash,cols)
	@xh.add_view("Metadata", "table", 1, "select name,mvalue as \"Value\" from #{@table}0 ")
        vals = line.strip.chomp.split
	@xh.add_row(id, "Profile", vals[4].split(":").last)
	@xh.add_row(id, "Threads", vals[1])
        id = 1
	cols = %w(ttime txn mbps data_tx ops)
	@xh.add_create(id, @typehash, cols)
        @xh.add_view("Throughput", "line", 2,
          "select ttime, txn, mbps from #{@table}1")
      elsif line =~ /^Txn/ then
        vals = line.strip.chomp.split
	@xh.add_row(id, vals[4], vals[0], vals[7], vals[1], vals[-2])
      elsif line =~ /^Total/
        @xh.add_row(0, "Total Mbps", line.split[7])
      elsif line =~ /^Netstat/ then
        id = id + 1        
        cols = %w|nic opkts ipkts obits ibits|
        @xh.add_create(id, @typehash, cols)
        @xh.add_view("Throughput", "table", 1, "select * from #{@table}#{id}")
        while (line = @f.gets) do
          break if line =~ /^$/
          next if line =~ /^--/ or line =~ /^Nic/
          @xh.add_row(id, line.split)
        end
      elsif line =~ /^Run Statistics/ then
        id = id + 1        
        cols = %w|hostname etime data throughput operations errors|
        @xh.add_create(id, @typehash, cols)
        @xh.add_view("Run Statistics", "table", 1, "select * from #{@table}#{id}")
        while (line = @f.gets) do
          break if line =~ /^$/
          next if line =~ /^--/ or line =~ /^Host/
          @xh.add_row(id, line.split)
        end
      end
    end
  end
end

App.new.main
