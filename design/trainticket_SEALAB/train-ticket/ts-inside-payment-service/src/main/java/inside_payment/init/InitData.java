package inside_payment.init;

import inside_payment.domain.*;
import inside_payment.repository.AddMoneyRepository;
import inside_payment.repository.PaymentRepository;
import inside_payment.service.InsidePaymentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;


@Component
public class InitData implements CommandLineRunner {
    @Autowired
    InsidePaymentService service;

    @Autowired
    PaymentRepository paymentRepository;

    @Autowired
    AddMoneyRepository addMoneyRepository;

    @Override
    public void run(String... args) throws Exception{
        CreateAccountInfo info1 = new CreateAccountInfo();
        info1.setUserId("4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f");
        info1.setMoney("10000");
        service.createAccount(info1,null);

//        PaymentInfo info2 = new PaymentInfo();
//        info2.setOrderId("5ad7750b-a68b-49c0-a8c0-32776b067703");
//        info2.setTripId("G1234");
//        info2.setUserId("4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f");
//        service.pay(info2);
        Payment payment = new Payment();
        payment.setId("5ad7750ba68b49c0a8c035276b321701");
        payment.setOrderId("5ad7750b-a68b-49c0-a8c0-32776b067702");
        payment.setPrice("100.0");
        payment.setUserId("4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f");
        payment.setType(PaymentType.P);
        service.initPayment(payment,null);
    }
}

