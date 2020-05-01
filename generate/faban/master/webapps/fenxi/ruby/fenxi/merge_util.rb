require 'fenxi'
module Fenxi
  module MergeUtil

    # Given a list of database, and tools, compare them
    # Returns a list of sections
    # compare_tools([fdb_a, fdb_b, fdb_c], "vmstat_a", "["vmstat_b", "vmstat_c"])
    def self.compare_tools(expts, first, rest)
      names = expts.collect {|e| e.name}
      [first, *rest].each_with_index do |tool, i|
        expts[i].execute_sections_for_tool(tool)
      end
      result = []
      expts[0].tools[first].each do |section|        
        seclist = []
        seclist <<  (Section.execute_success?(section) ? section : nil)
        rest.each_with_index do |rtool, i|          
          sect = expts[i+1].find_section_similar_to(rtool, section)         
          if Section.execute_success?(sect) then
            seclist << sect
          else
            seclist << nil
          end
        end        
        newsec = section.class.merge(names, first, seclist)
        result << newsec if newsec
      end
      result
    end

    # Given an array of arrays, find what tools can be compared +Returns+: Hash
    # {"vmstat.a" => ["vmstat.b", vmstat.c"], ..} This means vmstat.a can be
    # comapred with vmstat.b and vmstat.c
    # find_comparable_tools([["vmstat_a", "mpstat_a"],["vmstat_b", "mpstat_b"]]
    def self.find_comparable_tools(arr)
      h = Hash.new{|h,k| h[k]=[]}
      (1...arr.size).each do |i|
        arr[0].each do |a|
          h[a] << find_matching_tool(a, arr[i])
        end
      end
      if (arr.size == 2) then
        h = h.delete_if { |k,v| v[0].nil?}
      end
      h
    end

    # Find a matching tool from +list+ for +tool+
    # must match a min of 5 chars at beginning unless toolname is less than 4
    # example: find_matching_tool("vmstat",["mpstat","iostat","vmstat"]
    def self.find_matching_tool(tool, list)
      t = list.inject("") do |match, l|
        longest_match(tool, match) > longest_match(tool, l) ? match : l
      end
      min_match = tool.length > 5 ? 5 : tool.length
      longest_match(tool, t) > min_match ? t : nil
    end

    # Match 2 strings to get the number of chars matched at begining
    def self.longest_match(str1, str2)
      return -1 if str1.nil? or str2.nil?
      return 100 if str1 == str2
      length = (str1.size > str2.size ? str2.size : str1.size)
      match = 0
      (0...length).each do |i|
        break if str1[i] != str2[i]
        match += 1
      end
      match
    end
  end  
end