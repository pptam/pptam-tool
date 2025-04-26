package com.springsource.open.foo;

import org.aspectj.lang.annotation.AfterReturning;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.amqp.rabbit.core.ChannelCallback;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.stereotype.Component;

import com.rabbitmq.client.Channel;

@Aspect
@Component
public class FailureSimulator {

	private RabbitTemplate jmsTemplate;
	
	@Autowired
	public void setJmsTemplate(RabbitTemplate jmsTemplate) {
		this.jmsTemplate = jmsTemplate;
	}


	public void simulateMessageSystemFailure() {

		// Simulate a message system failure before the main transaction
		// commits...
		jmsTemplate.execute(new ChannelCallback<Object>() {
			public Object doInRabbit(Channel session) throws Exception {
				try {
					session.abort();
				} catch (Exception e) {
					// swallow it
					e.printStackTrace();
				}
				return null;
			}
		});

	}


	public void simulateBusinessProcessingFailure() {
		throw new DataIntegrityViolationException("Simulated failure.");
	}
	
	@AfterReturning("execution(* *..*Handler+.handle(String)) && args(msg)")
	public void maybeFail(String msg) {
		if (msg.contains("fail")) {
			if (msg.contains("partial")) {
				simulateMessageSystemFailure();
			} else {
				simulateBusinessProcessingFailure();
			}
		}		
	}

}
