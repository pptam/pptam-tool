package com.lightbend.akka.sample;

import akka.actor.ActorRef;
import akka.actor.ActorSystem;
import com.lightbend.akka.sample.Greeter.*;
import com.lightbend.akka.sample.Printer.Greeting;
import com.lightbend.akka.sample.Printer.Greeting2;
import akka.routing.Broadcast;
import akka.routing.RoundRobinPool;

import java.io.IOException;

public class AkkaQuickstart {
  public static void main(String[] args) {
    final ActorSystem system = ActorSystem.create("helloakka");
    try {
      //#create-actors
//      final ActorRef printerActor = 
//        system.actorOf(Printer.props().withRouter(RoundRobinPool(6)), "printerActor");
      final ActorRef printerActor = 
        system.actorOf(Printer.props(), "printerActor");
      final ActorRef howdyGreeter = 
        system.actorOf(Greeter.props("Howdy", printerActor), "howdyGreeter");
      final ActorRef helloGreeter = 
        system.actorOf(Greeter.props("Hello", printerActor), "helloGreeter");
      final ActorRef goodDayGreeter = 
        system.actorOf(Greeter.props("Good day", printerActor), "goodDayGreeter");
      //#create-actors

      //#main-send-messages
      howdyGreeter.tell(new WhoToGreet("Akka"), ActorRef.noSender());
      howdyGreeter.tell(new Greet(), ActorRef.noSender());

      howdyGreeter.tell(new WhoToGreet("Lightbend"), ActorRef.noSender());
      howdyGreeter.tell(new Greet(), ActorRef.noSender());

      helloGreeter.tell(new WhoToGreet("Java"), ActorRef.noSender());
      helloGreeter.tell(new Greet(), ActorRef.noSender());

      goodDayGreeter.tell(new WhoToGreet("Play"), ActorRef.noSender());
      goodDayGreeter.tell(new Greet(), ActorRef.noSender());
      
      printerActor.tell(new Greeting("111111"), ActorRef.noSender());
      printerActor.tell(new Greeting("222222"), ActorRef.noSender());
      printerActor.tell(new Greeting("333333"), ActorRef.noSender());
      printerActor.tell(new Greeting2("444444"), ActorRef.noSender());
      printerActor.tell(new Greeting2("555555"), ActorRef.noSender());
      printerActor.tell(new Greeting2("666666"), ActorRef.noSender());
      //#main-send-messages

      System.out.println(">>> Press ENTER to exit <<<");
      System.in.read();
    } catch (IOException ioe) {
    } finally {
      system.terminate();
    }
  }
}
