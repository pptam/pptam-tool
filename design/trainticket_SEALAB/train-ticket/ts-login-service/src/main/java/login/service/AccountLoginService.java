package login.service;

import login.domain.LoginInfo;
import login.domain.LoginResult;
import login.domain.LogoutInfo;
import login.domain.LogoutResult;
import org.springframework.http.HttpHeaders;
import org.springframework.integration.dsl.http.Http;
import org.springframework.web.bind.annotation.CookieValue;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public interface AccountLoginService {

    LoginResult login(LoginInfo li, String YsbCaptcha, HttpServletResponse response, HttpHeaders headers);

    LogoutResult logout(LogoutInfo li, HttpServletRequest request, HttpServletResponse response, HttpHeaders headers);

}
