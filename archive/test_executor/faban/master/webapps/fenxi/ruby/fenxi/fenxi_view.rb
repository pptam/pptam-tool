require 'logger'

module Fenxi
  @@logger = Logger.new("fenxi.log")
  @@fenxi_home=ENV["FENXI_HOME"]
  
  class FenxiView < Struct.new(:indir,:outdir,:fdb)
    include Fenxi::FenxiUtil

    # Called only by "process". Compare builds an inmemory db & hence no call
    def execute
      self.fdb = FenxiDatabase.new({:path=>outdir})
      mytime("Opening Database") { fdb.load_from_disk }
      mytime("Executing queries") { fdb.execute_all_sections}
      mytime("Generating html pages") { generate_html }
    end
    
    def generate_html # Called directly by compare
      IndexPage.new(fdb, outdir).to_html
      fdb.tools.keys.each { |k| ToolPage.new(fdb, k, outdir).to_html }
    end
  end

  class BasePage
    include ERB::Util   # for h()
    FENXI_HOME = ENV["FENXI_HOME"]
    FENXI_CSS_LOC = ENV["FENXI_CSS_LOC"]
    attr_accessor :infile, :outfile
    
    def to_html
      File.open(@outfile, "w") do |f|
        f.write(render_erb(@infile, binding))
      end
    end

    # This can throw an exception, but we catch it above
    def render_erb(file, mybinding)
      e = ERB.new(File.read("#{FENXI_HOME}/ruby/fenxi/#{file}"))
      e.result(mybinding)
    end
    def render_partial(file, mybinding, outvar)
      e = ERB.new(File.read("#{FENXI_HOME}/ruby/fenxi/#{file}"), nil, nil, outvar)
      e.result(mybinding)
      outvar
    end
  end

  class ToolPage < BasePage
    def initialize(fdb, tool, outdir)
      @infile = "tool_page.erb"    
      @outfile = outdir + "/" + tool+".html"      
      @tool = tool
      @destdir = outdir     
      @sections = Section.aggregate_summary_sections(fdb.tools[@tool])
      @imageid = 0
      @content=""            
      @sections.each_with_index do |section, id|
        begin          
          @content = @content + render_erb("section_view.erb", binding)
        rescue Exception => e
          $stderr.puts "Rendering Error: " + e.message
          $stderr.puts e.backtrace[0..5].join("\n")
        end
      end  
    end

    # store the image on disk
    def imagestore(img)
      imgfile = "#{@destdir}/#{@tool}_#{@imageid}.png"
      File.open(imgfile, "w") { |f| f.write(img)}
      @imageid += 1
      File.basename(imgfile)
    end    
  end 

  class IndexPage < BasePage
    def initialize(fdb, outdir)
      @infile = "index.erb"    
      @outfile = "#{outdir}/index.html"
      @name = fdb.name
      @tools = fdb.tools.keys
    end 
  end
end