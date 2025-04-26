package register.controller;

import org.springframework.http.HttpHeaders;
import register.domain.RegisterInfo;
import register.domain.RegisterResult;
import register.service.RegisterService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
public class AccountRegisterController {

    @Autowired
    private RegisterService accountService;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home() {
        return "Welcome to [ Accounts Register Service ] !";
    }

    @RequestMapping(path = "/register", method = RequestMethod.POST)
    public RegisterResult createNewAccount(@RequestBody RegisterInfo ri,@CookieValue String YsbCaptcha,
                                           @RequestHeader HttpHeaders headers){
        System.out.println("[Register Service][Register] Verification Code:" + ri.getVerificationCode() +
                " VerifyCookie:" + YsbCaptcha);
        return accountService.create(ri,YsbCaptcha,headers);
    }
}
