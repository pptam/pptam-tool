package hello;

import java.util.concurrent.Future;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.AsyncResult;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class RestbackService {

    private static final Logger log = LoggerFactory.getLogger(RestbackService.class);

    @Autowired
	private RestTemplate restTemplate;

    @Async
    public Future<Boolean> callbackResult(double cal2) throws InterruptedException {
        log.info("call back: " + cal2);
        Boolean result = restTemplate.getForObject("http://rest-service-6:16006/hello6_1?cal2="+cal2, Boolean.class);
        // Artificial delay of 1s for demonstration purposes
        Thread.sleep(1000L);
        log.info("-----------call back complete-------------");
        return new AsyncResult<>(result);
    }

}
