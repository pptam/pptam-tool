package ticketinfo.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import ticketinfo.domain.QueryForStationId;
import ticketinfo.domain.QueryForTravel;
import ticketinfo.domain.ResultForTravel;

/**
 * Created by Chenjie Xu on 2017/6/6.
 */
@Service
public class TicketInfoServiceImpl implements TicketInfoService{

    @Autowired
    private RestTemplate restTemplate;

    @Override
    public ResultForTravel queryForTravel(QueryForTravel info,HttpHeaders headers){
        HttpEntity requestEntity = new HttpEntity(info,headers);

        try{
            ResponseEntity<ResultForTravel> re = restTemplate.exchange(
                    "http://ts-basic-service:15680/basic/queryForTravel",
                    HttpMethod.POST,
                    requestEntity,
                    ResultForTravel.class);
            ResultForTravel result = re.getBody();
            return result;
        }catch(Exception e){
            ResponseEntity<String> sayHello = restTemplate.exchange(
                    "http://ts-basic-service:15680/welcome",
                    HttpMethod.GET,
                    requestEntity,
                    String.class);

            ResponseEntity<String> sayHelloPrice = restTemplate.exchange(
                    "http://ts-price-service:16579/welcome",
                    HttpMethod.GET,
                    requestEntity,
                    String.class);

            if(sayHello.getStatusCodeValue() == 200 && sayHelloPrice.getStatusCodeValue() == 200){
                ResultForTravel result = new ResultForTravel();
                result.setStatus(false);
                result.setMessage("OOM");
                return result;
            }else{
                ResultForTravel result = new ResultForTravel();
                result.setStatus(false);
                result.setMessage(sayHello.getBody());
                return null;
            }
        }


    }

    @Override
    public String queryForStationId(QueryForStationId info,HttpHeaders headers){
        HttpEntity requestEntity = new HttpEntity(info,headers);
        ResponseEntity<String> re = restTemplate.exchange(
                "http://ts-basic-service:15680/basic/queryForStationId",
                HttpMethod.POST,
                requestEntity,
                String.class);
        String id = re.getBody();
//        String id = restTemplate.postForObject(
//                "http://ts-basic-service:15680/basic/queryForStationId", info,String.class);
        return id;
    }
}
