package hello;

import java.util.concurrent.atomic.AtomicLong;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import org.springframework.beans.factory.annotation.Autowired;

@RestController
public class HelloController {
    
    private static final Logger log = LoggerFactory.getLogger(Application.class);
    @Autowired
	private RestTemplate restTemplate;

    @RequestMapping("/hello5")
    public Value hello5(@RequestParam(value="cal", defaultValue="50") String cal) {

        double cal2 = Math.abs(Double.valueOf(cal)+3)/1.03; 
        log.info(String.valueOf(cal2));
        
    	Value value = restTemplate.getForObject(
				"http://rest-service-4:16004/hello4?cal="+cal2, Value.class);
		
        log.info(value.toString());
		return value;
    }
    
    
    @RequestMapping("/monitor")
    public String monitor(@RequestParam(value="cal", defaultValue="50") String cal) {

        double cal2 = Math.abs(Double.valueOf(cal)+3)/1.03; 
        log.info(String.valueOf(cal2));
        
		return String.valueOf(cal2);
    }
}
