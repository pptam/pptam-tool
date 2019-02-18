require 'fileutils'

module Fenxi
  class FenxiCompare
    include FenxiUtil
    def initialize(*args)
      args.flatten! # Why?
      @outdir = args.last
      @dblist = args[0..-2].collect {|loc| FenxiDatabase.new({:path=>loc})}
    end
  
    def execute
      mytime("Opening databases") do        
        @dblist.each{|db| db.load_from_disk}
      end
      fnew=nil
      mytime("Comparing experiments") do
        name = "Compare_" + @dblist.collect{|e| e.name}.join("_")
        fnew = FenxiDatabase.new
        fnew.compare_loaded_databases(@dblist)
        fnew.name = name
      end
      FileUtils.mkdir @outdir
      fv = FenxiView.new("", @outdir, fnew)
      mytime("Generating html pages") { fv.generate_html }
    end
  end
end
