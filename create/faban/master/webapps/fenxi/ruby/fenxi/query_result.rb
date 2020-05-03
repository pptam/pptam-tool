module Fenxi
  class QueryResult < Struct.new(:types, :headers, :rows)

    # Merge an array of QueryResults. Can contain nulls
    def self.merge(names, qrlist)
      rows = join_rows(qrlist)
      headers = join_headers(qrlist)
      headers = update_headers(names, headers)
      types = join_types(qrlist)
      QueryResult.new(types, headers, rows)
    end
    
    def self.find_join_keys(qrlist)
      keys = []
      qrlist.each do |qr|
        qr.rows.each {|r| keys << r[0]} if qr
      end
      keys.uniq
    end

    def self.join_rows(qrlist)
      hash = Hash.new{|h, k| h[k] = []}
      keys = find_join_keys(qrlist)
      no_cols = qrlist.detect{|qr| qr}.headers.size
      # [foobar, a1, a2] & [foobar, b1, b2] => [foobar, a1, b1, a2, b2]
      keys.each do |key|
        (1...no_cols).each do |i|
          qrlist.each do |qrresult|
            row = qrresult.rows.find{|r| r[0] == key} if qrresult
            hash[key] << (row ? (row[i] || "-") : "-")
          end
        end
      end
      return keys.collect{|key| [key, hash[key]].flatten}
    end

    def self.join_headers(qrlist)
      ele = qrlist.detect{|qr| qr} #1st non-nil query result
      if ele then
        no_cols = ele.headers.size
        headers = [ele.headers[0]]
        (1...no_cols).each do |i|
          qrlist.each do |qr|
            headers << (qr ? qr.headers[i] : "NULL") #FIXME:
          end
        end
        return(headers)
      end
    end

    def self.join_types(qrlist)
      ele = qrlist.detect{|qr| qr} #1st non-nil query result
      if ele then
        types = [ele.types[0]]
        ele.types[1..-1].each do |type|
          qrlist.each { types << type }
        end
        return (types)
      end
    end

    # When we are doing compare, we need to qualify column headers with the
    # runid. This function does that.
    # Given (["A", "B"], ["Name", "Value1", "Value2"]) returns
    # [Name, "A Value1", "B Value2]
    def self.update_headers(names, headers)
      names_length = names.length
      newheaders = [headers.first]
      for j in 1...headers.length do
        newheaders << "#{names[((j-1)%names_length)]} #{headers[j]}"
      end
      newheaders
    end
  end
end