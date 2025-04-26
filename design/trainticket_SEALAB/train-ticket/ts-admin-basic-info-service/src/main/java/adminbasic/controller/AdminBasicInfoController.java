package adminbasic.controller;

import adminbasic.domin.bean.Config;
import adminbasic.domin.bean.Contacts;
import adminbasic.domin.bean.Station;
import adminbasic.domin.bean.TrainType;
import adminbasic.domin.info.*;
import adminbasic.domin.reuslt.*;
import adminbasic.service.AdminBasicInfoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.*;

@RestController
public class AdminBasicInfoController {

    @Autowired
    AdminBasicInfoService adminBasicInfoService;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home(@RequestHeader HttpHeaders headers) {
        return "Welcome to [ AdminBasicInfo Service ] !";
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/adminbasic/getAllContacts/{id}", method = RequestMethod.GET)
    public GetAllContactsResult getAllContacts(@PathVariable String id, @RequestHeader HttpHeaders headers){
        System.out.println("[Admin Basic Info Service][Find All Contacts by admin: " + id);
        return adminBasicInfoService.getAllContacts(id, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/adminbasic/deleteContacts", method = RequestMethod.POST)
    public DeleteContactsResult deleteContacts(@RequestBody DeleteContactsInfo dci, @RequestHeader HttpHeaders headers){
        System.out.println("[Admin Basic Info Service][Delete Contacts by admin: " + dci.getLoginId());
        return adminBasicInfoService.deleteContact(dci.getLoginId(), dci, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/adminbasic/modifyContacts", method = RequestMethod.POST)
    public ModifyContactsResult modifyContacts(@RequestBody ModifyContactsInfo mci, @RequestHeader HttpHeaders headers){
        System.out.println("[Admin Basic Info Service][Modify Contacts by admin: " + mci.getLoginId());
        return adminBasicInfoService.modifyContact(mci.getLoginId(), mci, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/adminbasic/addContacts", method = RequestMethod.POST)
    public AddContactsResult addContacts(@RequestBody Contacts c, @RequestHeader HttpHeaders headers){
        System.out.println("[Admin Basic Info Service][Modify Contacts by admin: " + c.getLoginId());
        return adminBasicInfoService.addContact(c.getLoginId(), c, headers);
    }

    /////////////////////////station/////////////////////////////////////////////////////////////////////////////////
    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/adminbasic/getAllStations/{id}", method = RequestMethod.GET)
    public GetAllStationResult getAllStations(@PathVariable String id, @RequestHeader HttpHeaders headers){
        System.out.println("[Admin Basic Info Service][Find All Station by admin: " + id);
        return adminBasicInfoService.getAllStations(id, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/adminbasic/deleteStation", method = RequestMethod.POST)
    public boolean deleteStation(@RequestBody Station s, @RequestHeader HttpHeaders headers){
        System.out.println("[Admin Basic Info Service][Delete Station by admin: " + s.getLoginId());
        return adminBasicInfoService.deleteStation(s, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/adminbasic/modifyStation", method = RequestMethod.POST)
    public boolean modifyStation(@RequestBody Station s, @RequestHeader HttpHeaders headers){
        System.out.println("[Admin Basic Info Service][Modify Station by admin: " + s.getLoginId());
        return adminBasicInfoService.modifyStation(s, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/adminbasic/addStation", method = RequestMethod.POST)
    public boolean addStation(@RequestBody Station s, @RequestHeader HttpHeaders headers){
        System.out.println("[Admin Basic Info Service][Modify Station by admin: " + s.getLoginId());
        return adminBasicInfoService.addStation(s, headers);
    }

    /////////////////////////train/////////////////////////////////////////////////////////////////////////////////
    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/adminbasic/getAllTrains/{id}", method = RequestMethod.GET)
    public GetAllTrainResult getAllTrains(@PathVariable String id, @RequestHeader HttpHeaders headers){
        System.out.println("[Admin Basic Info Service][Find All Train by admin: " + id);
        return adminBasicInfoService.getAllTrains(id, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/adminbasic/deleteTrain", method = RequestMethod.POST)
    public boolean deleteTrain(@RequestBody TrainInfo2 t, @RequestHeader HttpHeaders headers){
        System.out.println("[Admin Basic Info Service][Delete Train by admin: " + t.getLoginId());
        return adminBasicInfoService.deleteTrain(t, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/adminbasic/modifyTrain", method = RequestMethod.POST)
    public boolean modifyTrain(@RequestBody TrainType t, @RequestHeader HttpHeaders headers){
        System.out.println("[Admin Basic Info Service][Modify Train by admin: " + t.getLoginId());
        return adminBasicInfoService.modifyTrain(t, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/adminbasic/addTrain", method = RequestMethod.POST)
    public boolean addTrain(@RequestBody TrainType t, @RequestHeader HttpHeaders headers){
        System.out.println("[Admin Basic Info Service][Modify Train by admin: " + t.getLoginId());
        return adminBasicInfoService.addTrain(t, headers);
    }

    /////////////////////////config/////////////////////////////////////////////////////////////////////////////////
    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/adminbasic/getAllConfigs/{id}", method = RequestMethod.GET)
    public GetAllConfigResult getAllConfigs(@PathVariable String id, @RequestHeader HttpHeaders headers){
        System.out.println("[Admin Basic Info Service][Find All Config by admin: " + id);
        return adminBasicInfoService.getAllConfigs(id, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/adminbasic/deleteConfig", method = RequestMethod.POST)
    public String deleteConfig(@RequestBody ConfigInfo2 c, @RequestHeader HttpHeaders headers){
        System.out.println("[Admin Basic Info Service][Delete Config by admin: " + c.getLoginId());
        return adminBasicInfoService.deleteConfig(c, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/adminbasic/modifyConfig", method = RequestMethod.POST)
    public String modifyConfig(@RequestBody Config c, @RequestHeader HttpHeaders headers){
        System.out.println("[Admin Basic Info Service][Modify Config by admin: " + c.getLoginId());
        return adminBasicInfoService.modifyConfig(c, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/adminbasic/addConfig", method = RequestMethod.POST)
    public String addConfig(@RequestBody Config c, @RequestHeader HttpHeaders headers){
        System.out.println("[Admin Basic Info Service][Modify Config by admin: " + c.getLoginId());
        return adminBasicInfoService.addConfig(c, headers);
    }

    /////////////////////////price/////////////////////////////////////////////////////////////////////////////////
    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/adminbasic/getAllPrices/{id}", method = RequestMethod.GET)
    public GetAllPriceResult getAllPrices(@PathVariable String id, @RequestHeader HttpHeaders headers){
        System.out.println("[Admin Basic Info Service][Find All Price by admin: " + id);
        return adminBasicInfoService.getAllPrices(id, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/adminbasic/deletePrice", method = RequestMethod.POST)
    public boolean deletePrice(@RequestBody PriceInfo pi, @RequestHeader HttpHeaders headers){
        System.out.println("[Admin Basic Info Service][Delete Price by admin: " + pi.getLoginId());
        return adminBasicInfoService.deletePrice(pi, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/adminbasic/modifyPrice", method = RequestMethod.POST)
    public boolean modifyPrice(@RequestBody PriceInfo pi, @RequestHeader HttpHeaders headers){
        System.out.println("[Admin Basic Info Service][Modify Price by admin: " + pi.getLoginId());
        return adminBasicInfoService.modifyPrice(pi, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/adminbasic/addPrice", method = RequestMethod.POST)
    public ReturnSinglePriceConfigResult addPrice(@RequestBody PriceInfo pi, @RequestHeader HttpHeaders headers){
        System.out.println("[Admin Basic Info Service][Add Price by admin: " + pi.getLoginId());
        return adminBasicInfoService.addPrice(pi, headers);
    }


}
