package hello;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

@RestController
public class HelloController {

	@Autowired
	private RestTemplate restTemplate;


	@RequestMapping(value="/hello", method = RequestMethod.GET)
	public String hello() {
		String str3 = restTemplate.getForObject("http://rest-service-1:16001/hello",String.class);
		return str3 + " | Hello From Rest-Service-3";
	}
}
