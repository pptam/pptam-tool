

package com.springsource.open.foo.async;

import static org.junit.Assert.assertEquals;

import java.util.List;

import org.junit.Test;
import org.springframework.test.jdbc.JdbcTestUtils;

public class AsynchronousMessageTriggerSunnyDayTests extends AbstractAsynchronousMessageTriggerTests {

	@Test
	public void testCleanData() {
		jmsTemplate.convertAndSend("async", "foo");
		jmsTemplate.convertAndSend("async", "bar");
	}

	@Override
	protected void checkPostConditions() {

		// Two messages committed
		assertEquals(2, JdbcTestUtils.countRowsInTable(jdbcTemplate,
				"T_FOOS"));
		List<String> list = getMessages();
		// No messages rolled back so queue was empty
		assertEquals(0, list.size());

	}

}
