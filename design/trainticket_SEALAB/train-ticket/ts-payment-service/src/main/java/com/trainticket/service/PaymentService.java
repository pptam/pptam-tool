package com.trainticket.service;

import com.trainticket.domain.AddMoneyInfo;
import com.trainticket.domain.Payment;
import com.trainticket.domain.PaymentInfo;
import org.springframework.http.HttpHeaders;

import java.util.List;

/**
 * Created by Chenjie Xu on 2017/4/5.
 */
public interface PaymentService {

    boolean pay(PaymentInfo info, HttpHeaders headers);

    boolean addMoney(AddMoneyInfo info, HttpHeaders headers);

    List<Payment> query(HttpHeaders headers);

    void initPayment(Payment payment,HttpHeaders headers);

}
