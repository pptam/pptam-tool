package hello;

import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;

import org.hibernate.SessionFactory;
import org.hibernate.boot.MetadataSources;
import org.hibernate.boot.registry.StandardServiceRegistry;
import org.hibernate.boot.registry.StandardServiceRegistryBuilder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.web.client.RestTemplate;

import org.springframework.context.annotation.EnableAspectJAutoProxy;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.integration.annotation.IntegrationComponentScan;

@SpringBootApplication

@EnableAspectJAutoProxy(proxyTargetClass = true)
@EnableAsync
@IntegrationComponentScan
public class Application {

	private static final Logger log = LoggerFactory.getLogger(Application.class);

	// private SessionFactory sessionFactory = null;

	public static void main(String args[]) {
		SpringApplication.run(Application.class);
	}

	@Bean
	public RestTemplate restTemplate(RestTemplateBuilder builder) {
		return builder.build();
	}

	// @Bean
	// public SessionFactory sessionFactory() {
	// // A SessionFactory is set up once for an application!
	// final StandardServiceRegistry registry = new
	// StandardServiceRegistryBuilder()
	// .configure() // configures settings from hibernate.cfg.xml
	// .build();
	// try {
	// sessionFactory = new MetadataSources( registry
	// ).buildMetadata().buildSessionFactory();
	// }
	// catch (Exception e) {
	// // The registry would be destroyed by the SessionFactory, but we had
	// trouble building the SessionFactory
	// // so destroy it manually.
	// StandardServiceRegistryBuilder.destroy( registry );
	// }
	// return sessionFactory;
	// }

	@Bean
	public EntityManagerFactory entityManagerFactory() {
		return Persistence.createEntityManagerFactory("org.hibernate.tutorial.jpa");
	}
}