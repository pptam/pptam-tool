require 'fenxi'
require 'test/unit'
class TestMergeUtil < Test::Unit::TestCase

  def test_001_longest_match
    assert_equal(1, Fenxi::MergeUtil.longest_match("a", "aa"))
    assert_equal(100, Fenxi::MergeUtil.longest_match("vmstat", "vmstat"))
    assert_equal(8, Fenxi::MergeUtil.longest_match("mpstat.1a.out", "mpstat.1b"))
    assert_equal(6, Fenxi::MergeUtil.longest_match("mpstat.1a.out", "mpstat_a.1b"))
    assert_equal(-1, Fenxi::MergeUtil.longest_match(nil, "foobar"))
    assert_equal(-1, Fenxi::MergeUtil.longest_match(nil, nil))
  end
  def test_002_find_matching_tool#(tool, list)
    tool = "mpstat.1a.out"
    list=["mpstat_a", "mpstat.2a.out"]
    assert_equal("mpstat.2a.out", Fenxi::MergeUtil.find_matching_tool(tool, list))
    tool="mpstat.1a.out"
    list=["mpstat.1b","mpstat_a.1b"]
    assert_equal("mpstat.1b", Fenxi::MergeUtil.find_matching_tool(tool, list))
    tool="a"
    list=["a", "aa"]
    assert_equal("a", Fenxi::MergeUtil.find_matching_tool(tool, list))
    tool="statit"
    list=["sysbench", "status", "sysbench"]
    assert_nil(Fenxi::MergeUtil.find_matching_tool(tool, list))
  end
  def test_003_find_comparable_tools
    tools=[["vmstat_a", "mpstat_a"],["vmstat_b", "mpstat_b"]]
    expected={"vmstat_a"=>["vmstat_b"], "mpstat_a"=>["mpstat_b"]}
    assert_equal(expected, Fenxi::MergeUtil.find_comparable_tools(tools))
    assert_equal({}, Fenxi::MergeUtil.find_comparable_tools([[]]))
    tools=[["vmstat_a", "mpstat_a", "foobar"],["vmstat_b", "mpstat_b"]]
    assert_equal(expected, Fenxi::MergeUtil.find_comparable_tools(tools))
    tools=[["mpstat_a", "vmstat_a", "foobar"],["vmstat_b", "mpstat_b"]]
    assert_equal(expected, Fenxi::MergeUtil.find_comparable_tools(tools))
    tools=[["sbench.xan.rw10.1A"],["sbench.xan.rw10.1B"]]
    expected = {"sbench.xan.rw10.1A" => ["sbench.xan.rw10.1B"]}
    assert_equal(expected, Fenxi::MergeUtil.find_comparable_tools(tools))
    tools=[["mpstat.1a.out", "mpstat_a.1a.out"],["mpstat.1b","mpstat_a.1b"]]
    expected = {"mpstat.1a.out" => ["mpstat.1b"],
      "mpstat_a.1a.out" => ["mpstat_a.1b"]}
    assert_equal(expected, Fenxi::MergeUtil.find_comparable_tools(tools))
    tools=[["a", "b"], ["c", "d"]] #No match
    assert_equal({}, Fenxi::MergeUtil.find_comparable_tools(tools))
  end
end

