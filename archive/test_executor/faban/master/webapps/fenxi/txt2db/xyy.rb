#!/bin/env ruby -w

$LOAD_PATH << File.expand_path(File.dirname(__FILE__))
require 'xanadu'

class App 
  # Constructor, do sanity checks
  def initialize 
    if ARGV.length != 2 then
      puts("usage: xyy.rb infile outdir") 
      exit
    end 
    @f = File.open(ARGV[0])
    @title = @f.gets
    if not @title =~ /^Title/ then
      puts "#{ARGV[0]}: First line does not begin with Title:"
      exit
    end
    @table= escape_filename(File.basename(ARGV[0]))
    @xh = Xanadu.new(File.basename(ARGV[0]), ARGV[1])
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
    id = 1
    while (line = @f.gets) do
      if line =~ /^Section:/ then
        parse_section(line.split(":")[1].chomp, id)
        id += 10
      end
    end
  end

  # Parse a section
  def parse_section(hdr, id)
    cols = []
    allvalues=[]
    typehash = Hash.new("integer")	#assume integer type
    display="table"			# default display is table
    while (line = @f.gets) do
      next if line =~ /^[#-]/
      next if line =~ /^$/
      if line =~ /^Section:/ then
        if allvalues.length > 0 then
          @xh.add_create(id, typehash, cols)
          @xh.add_view(hdr, display, 1, "select #{cols.join(", ")} from #{@table}#{id}")
          allvalues.each { |row| @xh.add_row(id, row) }
          @xh.close_file(id)
        end
        parse_section(line.split(":")[1].chomp, id+1)
        return
      end
      if line =~ /^Display:/ then
        display=line.split(":")[1].downcase.chomp
        display = "table" if (display.chomp.strip == "html")
        next
      end
      #plot:Sysbench Read Only:line:1:select 1,2 from TABLE
      if line =~ /^Plot/ then
        plot=line.split(":")
        @xh.add_view(plot[1],plot[2],plot[3],plot[4].gsub(/TABLE/,"#{@table}#{id}").chomp)
        next
      end
      values = line.strip.split(/\t+\s*|\s\s+\t*/)
      if (cols.length == 0) then
        cols = values
	# get rid of special chars from headers as sql does not like it
        cols.each{|c| c.gsub!(/[\. ()\/%]/, "_"); c.chomp!}
	# as headers may have spaces, enclose them in quotes
        cols.collect!{|x1| "\"" + x1 +"\""}
        #cols = cols.collect do |x| "\"" + x +"\""}
        next
      end
      #precedence String > Double > int
      for i in 0...values.length do
        next if values[i].integer?
        if values[i].bigint?
          typehash[cols[i]] = "bigint" if typehash[cols[i]] == "integer"
        elsif values[i].double?
          typehash[cols[i]] = "double" if typehash[cols[i]] == "integer"
        else
          typehash[cols[i]] = "varchar(256)"
          values[i] = "\"#{values[i].strip.chomp}\""
        end
      end
      allvalues.push(values)
    end
    return if allvalues.length == 0
    @xh.add_create(id, typehash, cols)
    @xh.add_view(hdr, display, 1, "select #{cols.join(", ")} from #{@table}#{id}")
    allvalues.each { |row| @xh.add_row(id, row) }
  end

end

App.new.main
