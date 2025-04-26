package com.trainticket.verificationcode.domain;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "verification_code")
@JsonIgnoreProperties(ignoreUnknown = true)
public class VerificationCodeValue {

    @Id
    public String cookie;

    public String verificationCode;

    public VerificationCodeValue(){
        //Default Constructor
    }

    public VerificationCodeValue(String cookie, String verificationCode) {
        this.cookie = cookie;
        this.verificationCode = verificationCode;
    }

    public String getCookie() {
        return cookie;
    }

    public void setCookie(String cookie) {
        this.cookie = cookie;
    }

    public String getVerificationCode() {
        return verificationCode;
    }

    public void setVerificationCode(String verificationCode) {
        this.verificationCode = verificationCode;
    }
}
