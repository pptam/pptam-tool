# =GenericParser=
#
# Most tool output is like a set of columns repeated over time.
# For ex, vmstat, the output is repeated every "interval" times
# For such tools, it should be fairly easy to write a generic parser
# that understands the output and prepares the data for fenxi load.

require 'zlib'
# Let us extend String class to provide integer? and double?
class String
  # Is an integer?
  def integer?
    self =~ /^[-]?[0-9]+$/
  end

  # Is an float?
  def double?
    self =~ /^[-]?[0-9]+\.[0-9]+$/
  end
end


class GenericParser
  attr_accessor :columns, :coltypes
  
  # Creates a new generic parser.
  # +srcfile+ The file to be parsed
  # +outputdir+ Location of the parsed data
  def initialize(srcfile, outputdir)
    raise "Usage: script file tmpdir" if (srcfile.nil? or outputdir.nil?)    
    @ignore = nil
    @columns = []
    @coltypes = []
    @data_type = "integer"
    @auto_col_type = true
    @header = nil
    @cycle = nil
    @data_delimitor = nil #/[ \t]+/
    @src = srcfile
    if @src =~ /\.gz$/ then
      @srcfd = Zlib::GzipReader.open(@src)
    else
      @srcfd = File.open(@src)
    end
    @src
    @outdir = outputdir + File::SEPARATOR 
    @time = 0
    @data = []
    @orig_file = File.basename(srcfile)
    @table = escape_filename(@orig_file)
    @createf = File.open(@outdir+@table + ".create", "w")
    @viewf = File.open(@outdir+@table + ".view", "w")
    @dataf = File.open(@outdir+@table + ".data", "w")    
  end
  
  # Column types can be auto-found. This is expensive.
  # If the user knows the type, they can specify it via
  # this func, and the auto finding of column types will be
  # disabled
  def data_type(type)
    @data_type = type
    @auto_col_type = false    
  end
  
  # Lines matching this regular expression will be ignored
  # A block can also be passed, which should return true 
  # if the line needs to be ignored
  # +re+ The regular expression. 
  # +block+ Block of code (optional)
  def ignore(re, &block)
    @ignore = re
    @ignore_block = block
  end
  
  # The column names for the table will be derived from the lines
  # matching this regular expression. The first line that matches
  # this regular expression is split to get the column names.
  # +re+ The regular expression
  def header(re)
    @header = re
  end
  
  # We maintain an implicit "Time" field. Time is incremented whenever
  # the regular expression is matched. if @cycle is nil, "Time"
  # is not outputted
  # +re+ The regular expression
  def cycle(re)
    @cycle = re
  end

  # What do we use for split?
  def data_delimitor(re)
    @data_delimitor = re
  end
  
  # Add a new view. In fenxi, the view consists of table, title, type,dims and 
  # query. These are specified via a hash. You do not need to specify
  # table, as it is already known. dims has a default value of 1.  
  # The query param can be an Array in which case, we generate the query
  # only if at least two entries in the array are valid columns. This
  # is useful for ex in vmstat where there are different columns for vmstat
  # on solaris and linux
  def section(h)
    if h[:summarize] then
      c = h[:summarize]
      h[:type] = "Summary"
      h[:query] = "select avg(#{c}),max(#{c}),min(#{c}) from #{@table};"
      h[:query] << "select #{c} from #{@table}"
    end
    if h[:query].class == Array then
      # Insert into Db only if at least two columns are present in TABLE
      found_cols = @columns & h[:query]
      if found_cols.length > 1 then
        new_query = sprintf("select Time,%s from %s", found_cols.join(","),
          @table)
        @viewf.printf("%s|%s|%s|%d|%s|\n", @orig_file,h[:title], h[:type],
          h[:dims]||1, new_query)
      end
    else
      @viewf.printf("%s|%s|%s|%d|%s|\n", @orig_file,h[:title], h[:type],
        h[:dims]||1, h[:query].gsub("TABLE", @table))
    end
  end

  # This is where the data is processed and output is generated
  def process(&block)
    while not @srcfd.eof?
      line = @srcfd.readline      
      next if ignore?(line)
      if (line =~ @header and @columns.length == 0) then 
        @columns = line.split
        @coltypes = []
        @columns.each{ @coltypes << @data_type} 
      end
      if @cycle and line =~ @cycle then
        @time += 1
      end
      next if line =~ @header
      next if line =~ /^$/
      next if line =~ /always/
      fields = line.split(@data_delimitor)
      fields = yield(fields) if block

      auto_type_columns(fields) if @auto_col_type
            
      #Dump out the data
      if (@cycle) then      
        @dataf.puts(@time.to_s + "|" + fields.join("|"))
      else
        @dataf.puts(fields.join("|"))
      end
    end       
  end
  
  # Dump out the create table string. Make sure you have sanitized column
  # names before calling this function.
  def create_table
    @createf.puts(create_table_str) 
  end
  
  # Does this column exist?
  def has_column?(col)
    @columns.select { |c| c == col}
  end
  
  # Auto determine the field types.
  # precedence String > Double > int
  def auto_type_columns(fields)
    fields.each_with_index do |f, i|
      next if f.integer?
      if f.double? then
        @coltypes[i] = "double" if @coltypes[i] == "integer"
      else
        @coltypes[i] = "varchar(256)"
      end
    end
  end

  def close
    @createf.close
    @dataf.close
    @viewf.close
  end
  
  private
  # Generate the create table string from the column headers
  def create_table_str    
    ret = "create table #{@table} ("
    ret += "Time integer, " if @cycle
    0.upto(@columns.length - 2) do |i|            
      ret += @columns[i] + " " + @coltypes[i] + ", "
    end
    ret += @columns[-1] + " " + @coltypes[-1] + ")"    
  end
    
  def escape_filename(name)
    n = name.gsub(/[\.\-\: ]/,"_")
    n = "a" << n if n=~ /^[0-9]/
    return n    
  end
  
  def ignore?(line)    
    if @ignore.nil? then
      if (@ignore_block) then
        @ignore_block.call(line)
      else
        false         
      end
    else
      line =~ @ignore
    end
  end
end
