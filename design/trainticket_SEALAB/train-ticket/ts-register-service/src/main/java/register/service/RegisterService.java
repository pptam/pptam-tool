package register.service;

import org.springframework.http.HttpHeaders;
import register.domain.RegisterInfo;
import register.domain.RegisterResult;

public interface RegisterService {

    RegisterResult create(RegisterInfo ri,String YsbCaptcha, HttpHeaders headers);

}
