package order.init;

import order.domain.Order;
import order.service.OrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.util.Date;
import java.util.UUID;


@Component
public class InitData implements CommandLineRunner {
    @Autowired
    OrderService service;

    public void run(String... args)throws Exception{
        Order order = new Order();
        order.setId(UUID.fromString("5ad7750b-a68b-49c0-a8c0-32776b067703"));
        order.setBoughtDate(new Date());
        order.setTravelDate(new Date("Sat Jul 29 00:00:00 GMT+0800 2017"));
        order.setTravelTime(new Date("Mon May 04 09:02:00 GMT+0800 2013"));
        order.setAccountId(UUID.fromString("4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f"));
        order.setContactsName("Contacts_One");
        order.setDocumentType(1);
        order.setContactsDocumentNumber("DocumentNumber_One");
        order.setTrainNumber("G1237");
        order.setCoachNumber(5);
        order.setSeatClass(2);
        order.setSeatNumber("FirstClass-30");
        order.setFrom("nanjing");
        order.setTo("shanghaihongqiao");
        order.setStatus(0);
        order.setPrice("100.0");
        service.initOrder(order, null);


        Order orderTwo = new Order();
        orderTwo.setId(UUID.fromString("8177ac5a-61ac-42f4-83f4-bd7b394d0531"));
        orderTwo.setBoughtDate(new Date());
        orderTwo.setTravelDate(new Date("Sat Jul 29 00:00:00 GMT+0800 2017"));
        orderTwo.setTravelTime(new Date("Mon May 04 09:01:00 GMT+0800 2013"));
        orderTwo.setAccountId(UUID.fromString("4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f"));
        orderTwo.setContactsName("Contacts_One");
        orderTwo.setDocumentType(1);
        orderTwo.setContactsDocumentNumber("DocumentNumber_One");
        orderTwo.setTrainNumber("G1234");
        orderTwo.setCoachNumber(5);
        orderTwo.setSeatClass(2);
        orderTwo.setSeatNumber("FirstClass-30");
        orderTwo.setFrom("shanghai");
        orderTwo.setTo("beijing");
        orderTwo.setStatus(0);
        orderTwo.setPrice("100.0");
        service.initOrder(orderTwo, null);

        Order orderThree = new Order();
        orderThree.setId(UUID.fromString("d3c91694-d5b8-424c-9974-e14c89226e49"));
        orderThree.setBoughtDate(new Date());
        orderThree.setTravelDate(new Date("Sat Jul 29 00:00:00 GMT+0800 2017"));
        orderThree.setTravelTime(new Date("Mon May 04 09:00:00 GMT+0800 2013"));
        orderThree.setAccountId(UUID.fromString("4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f"));
        orderThree.setContactsName("Contacts_One");
        orderThree.setDocumentType(1);
        orderThree.setContactsDocumentNumber("DocumentNumber_One");
        orderThree.setTrainNumber("G1235");
        orderThree.setCoachNumber(5);
        orderThree.setSeatClass(2);
        orderThree.setSeatNumber("FirstClass-30");
        orderThree.setFrom("shanghai");
        orderThree.setTo("beijing");
        orderThree.setStatus(0);
        orderThree.setPrice("100.0");
        service.initOrder(orderThree, null);
    }

}
//<td class="all_order_id noshow_component">a1674800-1cbb-49e5-ac1a-f193bde8a728</td>
//Order{"id":"5ad7750b-a68b-49c0-a8c0-32776b067703",
// "boughtDate":"Jun 21, 2017 11:52:22 AM",
// "travelDate":"Jun 23, 2017 12:00:00 AM",
// "travelTime":"May 4, 2013 2:51:52 PM",
// "accountId":"4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f",
// "contactsName":"Contacts_One",
// "documentType":1,
// "contactsDocumentNumber":"DocumentNumber_One",
// "trainNumber":"Z1234",
// "coachNumber":5,
// "seatClass":2,
// "seatNumber":"FirstClass-30",
// "from":"Shang Hai",
// "to":"Tai Yuan",
// "status":0,
// "price":100.0}
