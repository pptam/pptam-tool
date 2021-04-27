module Fenxi

  class Database
    def initialize(path)
      @path = path
      org.apache.derby.jdbc.EmbeddedDriver
      @conn = java.sql.DriverManager.getConnection("jdbc:derby:#{@path}")
    end
     
    # Execute a query. Returns a QueryResult. Throws exception on error
    def execute(query)
      use_limit = false
      if query =~ /limit[ ]+[0-9]+/ then
        m = /limit[ ]+([\d]+)/.match(query)
        limit = m[1].to_i
        query.gsub!(/limit[ ]+([\d]+)/, "")
        use_limit = true
      end      
      stmt = @conn.createStatement
      rs = stmt.executeQuery(query)
      rsm = rs.getMetaData()
      res = QueryResult.new(get_types(rsm), get_column_names(rsm), [])
      while (rs.next) do
        row = []
        rsm.getColumnCount().times do |i|
          row << case res.types[i]
          when "float" then rs.getFloat(i+1)
          when "int" then rs.getInt(i+1)
          else rs.getString(i+1) #bigint is returned as string
          end
        end
        res.rows << row
        if use_limit then
          return (res) if limit == 0
          limit = limit - 1
        end
      end
      stmt.close
      return res
    end

    private
    
     # get column types
    def get_types(rsm)
      (1..rsm.getColumnCount()).collect{|i| gettype(rsm.getColumnType(i))}
    end

    # get column headers
    def get_column_names(rsm)
       (1..rsm.getColumnCount()).collect{|i| rsm.getColumnName(i)}
    end

    @@db_types = {
      java.sql.Types::INTEGER => "int", java.sql.Types::FLOAT => "float",
      java.sql.Types::DOUBLE => "float", java.sql.Types::DECIMAL => "float",
      java.sql.Types::BIGINT => "bigint", java.sql.Types::REAL => "float"
    }  
    def gettype(type)
      return @@db_types[type] || "string"
    end
  end
end
