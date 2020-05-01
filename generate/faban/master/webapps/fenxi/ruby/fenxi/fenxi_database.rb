require 'logger'

module Fenxi  
  class FenxiDatabase    
    EXPORT_VIEW_SQL = "select tablename, sectiondesc, displaytype, dims, viewquery from EXPORT_VIEW"
    TABLE_LIST_SQL = "select TABLENAME from sys.systables where tabletype ='T'" 
    NAME_SQL = "select metavalue from metatable where metaname='name'"
    
    attr_reader :tools, :db, :num_queries, :path
    attr_accessor :name

    def initialize(attributes=nil)
      @path = attributes[:path] if attributes
      @tools = Hash.new {|h, k| h[k] = []}      
      @tables = []
    end
  
    # Open the database and fill in some variables.
    def load_from_disk
      @db = Database.new(@path + "/xanaDB")
      @name = @db.execute(NAME_SQL).rows[0][0]      
      viewobjects = @db.execute(EXPORT_VIEW_SQL)            
      viewobjects.rows.each do |v|        
        @tools[v[0]] << Fenxi.new_section(v)
      end
      @num_queries = viewobjects.length
      @tables = @db.execute(TABLE_LIST_SQL).rows.flatten
    end

    def all_sections
      @tools.values.flatten
    end

    def find_section_similar_to(tool, section)
      @tools[tool].find do |sec|
        (sec.desc == section.desc) && (sec.display == section.display)
      end
    end

    def find_section_with_id(id)
      all_sections.detect {|s| s.id == id}
    end
    
    def execute_all_sections # used in static process
      all_sections.each {|s| s.execute(@db) unless s.executed? }
    end

    def sections_for_tool(tool) # used in compare
      @tools[tool]
    end
    
    def execute_sections_for_tool(tool) # used in compare
      sections_for_tool(tool).each {|s| s.execute(@db) unless s.executed? }
    end

    def compare_loaded_databases(dblist)
      tools = dblist.collect {|db| db.tools.keys}
      comparable_tools = MergeUtil.find_comparable_tools(tools)
      comparable_tools.each do |first, rest|
        result = MergeUtil.compare_tools(dblist, first, rest)
        new_tool = "#{first}_#{rest.join("_")}"
        @tools[new_tool] = result if result.length > 0
      end
    end
    
  end
end