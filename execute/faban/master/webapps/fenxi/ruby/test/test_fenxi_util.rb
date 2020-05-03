require 'test/unit'
require 'fenxi/fenxi_util'

class TestFenxiUtil < Test::Unit::TestCase
  def test_001_parse_tool_name
    h = { "statspack_schlitz1_1y" => [nil, "statspack_schlitz1_1y"],
      "sbench.xan.rw10" => ["rw10", "sbench"],
      "sbench.xan.rw10.3" => [nil, "sbench.rw10.3"],
      "test.xan" => [nil, "test"],
      "test.xan.1y" => [nil, "test.1y"],
      "mpstat.out.bursar" => ["bursar", "mpstat"],
      "mpstat.out.log.bursar" => ["bursar", "mpstat"],
      "statit.ballfire.12w" => [nil, "statit.ballfire.12w"],
      "1y.detail.xan" => [nil, "1y.detail"],
      "vmstat.1y.out" => [nil, "vmstat.1y"]
    }
    h.each do |key, value|
      assert_equal(value, Fenxi::FenxiUtil.parse_tool_name(key))
    end
    assert_equal([nil,""], Fenxi::FenxiUtil.parse_tool_name(""))
    assert_nil(Fenxi::FenxiUtil.parse_tool_name(nil))
  end

  def test_002_pretty_tool_list
    t = %W|vmstat.out.host1 mpstat.out.host1 vmstat.out.host2 mpstat.out.host2 test.xan|
    expected = {"nil" => [["test.xan", "test"]],
      "host1" => [["vmstat.out.host1", "vmstat"], ["mpstat.out.host1", "mpstat"]],
      "host2" => [["vmstat.out.host2", "vmstat"], ["mpstat.out.host2", "mpstat"]],
    }
    assert_equal(expected, Fenxi::FenxiUtil.pretty_tool_list(t))
    assert_equal({}, Fenxi::FenxiUtil.pretty_tool_list([]))
  end
end
