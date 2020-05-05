module Fenxi
  module Chart
    
    # Convert a java BufferedImage to a String.
    def self.java_buffered_img_to_string(img)
      baos = java.io.ByteArrayOutputStream.new(25*1024)
      javax.imageio.ImageIO.write(img, "png", baos)
      bytes = baos.toByteArray()
      string =  String.from_java_bytes bytes
      return (string)
    end

    # This methods converts data to a format that JFreechart understands
    def self.prepare_chart(data, dims)
      collection = org.jfree.data.XYSeriesCollection.new    
      s = (dims == "2") ? get_data_dims_2(data) : get_data_dims_1(data)    
      s.each{ |x| collection.addSeries(x) }
      collection
    end

    # This method renders the prepared data to a png stream
    def self.draw_chart(chartdata, hdr, xtitle, display, other)
      img = org.fenxi.chart.FenxiChartFactory.newChart(chartdata, hdr, display, 
        xtitle, hdr, other).draw
      java_buffered_img_to_string(img)
    end
  
    def self.draw_sparkline(rv)
      img = org.fenxi.view.Sparkline.new(rv.to_java(:float)).draw  
      java_buffered_img_to_string(img)
    end
  
    # data is of type [time, usr, sys, idle]
    def self.get_data_dims_1(values)
      xyseries = []
      cols = values.headers.size
      #need to check if types are integers or float
      if values.types.detect{|e| e == "string"} then
        raise %Q|Data is not numerical. Column types are #{values.types.inspect}|
      end
      
      (1...cols).each {|i| xyseries <<  org.jfree.data.XYSeries.new(values.headers[i])}
      values.rows.each do |r|
        (1...r.length).each do |i|
          xyseries[i-1].add(r[0], r[i])
        end
      end
      return (xyseries)
    end
    
    # data is of type [x, series_name, y] ex: iostat [time, disk, rps]
    def self.get_data_dims_2(values)
      if values.rows[0].length != 3
        raise "This data cannot be shown with dims == 2 #{values.rows[0].inspect}"
      end
      xyseries = {}
      values.rows.each do |r|
        key = r[1]
        xyseries[key] = org.jfree.data.XYSeries.new(key) unless xyseries[key]
        xyseries[key].add(r[0], r[2])
      end
      return (xyseries.values)
    end

    def self.supported_chart_types
      org.fenxi.chart.Chart.chart_names
    end
  end
end
