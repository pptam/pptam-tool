package queue.async;

import java.util.concurrent.atomic.AtomicInteger;

import org.springframework.amqp.rabbit.connection.CachingConnectionFactory;
import org.springframework.amqp.rabbit.connection.ConnectionFactory;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.config.BeanPostProcessor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.scheduling.annotation.ScheduledAnnotationBeanPostProcessor;

@Configuration
public class ProducerConfiguration {

	protected final String helloWorldQueueName = "hello.world.queue";

	@Bean
	public RabbitTemplate rabbitTemplate() {
		RabbitTemplate template = new RabbitTemplate(connectionFactory());
		template.setRoutingKey(this.helloWorldQueueName);
		return template;
	}

	@Bean
	public ConnectionFactory connectionFactory() {
		CachingConnectionFactory connectionFactory = new CachingConnectionFactory("localhost");
		connectionFactory.setUsername("guest");
		connectionFactory.setPassword("guest");
		return connectionFactory;
	}

	@Bean
	public ScheduledProducer scheduledProducer() {
		return new ScheduledProducer();
	}

	@Bean
	public BeanPostProcessor postProcessor() {
		return new ScheduledAnnotationBeanPostProcessor();
	}


	static class ScheduledProducer {

		@Autowired
		private volatile RabbitTemplate rabbitTemplate;

		private final AtomicInteger counter = new AtomicInteger();

		@Scheduled(fixedRate = 3000)
		public void sendMessage() {
			rabbitTemplate.convertAndSend("Hello World " + counter.incrementAndGet());
		}
	}

}
