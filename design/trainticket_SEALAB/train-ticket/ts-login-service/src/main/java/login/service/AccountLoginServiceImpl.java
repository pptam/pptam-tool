package login.service;

import login.domain.LoginInfo;
import login.domain.LoginResult;
import login.domain.LogoutInfo;
import login.domain.LogoutResult;
import login.util.CookieUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.UUID;

@Service
public class AccountLoginServiceImpl implements AccountLoginService {

    @Autowired
    private RestTemplate restTemplate;

    //cookie失效时间，秒为单位
    public static final int COOKIE_EXPIRED = 21600;

    @Override
    public LoginResult login(LoginInfo li,String YsbCaptcha, HttpServletResponse response, HttpHeaders headers){
        headers.add("Cookie","YsbCaptcha=" + YsbCaptcha);
        MultiValueMap<String, String> body = new LinkedMultiValueMap<>();
        body.add("verificationCode", li.getVerificationCode());
        HttpEntity requestEntity = new HttpEntity(body,headers);
        ResponseEntity rssResponse = restTemplate.exchange(
                "http://ts-verification-code-service:15678/verification/verify",
                HttpMethod.POST,
                requestEntity,
                String.class
        );
        String verifyResult = (String)rssResponse.getBody();
        System.out.println("[Login Service][Login] Verification Result:" + verifyResult);
        if(!verifyResult.contains("true")){
            LoginResult verifyCodeLr = new LoginResult();
            verifyCodeLr.setAccount(null);
            verifyCodeLr.setToken(null);
            verifyCodeLr.setStatus(false);
            verifyCodeLr.setMessage("Verification Code Wrong.");
            return verifyCodeLr;
        }
//        LoginResult lr = restTemplate.postForObject(
//                "http://ts-sso-service:12349/account/login",
//                li,LoginResult.class);
        requestEntity = new HttpEntity(li,headers);
        ResponseEntity<LoginResult> re = restTemplate.exchange(
                "http://ts-sso-service:12349/account/login",
                HttpMethod.POST,
                requestEntity,
                LoginResult.class);
        LoginResult lr = re.getBody();
        //将cookie放到response中
        System.out.println("[Login Service] Status:" + lr.getStatus());
        if(lr.getStatus() == false){
            System.out.println("[Login Service] Status: false. Cookie wrong.");
        }else{
            System.out.println("[Login Service] Status: true. Put Cookie.");
            CookieUtil.addCookie(response, "loginId", lr.getAccount().getId().toString(), COOKIE_EXPIRED);
            CookieUtil.addCookie(response, "loginToken", lr.getToken(), COOKIE_EXPIRED);
        }
        return lr;
    }

    @Override
    public LogoutResult logout(LogoutInfo li,HttpServletRequest request,HttpServletResponse response, HttpHeaders headers){
//        LogoutResult lr = restTemplate.postForObject("http://ts-sso-service:12349/logout",li,LogoutResult.class);
        HttpEntity requestEntity = new HttpEntity(li,headers);
        ResponseEntity<LogoutResult> re = restTemplate.exchange(
                "http://ts-sso-service:12349/logout",
                HttpMethod.POST,
                requestEntity,
                LogoutResult.class);
        LogoutResult lr = re.getBody();
        if(lr.isStatus()){
            System.out.println("[Login Service][Logout] Success");
        }else{
            System.out.println("[Login Service][Logout] Fail.Reason:" + lr.getMessage());
        }
        handleLogOutResponse(request, response);
        return lr;
    }

    private void handleLogOutResponse(HttpServletRequest request,HttpServletResponse response) {
//        Cookie[] cookies = request.getCookies();
//        for (Cookie cookie : cookies) {
//            if(cookie.getName().equals("YsbCaptcha")){
//                continue;
//            }
//            cookie.setMaxAge(0);
//            cookie.setValue(null);
//            cookie.setPath("/");
//            response.addCookie(cookie);
//        }
    }

}
