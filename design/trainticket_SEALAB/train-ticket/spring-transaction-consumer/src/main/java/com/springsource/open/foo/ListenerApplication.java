

package com.springsource.open.foo;

import org.springframework.amqp.core.Queue;
import org.springframework.amqp.rabbit.config.SimpleRabbitListenerContainerFactory;
import org.springframework.amqp.rabbit.connection.ConnectionFactory;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.BeansException;
import org.springframework.beans.factory.config.BeanPostProcessor;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.transaction.PlatformTransactionManager;

@SpringBootApplication
public class ListenerApplication {
	
	@Bean
	public Queue sync() {
		return new Queue("queue");
	}

	@Bean
	public Queue async() {
		return new Queue("async");
	}

	@Bean
	public RabbitTemplate jmsTemplate(ConnectionFactory connectionFactory) {
		RabbitTemplate jmsTemplate = new RabbitTemplate(connectionFactory);
		jmsTemplate.setReceiveTimeout(200);
		jmsTemplate.setChannelTransacted(true);
		return jmsTemplate;
	}

	@Bean
	public BeanPostProcessor connectionFactoryPostProcessor(
			PlatformTransactionManager transactionManager) {
		return new BeanPostProcessor() {

			@Override
			public Object postProcessBeforeInitialization(Object bean, String beanName)
					throws BeansException {
				return bean;
			}

			@Override
			public Object postProcessAfterInitialization(Object bean, String beanName)
					throws BeansException {
				if (bean instanceof SimpleRabbitListenerContainerFactory) {
					((SimpleRabbitListenerContainerFactory) bean)
							.setTransactionManager(transactionManager);
				}
				return bean;
			}
		};
	}

	public static void main(String[] args) throws Exception {
		SpringApplication.run(ListenerApplication.class, args);
	}

}
