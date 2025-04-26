

package hello;

import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.quartz.QuartzJobBean;

public class SampleJob extends QuartzJobBean {
	
	private static final Logger log = LoggerFactory.getLogger(QuartzJobBean.class);
	
	private String name;

	// Invoked if a Job data map entry with that name
	public void setName(String name) {
		this.name = name;
	}

	@Override
	protected void executeInternal(JobExecutionContext context)
			throws JobExecutionException {
		System.out.println(String.format("Hello %s!", this.name));
		log.info(this.name);
	}

}
