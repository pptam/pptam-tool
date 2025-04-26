package hello;

import java.util.concurrent.ExecutionException;
import java.util.concurrent.atomic.AtomicLong;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.AsyncRestTemplate;
import org.springframework.web.client.RestTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.util.concurrent.ListenableFuture;
import org.springframework.web.bind.annotation.*;

@RestController
public class HelloController {

	private static final Logger log = LoggerFactory.getLogger(Application.class);
	@Autowired
	private RestTemplate restTemplate;

	@Autowired
	private AsyncRestTemplate asyncRestTemplate;

	@RequestMapping(value = "api/v1/spans", method ={RequestMethod.POST,RequestMethod.GET})
	public String handle_collect(@RequestBody String info) {
		System.out.println("==========post============");
		System.out.println(info);
		return "---------post------------";
		
	}


	@RequestMapping(value = {"api/**", "**/spans"}, method ={RequestMethod.POST,RequestMethod.GET})
	public String handle_collect_2(@RequestBody String info) {
		System.out.println("==========post span any============");
		System.out.println(info);
		return "---------post span any------------";
		
	}



	@RequestMapping(value = "**", method ={RequestMethod.POST,RequestMethod.GET})
	public String handle_collect_any(@RequestBody String info) {
		System.out.println("==========post any============");
		System.out.println(info);
		return "---------post any------------";
		
	}
}
