

package com.springsource.open.foo.async;

import static org.junit.Assert.assertEquals;

import java.util.List;

import org.junit.Test;
import org.springframework.test.jdbc.JdbcTestUtils;

public class AsynchronousMessageTriggerAndRollbackTests  extends AbstractAsynchronousMessageTriggerTests {


	@Test
	public void testBusinessFailure() {
		jmsTemplate.convertAndSend("async", "foo");
		jmsTemplate.convertAndSend("async", "bar.fail");
	}

	@Override
	protected void checkPostConditions() {

		// One failed and rolled back, the other committed
		assertEquals(1, JdbcTestUtils.countRowsInTable(jdbcTemplate, "T_FOOS"));
		List<String> list = getMessages();
		// One message rolled back and returned to queue
		assertEquals(1, list.size());

	}

}
