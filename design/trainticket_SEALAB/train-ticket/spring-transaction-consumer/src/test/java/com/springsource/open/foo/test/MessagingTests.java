

package com.springsource.open.foo.test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

import java.util.ArrayList;
import java.util.List;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
@SpringBootTest
public class MessagingTests {

	@Autowired
	private RabbitTemplate jmsTemplate;

	@Before
	public void onSetUp() throws Exception {
		Thread.sleep(100L);
		getMessages(); // drain queue
		jmsTemplate.convertAndSend("queue", "foo");
		jmsTemplate.convertAndSend("queue", "bar");
	}

	@Test
	public void testMessaging() throws Exception {
		List<String> list = getMessages();
		System.err.println(list);
		assertEquals(2, list.size());
		assertTrue(list.contains("foo"));
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
