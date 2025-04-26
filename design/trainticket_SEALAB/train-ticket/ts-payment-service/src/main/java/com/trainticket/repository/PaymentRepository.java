package com.trainticket.repository;


import com.trainticket.domain.Payment;
import org.springframework.data.repository.CrudRepository;

import java.util.List;


public interface PaymentRepository extends CrudRepository<Payment,String> {

    Payment findById(String id);

    Payment findByOrderId(String orderId);

    List<Payment> findAll();

    List<Payment> findByUserId(String userId);
}
