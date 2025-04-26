package com.lightbend.akka.sample;

import akka.actor.AbstractActor;
import akka.actor.ActorRef;
import akka.actor.Props;
import akka.event.Logging;
import akka.event.LoggingAdapter;

//#printer-messages
public class Printer extends AbstractActor {
//#printer-messages
  static public Props props() {
    return Props.create(Printer.class, () -> new Printer());
  }

  //#printer-messages
  static public class Greeting {
    public final String message;

    public Greeting(String message) {
      this.message = message;
    }
  }
  //#printer-messages
  static public class Greeting2 {
	    public final String message;

	    public Greeting2(String message) {
	      this.message = message;
	    }
	  }

  private LoggingAdapter log = Logging.getLogger(getContext().getSystem(), this);

  public Printer() {
  }

  @Override
  public Receive createReceive() {
    return receiveBuilder()
        .match(Greeting.class, greeting -> {
        	Thread.sleep(1000);
            log.info(greeting.message);
        })
        .match(Greeting2.class, greeting -> {
        	Thread.sleep(1000);
            log.info(greeting.message);
        })
        .build();
  }
//#printer-messages
}
//#printer-messages
