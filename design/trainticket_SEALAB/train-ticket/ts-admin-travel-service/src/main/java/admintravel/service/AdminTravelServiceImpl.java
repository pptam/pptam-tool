package admintravel.service;

import admintravel.domain.bean.AdminTrip;
import admintravel.domain.request.AddAndModifyTravelRequest;
import admintravel.domain.request.DeleteTravelRequest;
import admintravel.domain.response.AdminFindAllResult;
import admintravel.domain.response.ResponseBean;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.ArrayList;

@Service
public class AdminTravelServiceImpl implements AdminTravelService {
    @Autowired
    private RestTemplate restTemplate;

    @Override
    public AdminFindAllResult getAllTravels(String id, HttpHeaders headers) {
        AdminFindAllResult result = new AdminFindAllResult();
        ArrayList<AdminTrip> trips = new ArrayList<AdminTrip>();
        if(checkId(id)){
            System.out.println("[Admin Travel Service][Get All Travels]");
            HttpEntity requestEntity = new HttpEntity(headers);
            ResponseEntity<AdminFindAllResult> re = restTemplate.exchange(
                    "http://ts-travel-service:12346/travel/adminQueryAll",
                    HttpMethod.GET,
                    requestEntity,
                    AdminFindAllResult.class);
            result = re.getBody();
//            result = restTemplate.getForObject(
//                    "http://ts-travel-service:12346/travel/adminQueryAll",
//                    AdminFindAllResult.class);
            if(result.isStatus()){
                System.out.println("[Admin Travel Service][Get Travel From ts-travel-service successfully!]");
                trips.addAll(result.getTrips());
            }
            else
                System.out.println("[Admin Travel Service][Get Travel From ts-travel-service fail!]");

            HttpEntity requestEntity2 = new HttpEntity(headers);
            ResponseEntity<AdminFindAllResult> re2 = restTemplate.exchange(
                    "http://ts-travel2-service:16346/travel2/adminQueryAll",
                    HttpMethod.GET,
                    requestEntity2,
                    AdminFindAllResult.class);
            result = re2.getBody();
//            result = restTemplate.getForObject(
//                    "http://ts-travel2-service:16346/travel2/adminQueryAll",
//                    AdminFindAllResult.class);
            if(result.isStatus()){
                System.out.println("[Admin Travel Service][Get Travel From ts-travel2-service successfully!]");
                trips.addAll(result.getTrips());
            }
            else
                System.out.println("[Admin Travel Service][Get Travel From ts-travel2-service fail!]");
            result.setTrips(trips);
        }
        else{
            result.setStatus(false);
            result.setMessage("Admin find all travel result fail: wrong login id");
            result.setTrips(null);
        }
        return result;
    }

    @Override
    public ResponseBean addTravel(AddAndModifyTravelRequest request, HttpHeaders headers) {
        ResponseBean responseBean = new ResponseBean();
        String result;
        if(checkId(request.getLoginId())){
            if(request.getTrainTypeId().charAt(0) == 'G' || request.getTrainTypeId().charAt(0) == 'D'){
                HttpEntity requestEntity = new HttpEntity(request, headers);
                ResponseEntity<String> re = restTemplate.exchange(
                        "http://ts-travel-service:12346/travel/create",
                        HttpMethod.POST,
                        requestEntity,
                        String.class);
                result = re.getBody();
//                result = restTemplate.postForObject(
//                        "http://ts-travel-service:12346/travel/create", request ,String.class);
            }else{
                HttpEntity requestEntity = new HttpEntity(request, headers);
                ResponseEntity<String> re = restTemplate.exchange(
                        "http://ts-travel2-service:16346/travel2/create",
                        HttpMethod.POST,
                        requestEntity,
                        String.class);
                result = re.getBody();
//                result = restTemplate.postForObject(
//                        "http://ts-travel2-service:16346/travel2/create", request ,String.class);

            }
            System.out.println("[Admin Travel Service][Admin add new travel]");
            responseBean.setStatus(true);
        }else{
            result = "Admin add new travel fail: wrong login id";
            System.out.println("[Admin Travel Service][Admin add new travel fail]");
            responseBean.setStatus(false);
        }
        responseBean.setMessage(result);
        return responseBean;
    }

    @Override
    public ResponseBean updateTravel(AddAndModifyTravelRequest request, HttpHeaders headers) {
        ResponseBean responseBean = new ResponseBean();
        String result;
        if(checkId(request.getLoginId())){
            if(request.getTrainTypeId().charAt(0) == 'G' || request.getTrainTypeId().charAt(0) == 'D'){
                HttpEntity requestEntity = new HttpEntity(request, headers);
                ResponseEntity<String> re = restTemplate.exchange(
                        "http://ts-travel-service:12346/travel/update",
                        HttpMethod.POST,
                        requestEntity,
                        String.class);
                result = re.getBody();
//                result = restTemplate.postForObject(
//                        "http://ts-travel-service:12346/travel/update", request ,String.class);
            }else{
                HttpEntity requestEntity = new HttpEntity(request, headers);
                ResponseEntity<String> re = restTemplate.exchange(
                        "http://ts-travel2-service:16346/travel2/update",
                        HttpMethod.POST,
                        requestEntity,
                        String.class);
                result = re.getBody();
//                result = restTemplate.postForObject(
//                        "http://ts-travel2-service:16346/travel2/update", request ,String.class);

            }
            System.out.println("[Admin Travel Service][Admin update travel]");
            responseBean.setStatus(true);
        }else{
            result = "Admin update travel fail: wrong login id";
            System.out.println("[Admin Travel Service][Admin update travel fail]");
            responseBean.setStatus(false);
        }
        responseBean.setMessage(result);
        return responseBean;
    }

    @Override
    public ResponseBean deleteTravel(DeleteTravelRequest request, HttpHeaders headers) {
        ResponseBean responseBean = new ResponseBean();
        String result;
        if(checkId(request.getLoginId())){
            if(request.getTripId().charAt(0) == 'G' || request.getTripId().charAt(0) == 'D'){
                HttpEntity requestEntity = new HttpEntity(request, headers);
                ResponseEntity<String> re = restTemplate.exchange(
                        "http://ts-travel-service:12346/travel/delete",
                        HttpMethod.POST,
                        requestEntity,
                        String.class);
                result = re.getBody();
//                result = restTemplate.postForObject(
//                        "http://ts-travel-service:12346/travel/delete", request ,String.class);
            }else{
                HttpEntity requestEntity = new HttpEntity(request, headers);
                ResponseEntity<String> re = restTemplate.exchange(
                        "http://ts-travel2-service:16346/travel2/delete",
                        HttpMethod.POST,
                        requestEntity,
                        String.class);
                result = re.getBody();
//                result = restTemplate.postForObject(
//                        "http://ts-travel2-service:16346/travel2/delete", request ,String.class);

            }
            System.out.println("[Admin Travel Service][Admin delete travel]");
            responseBean.setStatus(true);
        }else{
            result = "Admin delete travel fail: wrong login id";
            System.out.println("[Admin Travel Service][Admin delete travel fail]");
            responseBean.setStatus(false);
        }
        responseBean.setMessage(result);
        return responseBean;
    }

    private boolean checkId(String id){
        if("1d1a11c1-11cb-1cf1-b1bb-b11111d1da1f".equals(id)){
            return true;
        }
        else{
            return false;
        }
    }

}
