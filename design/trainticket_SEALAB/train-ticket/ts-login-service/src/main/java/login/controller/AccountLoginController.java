package login.controller;

import login.domain.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.*;
import login.service.AccountLoginService;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@RestController
public class AccountLoginController {

    @Autowired
    private AccountLoginService accountService;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home() {
        return "Welcome to [ Accounts Login Service ] !";
    }

    @RequestMapping(path = "/login", method = RequestMethod.POST)
    public LoginResult login(@RequestBody LoginInfo li, @CookieValue String YsbCaptcha,  HttpServletResponse response,@RequestHeader HttpHeaders headers){
        System.out.println(String.format("The headers in login service is %s", headers.toString()));
        if(YsbCaptcha == null || YsbCaptcha.length() == 0 ||
                li.getEmail() == null || li.getEmail().length() == 0 ||
                li.getPassword() == null || li.getPassword().length() == 0 ||
                li.getVerificationCode() == null || li.getEmail().length() == 0){
            LoginResult errorResult = new LoginResult();
            errorResult.setAccount(null);
            errorResult.setMessage("Verification Code or Email or Password format wrong.");
            errorResult.setStatus(false);
            errorResult.setToken(null);
            return errorResult;
        }
        System.out.println("[Login Service][Login] Verification Code:" + li.getVerificationCode() +
                " VerifyCookie:" + YsbCaptcha);
        return accountService.login(li,YsbCaptcha, response,headers);
    }

    @RequestMapping(path = "/logout", method = RequestMethod.POST)
    public LogoutResult logout(@RequestBody LogoutInfo li, HttpServletRequest request, HttpServletResponse response, @RequestHeader HttpHeaders headers){
        System.out.println("[Login Service][Logout] Logout ID:" + li.getId() + " Token:" + li.getToken());
        return accountService.logout(li,request,response,headers);
    }

}