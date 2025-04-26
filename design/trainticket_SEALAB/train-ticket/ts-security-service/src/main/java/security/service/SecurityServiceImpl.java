package security.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import security.domain.*;
import security.repository.SecurityRepository;

import java.security.Security;
import java.util.Date;
import java.util.UUID;

@Service
public class SecurityServiceImpl implements SecurityService{

    @Autowired
    private SecurityRepository securityRepository;

    @Autowired
    RestTemplate restTemplate;

    @Override
    public GetAllSecurityConfigResult findAllSecurityConfig(HttpHeaders headers){
        GetAllSecurityConfigResult result = new GetAllSecurityConfigResult();
        result.setStatus(true);
        result.setMessage("Success");
        result.setResult(securityRepository.findAll());
        return result;
    }

    @Override
    public CreateSecurityConfigResult addNewSecurityConfig(CreateSecurityConfigInfo info, HttpHeaders headers){
        SecurityConfig sc = securityRepository.findByName(info.getName());
        CreateSecurityConfigResult result = new CreateSecurityConfigResult();
        if(sc != null){
            result.setStatus(false);
            result.setMessage("Security Config Already Exist");
            result.setSecurityConfig(null);
        }else{
            SecurityConfig config = new SecurityConfig();
            config.setId(UUID.randomUUID());
            config.setName(info.getName());
            config.setValue(info.getValue());
            config.setDescription(info.getDescription());
            securityRepository.save(config);
            result.setStatus(true);
            result.setMessage("Success");
            result.setSecurityConfig(config);
        }
        return result;
    }

    @Override
    public UpdateSecurityConfigResult modifySecurityConfig(UpdateSecurityConfigInfo info, HttpHeaders headers){
        SecurityConfig sc = securityRepository.findById(UUID.fromString(info.getId()));
        UpdateSecurityConfigResult result = new UpdateSecurityConfigResult();
        if(sc == null){
            result.setStatus(false);
            result.setMessage("Security Config Not Exist");
            result.setResult(null);
        }else{
            sc.setName(info.getName());
            sc.setValue(info.getValue());
            sc.setDescription(info.getDescription());
            securityRepository.save(sc);
            result.setStatus(true);
            result.setMessage("Success");
            result.setResult(sc);
        }
        return result;
    }

    @Override
    public DeleteConfigResult deleteSecurityConfig(DeleteConfigInfo info, HttpHeaders headers){
        securityRepository.deleteById(UUID.fromString(info.getId()));
        SecurityConfig sc = securityRepository.findById(UUID.fromString(info.getId()));
        DeleteConfigResult result = new DeleteConfigResult();
        if(sc == null){
            result.setStatus(true);
            result.setMessage("Success");
        }else{
            result.setStatus(false);
            result.setMessage("Reason Not clear");
        }
        return result;
    }

    @Override
    public CheckResult check(CheckInfo info,HttpHeaders headers){
        CheckResult result = new CheckResult();
        //1.获取自己过去一小时的订单数和总有效票数
        System.out.println("[Security Service][Get Order Num Info]");
        GetOrderInfoForSecurity infoOrder = new GetOrderInfoForSecurity();
        infoOrder.setAccountId(info.getAccountId());
        infoOrder.setCheckDate(new Date());
        GetOrderInfoForSecurityResult orderResult = getSecurityOrderInfoFromOrder(infoOrder,headers);
        GetOrderInfoForSecurityResult orderOtherResult = getSecurityOrderOtherInfoFromOrder(infoOrder,headers);
        int orderInOneHour = orderOtherResult.getOrderNumInLastOneHour() + orderResult.getOrderNumInLastOneHour();
        int totalValidOrder = orderOtherResult.getOrderNumOfValidOrder() + orderOtherResult.getOrderNumOfValidOrder();
        //2.获取关键配置信息
        System.out.println("[Security Service][Get Security Config Info]");
        SecurityConfig configMaxInHour = securityRepository.findByName("max_order_1_hour");
        SecurityConfig configMaxNotUse = securityRepository.findByName("max_order_not_use");
        System.out.println("[Security Service] Max In One Hour:" + configMaxInHour.getValue() + " Max Not Use:" + configMaxNotUse.getValue());
        int oneHourLine = Integer.parseInt(configMaxInHour.getValue());
        int totalValidLine = Integer.parseInt(configMaxNotUse.getValue());
        if(orderInOneHour > oneHourLine || totalValidOrder > totalValidLine){
            result.setStatus(false);
            result.setAccountId(info.getAccountId());
            result.setMessage("Too much order in last one hour or too much valid order");
        }else{
            result.setStatus(true);
            result.setMessage("Success.");
            result.setAccountId(info.getAccountId());
        }
        return result;
    }

    private GetOrderInfoForSecurityResult getSecurityOrderInfoFromOrder(GetOrderInfoForSecurity info, HttpHeaders headers){
        System.out.println("[Security Service][Get Order Info For Security] Getting....");
        HttpEntity requestEntity = new HttpEntity(info,headers);
        ResponseEntity<GetOrderInfoForSecurityResult> re = restTemplate.exchange(
                "http://ts-order-service:12031/getOrderInfoForSecurity",
                HttpMethod.POST,
                requestEntity,
                GetOrderInfoForSecurityResult.class);
        GetOrderInfoForSecurityResult result = re.getBody();
//        GetOrderInfoForSecurityResult result = restTemplate.postForObject(
//                "http://ts-order-service:12031/getOrderInfoForSecurity",info,
//                GetOrderInfoForSecurityResult.class);
        System.out.println("[Security Service][Get Order Info For Security] Last One Hour:" + result.getOrderNumInLastOneHour()
        + " Total Valid Order:" + result.getOrderNumOfValidOrder());
        return result;
    }

    private GetOrderInfoForSecurityResult getSecurityOrderOtherInfoFromOrder(GetOrderInfoForSecurity info, HttpHeaders headers){
        System.out.println("[Security Service][Get Order Other Info For Security] Getting....");
        HttpEntity requestEntity = new HttpEntity(info,headers);
        ResponseEntity<GetOrderInfoForSecurityResult> re = restTemplate.exchange(
                "http://ts-order-other-service:12032/getOrderOtherInfoForSecurity",
                HttpMethod.POST,
                requestEntity,
                GetOrderInfoForSecurityResult.class);
        GetOrderInfoForSecurityResult result = re.getBody();
//        GetOrderInfoForSecurityResult result = restTemplate.postForObject(
//                "http://ts-order-other-service:12032/getOrderOtherInfoForSecurity",info,
//                GetOrderInfoForSecurityResult.class);
        System.out.println("[Security Service][Get Order Other Info For Security] Last One Hour:" + result.getOrderNumInLastOneHour()
                + " Total Valid Order:" + result.getOrderNumOfValidOrder());
        return result;
    }

}
