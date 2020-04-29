module Fenxi
  # The Section class maps to one row in the EXPORT_VIEW table and has some
  # additional data attached to it. Section can have 2 states of data.
  # For tables and charts, the data is in the QueryResult class.
  # For a chart, additionally, there is a "image" needs to be generated.
  # A SummarySection is a special case of the TableSection with a sparkline

  def self.new_section(arr)
    case arr[2].downcase
    when "table" then TableSection.new(arr)
    when "summary" then SummarySection.new(arr)
    else ChartSection.new(arr)
    end
  end
  
  class Section    
    attr_reader :tablename, :desc, :display
    attr_reader :dims, :query,  :customizations
    attr_accessor :chart_data, :exception, :query_result
        
    def initialize(arr)
      @tablename, @desc, @display, @dims, @query = arr
      @display, @customizations = @display.split(";", 2)
    end
    
    def execute(db)
      return if executed?
      begin      
        first = @query.split(";",2).first
        @query_result = db.execute(first)
        send(:post_execute, db) if respond_to?(:post_execute)
      rescue Exception => e
        @exception = e
      end      
    end
    
    def executed?
      @exception or @query_result or @chart_data
    end

    def id
      @id ||="#{@tablename}_#{@display}_#{@desc}_#{@dims}_#{@query}".hash.to_s
    end

    def sparkline(row, col)
      @query_result.rows[row][col] if @query_result
    end

    # summary sections are actually multiple "sections" in the database.
    # We have to aggregate them and put them at the top of the page
    def self.aggregate_summary_sections(sections)
      summaries, others = sections.partition{|s| s.class.to_s == "Fenxi::SummarySection"}
      return others if summaries.size == 0 || summaries[0].query_result.nil?
      summary = TableSection.new([summaries[0].tablename, "Summary", "summary",1,"",0])
      types = summaries[0].query_result.types
      headers = summaries[0].query_result.headers
      rows = summaries.collect {|s| s.query_result.rows[0].flatten}
      summary.query_result = QueryResult.new(types, headers, rows)
      return [summary] + others
    end

    def self.merge(names, tool, seclist)
      s = seclist.detect{|sec| sec}
      return nil if s.nil?  #No sections could be merged
      section = TableSection.new([tool, s.desc, s.display, s.dims, s.query])
      if s.exception then
        section.exception = s.exception
      else
        qrlist = seclist.collect {|sec| sec ? sec.query_result : nil}
        section.query_result = QueryResult.merge(names, qrlist)
      end
      section
    end

    def self.execute_success?(section)
      section && section.executed? && !section.exception      
    end
  end    
  
  class TableSection < Section
  end
  
  class SummarySection < Section    
    def post_execute(db)      
      sparkline = @query.split(";",2).last
      raise "Sparkline query not specified" unless sparkline
      @query_result.rows[0] << Chart.draw_sparkline(db.execute(sparkline).rows.flatten)
      @query_result.types = %W|string float float float image|
      @query_result.headers = %W|Metric Average Max Min Trend|
      @query_result.rows[0].insert(0, @desc)
    end
  end
  
  class ChartSection < Section    
    def post_execute(db)
      @xtitle = @query_result.headers[0]
      @chart_data = Chart.prepare_chart(@query_result, @dims)      
    end
    # lazy draw image
    def image
      @image ||= Chart.draw_chart(@chart_data, @desc, @xtitle, @display, @customizations)
    end

    def self.merge(names, tool, seclist)
      s = seclist.detect{|sec| sec}
      return nil if s.nil?  #No sections could be merged
      section = ChartSection.new([tool, s.desc, s.display, s.dims, s.query])
      section.chart_data = org.jfree.data.XYSeriesCollection.new
      seclist.each_with_index do |sec, j|
        next unless Section.execute_success?(sec)
        xysc = sec.chart_data
        (0...xysc.getSeriesCount()).each do |i|
          # We have to clone coz we will be changing the name
          newseries = xysc.getSeries(i).clone
          newseries.setName(names[j%names.length] + " " + xysc.getSeries(i).getName)
          section.chart_data.addSeries(newseries)
        end
      end
      section.chart_data.getSeriesCount > 0 ? section : nil
    end
  end
end