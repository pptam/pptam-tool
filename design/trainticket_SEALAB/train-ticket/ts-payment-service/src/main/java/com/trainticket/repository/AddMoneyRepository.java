package com.trainticket.repository;

import com.trainticket.domain.AddMoney;
import com.trainticket.domain.Payment;
import org.springframework.data.repository.CrudRepository;


public interface AddMoneyRepository extends CrudRepository<AddMoney,String> {
}
