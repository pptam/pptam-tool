package security.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.*;
import security.domain.*;
import security.domain.CheckResult;
import security.domain.CheckInfo;
import security.service.SecurityService;

@RestController
public class SecurityController {

    @Autowired
    private SecurityService securityService;

    @RequestMapping(value = "/welcome", method = RequestMethod.GET)
    public String home(@RequestHeader HttpHeaders headers){
        return "welcome to [Security Service]";
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/securityConfig/findAll", method = RequestMethod.GET)
    public GetAllSecurityConfigResult findAllSecurityConfig(@RequestHeader HttpHeaders headers){
        System.out.println("[Security Service][Find All]");
        return securityService.findAllSecurityConfig(headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/securityConfig/create", method = RequestMethod.POST)
    public CreateSecurityConfigResult create(@RequestBody CreateSecurityConfigInfo info,@RequestHeader HttpHeaders headers){
        System.out.println("[Security Service][Create] Name:" + info.getName());
        return securityService.addNewSecurityConfig(info,headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/securityConfig/update", method = RequestMethod.POST)
    public UpdateSecurityConfigResult update(@RequestBody UpdateSecurityConfigInfo info,@RequestHeader HttpHeaders headers){
        System.out.println("[Security Service][Update] Name:" + info.getName());
        return securityService.modifySecurityConfig(info,headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/securityConfig/delete", method = RequestMethod.POST)
    public DeleteConfigResult delete(@RequestBody DeleteConfigInfo info,@RequestHeader HttpHeaders headers){
        System.out.println("[Security Service][Delete] Id:" + info.getId());
        return securityService.deleteSecurityConfig(info,headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/security/check", method = RequestMethod.POST)
    public CheckResult check(@RequestBody CheckInfo info, @RequestHeader HttpHeaders headers){
        System.out.println("[Security Service][Check Security] Check Account Id:" + info.getAccountId());
        return securityService.check(info,headers);
    }
}
