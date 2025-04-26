

package com.springsource.open.foo.sync;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import javax.sql.DataSource;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.context.transaction.AfterTransaction;
import org.springframework.test.context.transaction.BeforeTransaction;
import org.springframework.test.jdbc.JdbcTestUtils;
import org.springframework.transaction.annotation.Transactional;

@RunWith(SpringRunner.class)
@SpringBootTest
public class SynchronousMessageTriggerAndRollbackTests {

	@Autowired
	private RabbitTemplate jmsTemplate;

	private JdbcTemplate jdbcTemplate;

	@Autowired
	public void setDataSource(@Qualifier("dataSource") DataSource dataSource) {
		this.jdbcTemplate = new JdbcTemplate(dataSource);
	}

	@BeforeTransaction
	public void clearData() {
		getMessages(); // drain queue
		jmsTemplate.convertAndSend("queue", "foo");
		jmsTemplate.convertAndSend("queue", "bar");
		jdbcTemplate.update("delete from T_FOOS");
	}

	@AfterTransaction
	public void checkPostConditions() {

		assertEquals(0, JdbcTestUtils.countRowsInTable(jdbcTemplate, "T_FOOS"));
		List<String> list = getMessages();
		assertEquals(2, list.size());

	}

	@Test
	@Transactional
	public void testReceiveMessageUpdateDatabase() throws Exception {

		List<String> list = getMessages();
		assertEquals(2, list.size());
		assertTrue(list.contains("foo"));

		int id = 0;
		for (String name : list) {			
			jdbcTemplate.update("INSERT INTO T_FOOS (id,name,foo_date) values (?,?,?)", id++, name, new Date());
		}

		assertEquals(2, JdbcTestUtils.countRowsInTable(jdbcTemplate, "T_FOOS"));

	}

	private List<String> getMessages() {
		String next = "";
		List<String> msgs = new ArrayList<String>();
		while (next != null) {
			next = (String) jmsTemplate.receiveAndConvert("queue");
			if (next != null)
				msgs.add(next);
		}
		return msgs;
	}
}
