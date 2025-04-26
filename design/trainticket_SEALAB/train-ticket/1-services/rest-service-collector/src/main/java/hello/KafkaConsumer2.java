package hello;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class KafkaConsumer2 {
	
	private static final Logger log = LoggerFactory.getLogger(Application.class);

	@Scheduled(fixedRate = 1000 * 60)
	public void testKafka() throws Exception {
		//TODO pure kafka consume timely
	}
}
