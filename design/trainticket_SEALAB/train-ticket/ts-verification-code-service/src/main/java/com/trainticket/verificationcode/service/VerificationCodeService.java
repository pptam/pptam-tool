package com.trainticket.verificationcode.service;

import org.springframework.http.HttpHeaders;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.OutputStream;
import java.util.Map;

public interface VerificationCodeService {
	Map<String, Object> getImageCode(int width, int height, OutputStream os, HttpServletRequest request, HttpServletResponse response,HttpHeaders headers);
	boolean verifyCode(HttpServletRequest request, HttpServletResponse response, String receivedCode,HttpHeaders headers);
}
