#!/bin/env ruby -w

# Let us extend String class to provide integer? and double?
class String
  # Is an integer?
  def integer?
    self =~ /^[-]?[0-9]+$/ && self.size < 9
  end

  def bigint?
    self =~ /^[-]?[0-9]+$/ && self.size >= 9
  end

  # Is an float?
  def double?
    self =~ /^[-]?[0-9]+\.[0-9]+$/
  end
end


def escape_filename(name)
  n = name.gsub(/[\.\-\: ]/,"_")
  n = "a" << n if n=~ /^[0-9]/
  return n
end

class Xanadu
  def initialize(tbname, outdir)
	@tname_orig = tbname
	@tname = escape_filename(tbname)
    @outdir = outdir + File::SEPARATOR
    @create = File.open(@outdir+@tname + ".create", "w")
    @view = File.open(@outdir+@tname + ".view", "w")
    @tablehash = Hash.new
  end
  def close
    @create.close
    @view.close
    @tablehash.each{|k,v| v.close}
  end
  def close_file(id)
    @tablehash[@tname+id.to_s].close if @tablehash[@tname+id.to_s]
    @tablehash.delete(@tname+id.to_s)
  end
  def add_create(id, th, *cols)
    #tname is tablename
    #th is type hash
    #*cols is a variable size args of coloum names
    @create.printf("create table #{@tname}#{id} (")
    sep = ","
    for i in 0...cols.flatten.length
      d = c = cols.flatten[i]
      sep = " " if i == cols.flatten.length - 1
      c = "\"#{c}\"" if c.upcase == "GROUP"
      c = "\"#{c}\"" if c.upcase == "TIME"
      c1 = c.gsub(/[\.\+=:\*-\/\\]+/, "")
      if th.class.to_s == "String" then
        @create.printf("%s %s%s ", c1, th, sep)
      else
        @create.printf("%s %s%s ", c1, th[d], sep)
      end
        
    end
    @create.puts ")"
    @tablehash[@tname+id.to_s] = File.open(@outdir+@tname+id.to_s+".data", "w")
  end
  def add_view(title, type, dims, sql)
    @view.printf("%s|%s|%s|%d|%s\n", @tname_orig, title, type.strip, dims, sql)
  end
  def add_row(id, *args)
    #return if args.nil?
    args = args.flatten.each{|a| a.strip! if a.class.to_s == "String" }
    args.collect!{|e| e == "\"-\"" ? "" :e }
    @tablehash[@tname+id.to_s].puts(args.join("|"))
  end
  def add_nv_pair(name, value, source)
    @create.puts "insert into Metatable values('#{name}','#{value}', '#{source}')\n";
  end
end

