

package com.springsource.open.foo.test;

import static org.junit.Assert.assertEquals;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.transaction.annotation.Transactional;

@RunWith(SpringRunner.class)
@SpringBootTest
public class DatasourceTests {

	@Autowired
	private JdbcTemplate simpleJdbcTemplate;

	@Transactional @Test
	public void testTemplate() throws Exception {
		simpleJdbcTemplate.execute("delete from T_FOOS");
		int count = simpleJdbcTemplate.queryForObject("select count(*) from T_FOOS", Integer.class);
		assertEquals(0, count);

		simpleJdbcTemplate.update("INSERT into T_FOOS (id,name,foo_date) values (?,?,null)", 0, "foo");
	}
}
