package com.trainticket.verificationcode.repository;

import com.trainticket.verificationcode.domain.VerificationCodeValue;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;

@Repository
public interface VerificationCodeRepository extends MongoRepository<VerificationCodeValue, String> {

    @Query("{ 'cookie': ?0 }")
    VerificationCodeValue findByCookie(String cookie);

    @Query("{ 'verificationCode': ?0 }")
    VerificationCodeValue findByVerificationCode(String verificationCode);

    ArrayList<VerificationCodeValue> findAll();

}
