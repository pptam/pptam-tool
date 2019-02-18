module Fenxi
  module FenxiUtil
    def mytime(name, &block)
      start = Time.now
      printf("%-48s ", "#{name} ..." )
      block.call
      printf("%4.2fs\n", (Time.now - start))
    end

    def self.pretty_tool_list(tools)
      return nil if tools.nil?
      # { :host => [[realname, prettyname],..] }
      h = Hash.new{|h, k| h[k] = []}
      pretty_tools = tools.collect{|e| [e, *parse_tool_name(e)]} #splat :-)
      #[[toolname, hostname, prettyname] ... ]
      pretty_tools.each{|e| h[e[1]||"nil"] << [e[0], e[2]]}
      h
    end

    # parse a toolname and return [host, toolname] if we understand it
    # ex. mpstat.out.bursar => [bursar, mpstat]
    # 1y.detail.xan => [nil, 1y.detail]
    def self.parse_tool_name(tool)
      return nil if tool.nil?
      modtool = tool.gsub(/\.log|\.xan|\.out|.gz|.txt/, "")
      f = modtool.split(/\./)
      return [nil, modtool] if f.length < 2 # test.xan
      return [nil, modtool] if f[-1] =~ /^[0-9]+/ #test.xan.1y
      return [nil, modtool] if f[0] =~ /^[0-9]/ #1y.detail.xan
      [f[-1], f[0...f.length-1].join(".")]
    end
  end
end
