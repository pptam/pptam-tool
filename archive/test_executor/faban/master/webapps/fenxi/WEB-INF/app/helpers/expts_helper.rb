module ExptsHelper
  def section_type(section)
    if section.exception then
      "exception"
    elsif section.class.to_s == "Fenxi::ChartSection"
      "chart"
    else
      "table"
    end
  end
  def supported_display_types
    options = [["Table", "table"]]
    Fenxi::Chart.supported_chart_types.each do |e|
      options << [e, e.downcase]
    end
    options
  end
  def pretty_tool_list(expt)
    Fenxi::FenxiUtil.pretty_tool_list(expt.tools.keys)
    #{ host => [[realname, prettyname],..] }
  end  
end
