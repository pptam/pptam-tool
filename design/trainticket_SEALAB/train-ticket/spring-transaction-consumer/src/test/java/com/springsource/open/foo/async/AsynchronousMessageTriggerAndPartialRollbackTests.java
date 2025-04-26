

package com.springsource.open.foo.async;

import static org.junit.Assert.assertEquals;

import java.util.List;

import org.junit.Test;
import org.springframework.test.jdbc.JdbcTestUtils;

public class AsynchronousMessageTriggerAndPartialRollbackTests extends AbstractAsynchronousMessageTriggerTests {

	@Test
	public void testPartialFailureWithDuplicateMessage() {
		jmsTemplate.convertAndSend("async", "foo");
		jmsTemplate.convertAndSend("async", "bar.fail.partial");
	}

	@Override
	protected void checkPostConditions() {

		// Both committed
		assertEquals(2, JdbcTestUtils.countRowsInTable(jdbcTemplate, "T_FOOS"));
		List<String> list = getMessages();
		// One message rolled back and returned to queue
		assertEquals(1, list.size());

	}

}
