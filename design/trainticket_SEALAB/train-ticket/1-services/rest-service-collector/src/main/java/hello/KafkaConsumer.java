package hello;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
public class KafkaConsumer {
	
	private static final Logger log = LoggerFactory.getLogger(Application.class);

    /**
     * reader
     */
    @KafkaListener(topics = {"app_log"})
    public void consumer(String message){
        log.info("test topic message : {}", message);
    }
}
