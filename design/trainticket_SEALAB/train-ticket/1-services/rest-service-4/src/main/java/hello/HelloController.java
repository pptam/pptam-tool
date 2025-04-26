package hello;

import java.util.Date;
import java.util.List;
import java.util.concurrent.atomic.AtomicLong;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;

import org.hibernate.Session;
import org.hibernate.SessionFactory;
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

	// @Autowired
	// private SessionFactory sessionFactory;

	@Autowired
	private EntityManagerFactory entityManagerFactory;

	@RequestMapping("/hello4")
	public Value hello4(@RequestParam(value = "cal", defaultValue = "50") String cal) {

		double cal2 = (Double.valueOf(cal) + 10) / 1.1;
		log.info(String.valueOf(cal2));

		Value value = restTemplate.getForObject("http://rest-service-3:16003/hello3?cal=" + cal2, Value.class);
		log.info(value.toString());
		return value;
	}

	// @RequestMapping("/getdata")
	// public String getdata(@RequestParam(value = "cal", defaultValue = "50")
	// String cal) {
	//
	// log.info("----------------");
	//
	// Session session = sessionFactory.openSession();
	// session.beginTransaction();
	// session.save(new Event("Our very first event!", new Date()));
	// session.save(new Event("A follow up event", new Date()));
	// session.getTransaction().commit();
	// session.close();
	//
	// // now lets pull events from the database and list them
	// session = sessionFactory.openSession();
	// session.beginTransaction();
	// List result = session.createQuery("from Event").list();
	// for (Event event : (List<Event>) result) {
	// System.out.println("Event (" + event.getDate() + ") : " +
	// event.getTitle());
	// }
	// session.getTransaction().commit();
	// session.close();
	//
	// return result.toString();
	// }

	@RequestMapping("/getdata1")
	public String getdata1(@RequestParam(value = "cal", defaultValue = "50") String cal) {

		log.info("----------------");

		EntityManager entityManager = entityManagerFactory.createEntityManager();
		entityManager.getTransaction().begin();
		entityManager.persist(new Event("Our very first event!", new Date()));
		entityManager.persist(new Event("A follow up event", new Date()));
		entityManager.getTransaction().commit();
		entityManager.close();

		// now lets pull events from the database and list them
		entityManager = entityManagerFactory.createEntityManager();
		entityManager.getTransaction().begin();
		List<Event> result = entityManager.createQuery("from Event", Event.class).getResultList();
		for (Event event : result) {
			System.out.println("Event (" + event.getDate() + ") : " + event.getTitle());
		}
		entityManager.getTransaction().commit();
		entityManager.close();

		return result.toString();
	}
}
