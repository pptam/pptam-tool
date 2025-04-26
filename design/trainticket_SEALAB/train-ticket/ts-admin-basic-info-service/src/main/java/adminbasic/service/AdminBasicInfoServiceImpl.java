package adminbasic.service;

import adminbasic.domin.bean.*;
import adminbasic.domin.info.*;
import adminbasic.domin.reuslt.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import java.util.List;

@Service
public class  AdminBasicInfoServiceImpl implements AdminBasicInfoService{

    @Autowired
    private RestTemplate restTemplate;

    private String adminID="1d1a11c1-11cb-1cf1-b1bb-b11111d1da1f";


    @Override
    public  GetAllContactsResult getAllContacts(String loginId, HttpHeaders headers) {
        GetAllContactsResult result ;
        if(adminID.equals(loginId)){
            HttpEntity requestEntity = new HttpEntity(headers);
            ResponseEntity<GetAllContactsResult> re = restTemplate.exchange(
                    "http://ts-contacts-service:12347/contacts/findAll",
                    HttpMethod.GET,
                    requestEntity,
                    GetAllContactsResult.class);
            result = re.getBody();
//            result = restTemplate.getForObject(
//                    "http://ts-contacts-service:12347/contacts/findAll",
//                    GetAllContactsResult.class);
        } else {
            result = new GetAllContactsResult();
            result.setStatus(false);
            result.setMessage("The loginId is Wrong: " + loginId);
        }

        return result;
    }

    @Override
    public DeleteContactsResult deleteContact(String loginId, DeleteContactsInfo dci, HttpHeaders headers) {
        DeleteContactsResult result;
        if(adminID.equals(loginId)){
            HttpEntity requestEntity = new HttpEntity(dci, headers);
            ResponseEntity<DeleteContactsResult> re = restTemplate.exchange(
                    "http://ts-contacts-service:12347/contacts/deleteContacts",
                    HttpMethod.POST,
                    requestEntity,
                    DeleteContactsResult.class);
            result = re.getBody();
//            result = restTemplate.postForObject(
//                    "http://ts-contacts-service:12347/contacts/deleteContacts",dci,
//                    DeleteContactsResult.class);
        } else {
            result = new DeleteContactsResult();
            result.setStatus(false);
            result.setMessage("The loginId is Wrong: " + loginId);
        }
        return result;
    }

    @Override
    public ModifyContactsResult modifyContact(String loginId, ModifyContactsInfo mci, HttpHeaders headers) {
        ModifyContactsResult result;
        if(adminID.equals(loginId)){
            HttpEntity requestEntity = new HttpEntity(mci, headers);
            ResponseEntity<ModifyContactsResult> re = restTemplate.exchange(
                    "http://ts-contacts-service:12347/contacts/modifyContacts",
                    HttpMethod.POST,
                    requestEntity,
                    ModifyContactsResult.class);
            result = re.getBody();
//            result = restTemplate.postForObject(
//                    "http://ts-contacts-service:12347/contacts/modifyContacts",mci,
//                    ModifyContactsResult.class);
        } else {
            result = new ModifyContactsResult();
            result.setStatus(false);
            result.setMessage("The loginId is Wrong: " + loginId);
        }
        return result;
    }


    @Override
    public AddContactsResult addContact(String loginId, Contacts c, HttpHeaders headers) {
        AddContactsResult result;
        if (adminID.equals(loginId)) {
            HttpEntity requestEntity = new HttpEntity(c, headers);
            ResponseEntity<AddContactsResult> re = restTemplate.exchange(
                    "http://ts-contacts-service:12347/contacts/admincreate",
                    HttpMethod.POST,
                    requestEntity,
                    AddContactsResult.class);
            result = re.getBody();
//            result = restTemplate.postForObject(
//                    "http://ts-contacts-service:12347/contacts/admincreate",c,
//                    AddContactsResult.class);

        } else {
            result = new AddContactsResult();
            result.setStatus(false);
            result.setMessage("The Contact add operation failed.");
        }
        return result;
    }

    //////////////station////////////////////////////////////////////////
    @Override
    public GetAllStationResult getAllStations(String loginId, HttpHeaders headers) {
        GetAllStationResult result = new GetAllStationResult();;
        if (adminID.equals(loginId)) {
            List<Station> l;
            HttpEntity requestEntity = new HttpEntity(headers);
            ResponseEntity<List<Station>> re = restTemplate.exchange(
                    "http://ts-station-service:12345/station/query",
                    HttpMethod.GET,
                    requestEntity,
                    new ParameterizedTypeReference<List<Station>>(){});
            l = re.getBody();
//            l= restTemplate.getForObject("http://ts-station-service:12345/station/query", l.getClass());
            result.setStatus(true);
            result.setMessage("Success");
            result.setStationList(l);
        } else {
            result.setStatus(false);
            result.setMessage("The loginId is Wrong: " + loginId);
        }
        return result;
    }

    @Override
    public boolean addStation(Station s, HttpHeaders headers) {
        boolean result = false;
        if (adminID.equals(s.getLoginId())) {
            HttpEntity requestEntity = new HttpEntity(s, headers);
            ResponseEntity<Boolean> re = restTemplate.exchange(
                    "http://ts-station-service:12345/station/create",
                    HttpMethod.POST,
                    requestEntity,
                    Boolean.class);
            result = re.getBody();

//            result = restTemplate.postForObject("http://ts-station-service:12345/station/create",s, Boolean.class);
            return result;
        }
        return result;
    }

    @Override
    public boolean deleteStation(Station s, HttpHeaders headers) {
        boolean result = false;
        if (adminID.equals(s.getLoginId())) {
            HttpEntity requestEntity = new HttpEntity(s, headers);
            ResponseEntity<Boolean> re = restTemplate.exchange(
                    "http://ts-station-service:12345/station/delete",
                    HttpMethod.POST,
                    requestEntity,
                    Boolean.class);
            result = re.getBody();

//            result = restTemplate.postForObject("http://ts-station-service:12345/station/delete",s, Boolean.class);
            return result;
        }
        return result;
    }

    @Override
    public boolean modifyStation(Station s, HttpHeaders headers) {
        boolean result = false;
        if (adminID.equals(s.getLoginId())) {
            HttpEntity requestEntity = new HttpEntity(s, headers);
            ResponseEntity<Boolean> re = restTemplate.exchange(
                    "http://ts-station-service:12345/station/update",
                    HttpMethod.POST,
                    requestEntity,
                    Boolean.class);
            result = re.getBody();
//            result = restTemplate.postForObject("http://ts-station-service:12345/station/update",s, Boolean.class);
            return result;
        }
        return result;
    }

    //////////////train////////////////////////////////////////////////
    @Override
    public GetAllTrainResult getAllTrains(String loginId, HttpHeaders headers) {
        GetAllTrainResult result = new GetAllTrainResult();
        if (adminID.equals(loginId)) {
            List<TrainType> l;
            HttpEntity requestEntity = new HttpEntity(headers);
            ResponseEntity<List<TrainType>> re = restTemplate.exchange(
                    "http://ts-train-service:14567/train/query",
                    HttpMethod.GET,
                    requestEntity,
                    new ParameterizedTypeReference<List<TrainType>>(){});
            l = re.getBody();

//            List<TrainType> l = new ArrayList<TrainType>();
//            l = restTemplate.getForObject("http://ts-train-service:14567/train/query", l.getClass());
            result.setStatus(true);
            result.setMessage("Success");
            result.setTrainList(l);
            return result;
        } else {
            result.setStatus(false);
            result.setMessage("The loginId is wrong:"+ loginId);
        }
        return result;
    }

    @Override
    public boolean addTrain(TrainType t, HttpHeaders headers) {
        boolean result = false;
        if (adminID.equals(t.getLoginId())) {
            HttpEntity requestEntity = new HttpEntity(t, headers);
            ResponseEntity<Boolean> re = restTemplate.exchange(
                    "http://ts-train-service:14567/train/create",
                    HttpMethod.POST,
                    requestEntity,
                    Boolean.class);
            result = re.getBody();
//            result = restTemplate.postForObject("http://ts-train-service:14567/train/create",t, Boolean.class);
            return result;
        }
        return result;
    }

    @Override
    public boolean deleteTrain(TrainInfo2 t, HttpHeaders headers) {
        boolean result = false;
        if (adminID.equals(t.getLoginId())) {
            HttpEntity requestEntity = new HttpEntity(t, headers);
            ResponseEntity<Boolean> re = restTemplate.exchange(
                    "http://ts-train-service:14567/train/delete",
                    HttpMethod.POST,
                    requestEntity,
                    Boolean.class);
            result = re.getBody();
//            result = restTemplate.postForObject("http://ts-train-service:14567/train/delete",t, Boolean.class);
            return result;
        }
        return result;
    }

    @Override
    public boolean modifyTrain(TrainType t, HttpHeaders headers) {
        boolean result = false;
        if (adminID.equals(t.getLoginId())) {
            HttpEntity requestEntity = new HttpEntity(t, headers);
            ResponseEntity<Boolean> re = restTemplate.exchange(
                    "http://ts-train-service:14567/train/update",
                    HttpMethod.POST,
                    requestEntity,
                    Boolean.class);
            result = re.getBody();
//            result = restTemplate.postForObject("http://ts-train-service:14567/train/update",t, Boolean.class);
            return result;
        }
        return result;
    }

    //////////////config////////////////////////////////////////////////
    @Override
    public GetAllConfigResult getAllConfigs(String loginId, HttpHeaders headers) {
        GetAllConfigResult result = new GetAllConfigResult();
        if (adminID.equals(loginId)) {
            List<Config> l;
            HttpEntity requestEntity = new HttpEntity(headers);
            ResponseEntity<List<Config>> re = restTemplate.exchange(
                    "http://ts-config-service:15679/config/queryAll",
                    HttpMethod.GET,
                    requestEntity,
                    new ParameterizedTypeReference<List<Config>>(){});
            l = re.getBody();

//            List<Config> l = new ArrayList<Config>();
//            l = restTemplate.getForObject("http://ts-config-service:15679/config/queryAll", l.getClass());
            result.setStatus(true);
            result.setMessage("Success");
            result.setConfigs(l);
            return result;
        } else {
            result.setStatus(false);
            result.setMessage("The loginId is wrong:"+ loginId);
        }
        return result;
    }

    @Override
    public String addConfig(Config c, HttpHeaders headers) {
        String result = null;
        if (adminID.equals(c.getLoginId())) {
            HttpEntity requestEntity = new HttpEntity(c, headers);
            ResponseEntity<String> re = restTemplate.exchange(
                    "http://ts-config-service:15679/config/create",
                    HttpMethod.POST,
                    requestEntity,
                    String.class);
            result = re.getBody();
//            result = restTemplate.postForObject("http://ts-config-service:15679/config/create",c, String.class);
            return result;
        }
        return result;
    }

    @Override
    public String deleteConfig(ConfigInfo2 ci, HttpHeaders headers) {
        String result = null;
        if (adminID.equals(ci.getLoginId())) {
            HttpEntity requestEntity = new HttpEntity(ci, headers);
            ResponseEntity<String> re = restTemplate.exchange(
                    "http://ts-config-service:15679/config/delete",
                    HttpMethod.POST,
                    requestEntity,
                    String.class);
            result = re.getBody();
//            result = restTemplate.postForObject("http://ts-config-service:15679/config/delete",ci, String.class);
            return result;
        }
        return result;
    }

    @Override
    public String modifyConfig(Config c, HttpHeaders headers) {
        String result = null;
        if (adminID.equals(c.getLoginId())) {
            HttpEntity requestEntity = new HttpEntity(c, headers);
            ResponseEntity<String> re = restTemplate.exchange(
                    "http://ts-config-service:15679/config/update",
                    HttpMethod.POST,
                    requestEntity,
                    String.class);
            result = re.getBody();
//            result = restTemplate.postForObject("http://ts-config-service:15679/config/update",c, String.class);
            return result;
        }
        return result;
    }

    //////////////price////////////////////////////////////////////////
    @Override
    public GetAllPriceResult getAllPrices(String loginId, HttpHeaders headers) {
        GetAllPriceResult result = new GetAllPriceResult();
        if (adminID.equals(loginId)) {
            HttpEntity requestEntity = new HttpEntity(headers);
            ResponseEntity<GetAllPriceResult> re = restTemplate.exchange(
                    "http://ts-price-service:16579/price/queryAll",
                    HttpMethod.GET,
                    requestEntity,
                    GetAllPriceResult.class);
            result = re.getBody();

//            result = restTemplate.getForObject("http://ts-price-service:16579/price/queryAll", GetAllPriceResult.class);
            System.out.println("[!!!!GetAllPriceResult] " + result.getPriceConfig());
            return result;
        } else {
            result.setStatus(false);
            result.setMessage("The loginId is wrong:"+ loginId);
        }
        return result;
    }

    @Override
    public ReturnSinglePriceConfigResult addPrice(PriceInfo pi, HttpHeaders headers) {
        ReturnSinglePriceConfigResult result = new ReturnSinglePriceConfigResult();
        if (adminID.equals(pi.getLoginId())) {
            HttpEntity requestEntity = new HttpEntity(pi, headers);
            ResponseEntity<ReturnSinglePriceConfigResult> re = restTemplate.exchange(
                    "http://ts-price-service:16579/price/create",
                    HttpMethod.POST,
                    requestEntity,
                    ReturnSinglePriceConfigResult.class);
            result = re.getBody();
//            result = restTemplate.postForObject("http://ts-price-service:16579/price/create",pi, ReturnSinglePriceConfigResult.class);
            return result;
        } else {
            result.setStatus(false);
            result.setMessage("The loginId is wrong:"+ pi.getLoginId());
        }
        return result;
    }

    @Override
    public boolean deletePrice(PriceInfo pi, HttpHeaders headers) {
        boolean result = false;
        if (adminID.equals(pi.getLoginId())) {
            HttpEntity requestEntity = new HttpEntity(pi, headers);
            ResponseEntity<Boolean> re = restTemplate.exchange(
                    "http://ts-price-service:16579/price/delete",
                    HttpMethod.POST,
                    requestEntity,
                    Boolean.class);
            result = re.getBody();
//            result = restTemplate.postForObject("http://ts-price-service:16579/price/delete",pi, Boolean.class);
            return result;
        }
        return result;
    }

    @Override
    public boolean modifyPrice(PriceInfo pi, HttpHeaders headers) {
        boolean result = false;
        if (adminID.equals(pi.getLoginId())) {
            HttpEntity requestEntity = new HttpEntity(pi, headers);
            ResponseEntity<Boolean> re = restTemplate.exchange(
                    "http://ts-price-service:16579/price/update",
                    HttpMethod.POST,
                    requestEntity,
                    Boolean.class);
            result = re.getBody();
//            result = restTemplate.postForObject("http://ts-price-service:16579/price/update",pi, Boolean.class);
            return result;
        }
        return result;
    }


}
