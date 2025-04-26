package inside_payment.controller;

import inside_payment.domain.*;
import inside_payment.service.InsidePaymentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.*;
import javax.servlet.http.HttpServletRequest;
import java.util.List;

@RestController
public class InsidePaymentController {

    @Autowired
    public InsidePaymentService service;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home() {
        return "Welcome to [ InsidePayment Service ] !";
    }

    @RequestMapping(value="/inside_payment/pay", method = RequestMethod.POST)
    public boolean pay(@RequestBody PaymentInfo info, HttpServletRequest request, @RequestHeader HttpHeaders headers){
        System.out.println("[Inside Payment Service][Pay] Pay for:" + info.getOrderId());
        return service.pay(info, request, headers);
    }

    @RequestMapping(value="/inside_payment/createAccount", method = RequestMethod.POST)
    public boolean createAccount(@RequestBody CreateAccountInfo info, @RequestHeader HttpHeaders headers){
        return service.createAccount(info, headers);
    }

    @RequestMapping(value="/inside_payment/addMoney", method = RequestMethod.POST)
    public boolean addMoney(@RequestBody AddMoneyInfo info, @RequestHeader HttpHeaders headers){
        return service.addMoney(info, headers);
    }

    @RequestMapping(value="/inside_payment/queryPayment", method = RequestMethod.GET)
    public List<Payment> queryPayment(@RequestHeader HttpHeaders headers){
        return service.queryPayment(headers);
    }

    @RequestMapping(value="/inside_payment/queryAccount", method = RequestMethod.GET)
    public List<Balance> queryAccount(@RequestHeader HttpHeaders headers){
        return service.queryAccount(headers);
    }

    @RequestMapping(value="/inside_payment/drawBack", method = RequestMethod.POST)
    public boolean drawBack(@RequestBody DrawBackInfo info, @RequestHeader HttpHeaders headers){
        return service.drawBack(info, headers);
    }

    @RequestMapping(value="/inside_payment/payDifference", method = RequestMethod.POST)
    public boolean payDifference(@RequestBody PaymentDifferenceInfo info, HttpServletRequest request, @RequestHeader HttpHeaders headers){
        return service.payDifference(info, request, headers);
    }

    @RequestMapping(value="/inside_payment/queryAddMoney", method = RequestMethod.GET)
    public List<AddMoney> queryAddMoney(@RequestHeader HttpHeaders headers){
        return service.queryAddMoney(headers);
    }

    @RequestMapping("/hello1_callback")
    public String hello1_callback(@RequestParam(value="result", defaultValue="satan") String cal_back, @RequestHeader HttpHeaders headers) {

        System.out.println("Call Back Result:" + cal_back);
        System.out.println("-------------external call back-------------");
        return "-------call back end-------";

    }
}
