require 'fenxi'
require 'test/unit'
class TestQueryResult < Test::Unit::TestCase
  def setup
    types = ["string", "int", "int"]
    headers = ["name", "value1", "value2"]
    row1=[["first row", 1, 1], ["second row", 2, 2]]
    row2=[["first row", 10, 10], ["second row", 20, 20], ["add", 1, 2]]
    @qr1 = Fenxi::QueryResult.new(types, headers, row1)
    @qr2 = Fenxi::QueryResult.new(types, headers, row2)
  end
  def teardown

  end

  def test_find_join_keys
    assert_equal([], Fenxi::QueryResult.find_join_keys([]))
    val = ["first row", "second row", "add"]
    assert_equal(val, Fenxi::QueryResult.find_join_keys([@qr1, @qr2]))
    val = ["first row", "second row"]
    assert_equal(val, Fenxi::QueryResult.find_join_keys([@qr1]))
    assert_equal(val, Fenxi::QueryResult.find_join_keys([nil, @qr1]))
  end

  def test_join_rows
    val = [["first row", 1, 10, 1, 10], ["second row", 2, 20, 2, 20], ["add", "-", 1, "-", 2]]
    assert_equal(val, Fenxi::QueryResult.join_rows([@qr1, @qr2]))
    val = [["first row", 1, "-", 1, "-"], ["second row", 2, "-", 2, "-"]]
    val = [["first row", "-", 1, "-", 1], ["second row", "-", 2, "-", 2]]
    assert_equal(val, Fenxi::QueryResult.join_rows([nil, @qr1]))
  end

  def test_join_headers
    val = ["name", "value1", "value1", "value2", "value2"]
    assert_equal(val, Fenxi::QueryResult.join_headers([@qr1, @qr2]))
    assert_equal(val, Fenxi::QueryResult.join_headers([@qr2, @qr1]))
    val = ["name", "value1", "NULL", "value2", "NULL"]
    assert_equal(val, Fenxi::QueryResult.join_headers([@qr1, nil]))
    val = ["name", "NULL", "value1", "NULL", "value2"]
    assert_equal(val, Fenxi::QueryResult.join_headers([nil, @qr2]))
  end

  def test_join_types
    val = ["string", "int", "int", "int", "int"]
    assert_equal(val, Fenxi::QueryResult.join_types([@qr1, @qr2]))
    assert_equal(val, Fenxi::QueryResult.join_types([@qr2, @qr1]))
    val = ["string", "int", "int", "int", "int"]
    assert_equal(val, Fenxi::QueryResult.join_types([@qr1, nil]))
    val = ["string", "int", "int", "int", "int"]
    assert_equal(val, Fenxi::QueryResult.join_types([nil, @qr2]))
  end

  def test_merge
    
  end

  def test_update_headers
        # Given (["A", "B"], ["Name", "Value1", "Value2"]) returns
    # [Name, "A Value1", "B Value2]
    names = ["A", "B"]
    headers = ["Name", "Value1", "Value2"]
    expected =  ["Name", "A Value1", "B Value2"]
    assert_equal(expected, Fenxi::QueryResult.update_headers(names, headers))
    headers = ["Name", "Value1", "Value2", "Value3", "Value4"]
    expected =  ["Name", "A Value1", "B Value2", "A Value3", "B Value4"]
    assert_equal(expected, Fenxi::QueryResult.update_headers(names, headers))
  end
end

