package assurance.controller;

import assurance.domain.*;
import assurance.service.AssuranceService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import java.util.List;
import java.util.UUID;

@RestController
public class AssuranceController {

    @Autowired
    private AssuranceService assuranceService;

    @Autowired
    private RestTemplate restTemplate;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home(@RequestHeader HttpHeaders headers){
        return "Welcome to [ Assurance Service ] !";
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/assurance/findAll", method = RequestMethod.GET)
    public GetAllAssuranceResult getAllAssurances(@RequestHeader HttpHeaders headers){
        System.out.println("[Assurances Service][Get All Assurances]");
        return assuranceService.getAllAssurances(headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/assurance/getAllAssuranceType", method = RequestMethod.GET)
    public List<AssuranceTypeBean> getAllAssuranceType(@RequestHeader HttpHeaders headers){
        System.out.println("[Assurances Service][Get Assurance Type]");
        return assuranceService.getAllAssuranceTypes(headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/assurance/deleteAssurance", method = RequestMethod.POST)
    public DeleteAssuranceResult deleteAssurance(@RequestParam(value="assuranceId",required = true) String assuranceId, @RequestHeader HttpHeaders headers){
        System.out.println("[Assurances Service][Delete Assurance]");
        return assuranceService.deleteById(UUID.fromString(assuranceId), headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/assurance/deleteAssuranceByOrderId", method = RequestMethod.POST)
    public DeleteAssuranceResult deleteAssuranceByOrderId(@RequestParam(value="orderId",required = true) String orderId, @RequestHeader HttpHeaders headers){
        System.out.println("[Assurances Service][Delete Assurance by orderId]");
        return assuranceService.deleteByOrderId(UUID.fromString(orderId), headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/assurance/modifyAssurance", method = RequestMethod.POST)
    public ModifyAssuranceResult modifyAssurance(@RequestBody ModifyAssuranceInfo modifyAssuranceInfo, @RequestHeader HttpHeaders headers){
        System.out.println("[Assurances Service][Modify Assurance]");
        return assuranceService.modify(modifyAssuranceInfo, headers);
    }

    ///////////////////////////////////////////////////////////////////////////////////////

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/assurance/create", method = RequestMethod.POST)
    public AddAssuranceResult createNewAssurance(@RequestBody AddAssuranceInfo addAssuranceInfo, @RequestHeader HttpHeaders headers){
//        VerifyResult tokenResult = verifySsoLogin(loginToken);
//        if(tokenResult.isStatus() == true){
//            System.out.println("[AssuranceService][VerifyLogin] Success.");
            return assuranceService.create(addAssuranceInfo, headers);
//        }else {
//            System.out.println("[AssuranceService][VerifyLogin] Fail.");
//            AddAssuranceResult aar = new AddAssuranceResult();
//            return aar;
//        }
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/assurance/getAssuranceById", method = RequestMethod.GET)
    public Assurance getAssuranceById(@RequestBody GetAssuranceById gabi, @CookieValue String loginId, @CookieValue String loginToken, @RequestHeader HttpHeaders headers){
//        VerifyResult tokenResult = verifySsoLogin(loginToken);
//        if(tokenResult.isStatus() == true){
//            System.out.println("[AssuranceService][VerifyLogin] Success.");
            return assuranceService.findAssuranceById(UUID.fromString(gabi.getAssuranceId()), headers);
//        }else {
//            System.out.println("[AssuranceService][VerifyLogin] Fail.");
//            Assurance resultAssurance = new Assurance();
//            return resultAssurance;
//        }
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/assurance/findAssuranceByOrderId", method = RequestMethod.GET)
    public Assurance findAssuranceByOrderId(@RequestBody FindAssuranceByOrderId gabi, @RequestHeader HttpHeaders headers){
//        VerifyResult tokenResult = verifySsoLogin(gabi.getLoginToken());
//        if(tokenResult.isStatus() == true){
//            System.out.println("[AssuranceService][VerifyLogin] Success.");
            return assuranceService.findAssuranceByOrderId(UUID.fromString(gabi.getOrderId()), headers);
//        }else {
//            System.out.println("[AssuranceService][VerifyLogin] Fail.");
//            Assurance resultAssurance = new Assurance();
//            return resultAssurance;
//        }
    }

    private VerifyResult verifySsoLogin(String loginToken, @RequestHeader HttpHeaders headers){
        System.out.println("[Order Service][Verify Login] Verifying....");

        HttpEntity requestTokenResult = new HttpEntity(null,headers);
        ResponseEntity<VerifyResult> reTokenResult  = restTemplate.exchange(
                "http://ts-sso-service:12349/verifyLoginToken/" + loginToken,
                HttpMethod.GET,
                requestTokenResult,
                VerifyResult.class);
        VerifyResult tokenResult = reTokenResult.getBody();
//        VerifyResult tokenResult = restTemplate.getForObject(
//                "http://ts-sso-service:12349/verifyLoginToken/" + loginToken,
//                VerifyResult.class);


        return tokenResult;
    }
}
