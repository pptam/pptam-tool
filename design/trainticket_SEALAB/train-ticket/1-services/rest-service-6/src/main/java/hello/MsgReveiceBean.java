

package hello;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.cloud.stream.annotation.EnableBinding;
import org.springframework.cloud.stream.annotation.StreamListener;
import org.springframework.cloud.stream.messaging.Sink;


@EnableBinding(Sink.class)
public class MsgReveiceBean {

	private static Logger logger = LoggerFactory.getLogger(MsgReveiceBean.class);

	@StreamListener(Sink.INPUT)
	public void loggerSink(Object payload) {
		try {
			Thread.sleep(1);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		logger.info("message received: " + payload);
	}

}
