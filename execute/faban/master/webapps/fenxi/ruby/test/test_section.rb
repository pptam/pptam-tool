require 'fenxi' 
require 'test/unit' 
class TestSection < Test::Unit::TestCase
  def setup
    @s = Fenxi::Section.new(["tablename", "desc", "line", "1", "query"])
    @s1 = Fenxi::Section.new(["tablename", "desc", "line;xaxis=x;yaxis=y", "1", "query"])
  end
  def teardown

  end

  def test_section_init    
    assert_nil(@s.customizations)
    assert_not_nil(@s1.customizations)
    assert_equal("xaxis=x;yaxis=y", @s1.customizations)
    assert_nil(@s.executed?)
  end
  def test_execute_db_nil    
    @s1.execute(nil)
    assert_not_nil(@s1.exception)
    assert(@s1.executed?)
  end
  def test_aggregate_summary_sections
    slist= [
      Fenxi::TableSection.new(["tablename", "desc", "line", "1", "query"]),
      Fenxi::TableSection.new(["tablename", "desc", "line", "1", "query"]),
      Fenxi::ChartSection.new(["tablename", "desc", "line", "1", "query"]),
    ]
    assert_equal([], Fenxi::Section.aggregate_summary_sections([]))
    assert_equal(slist, Fenxi::Section.aggregate_summary_sections(slist))    
  end
end 

