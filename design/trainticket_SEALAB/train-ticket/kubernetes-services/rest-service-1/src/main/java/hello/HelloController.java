package hello;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import org.springframework.beans.factory.annotation.Autowired;

@RestController
public class HelloController {

	@Autowired
	private RestTemplate restTemplate;


	@RequestMapping(value="/hello", method = RequestMethod.GET)
	public String hello() {
		String str2 = restTemplate.getForObject("http://rest-service-2:16002/hello",String.class);
		return str2 + " | Hello From Rest-Service-1";
	}
}
