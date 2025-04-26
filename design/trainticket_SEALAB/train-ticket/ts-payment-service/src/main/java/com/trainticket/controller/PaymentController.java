package com.trainticket.controller;

import com.trainticket.domain.AddMoneyInfo;
import com.trainticket.domain.Payment;
import com.trainticket.domain.PaymentInfo;
import com.trainticket.service.PaymentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.*;

import java.util.*;

/**
 * Created by Chenjie Xu on 2017/4/7.
 */
@RestController
public class PaymentController {

    @Autowired
    PaymentService service;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home() {
        return "Welcome to [ Payment Service ] !";
    }

    @RequestMapping(path="/payment/pay",method= RequestMethod.POST)
    public boolean pay(@RequestBody PaymentInfo info, @RequestHeader HttpHeaders headers){
        return service.pay(info, headers);
    }

    @RequestMapping(path="/payment/addMoney",method= RequestMethod.POST)
    public boolean addMoney(@RequestBody AddMoneyInfo info, @RequestHeader HttpHeaders headers){
        return service.addMoney(info, headers);
    }

    @RequestMapping(path="/payment/query",method= RequestMethod.GET)
    public List<Payment> query(@RequestHeader HttpHeaders headers){
        return service.query(headers);
    }
}
