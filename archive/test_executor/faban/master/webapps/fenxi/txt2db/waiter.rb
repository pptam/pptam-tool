#!/bin/env ruby -w

$LOAD_PATH << File.expand_path(File.dirname(__FILE__))
require 'xanadu'
require 'time'

class App 
  def initialize 
    if ARGV.length != 2 then
      puts("usage: waiter.rb f outdir") 
      exit
    end 
    puts("waiter.rb #{ARGV[0]} #{ARGV[1]}")
    if ARGV[0] =~ /\.gz$/
      @f =  Zlib::GzipReader.open(ARGV[0])
    else
      @f = File.open(ARGV[0])
    end

    @table= escape_filename(File.basename(ARGV[0]))
    @xh = Xanadu.new(File.basename(ARGV[0]), ARGV[1])
    @h = Hash.new([])
    @tarray = Array.new
  end 

  def main
    begin
      parse
      dump
    rescue SystemCallError
      $stderr.print "Parse failed: " + $!
      raise
    ensure
      @f.close
      @xh.close
    end
  end

  def parse
    return if @f.eof?
    prev = @f.readline
    starttime = Time.parse(prev)

    while not @f.eof? 
      line = @f.readline
      if line =~ /EVENT/
        t = Time.parse(prev)
        time_from_begin =  t - starttime
        3.times do
          @f.readline #ignore --- line
          vals =  @f.readline.split
          finish = vals.length - 2
          key = vals[2..finish].to_s
          next if vals.last.to_i < 5
          if not @h.has_key?(key)
            @h[key]=Array.new(0)
          end
          @h[key][time_from_begin] = vals.last
          @tarray.push(time_from_begin)
        end # end of 3.times
      end # end of if EVENT
      prev = line
    end  #end of while loop
    prev = line
  end
  def dump
    # now print them out
    headers=["Time"]
    @h.keys.each{|hdr| headers << hdr}
    @xh.add_create(0, "INTEGER" , headers)
    @xh.add_view("Waiter statistics", "Stacked area", 1, "select * from #{@table}0")

    @tarray.each do |t|
      row = [t.to_i]
      @h.each do |k, v|
        value = v[t].nil? ? 0 : v[t].to_i
        row << value
      end
      @xh.add_row(0, row)
    end
  end

end

App.new.main
