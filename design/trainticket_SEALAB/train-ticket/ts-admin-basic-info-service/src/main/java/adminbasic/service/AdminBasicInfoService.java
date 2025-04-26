package adminbasic.service;

import adminbasic.domin.bean.Config;
import adminbasic.domin.bean.Contacts;
import adminbasic.domin.bean.Station;
import adminbasic.domin.bean.TrainType;
import adminbasic.domin.info.*;
import adminbasic.domin.reuslt.*;
import org.springframework.http.HttpHeaders;

public interface AdminBasicInfoService {

    ////////////contact/////////////////////////////////////////
    GetAllContactsResult getAllContacts(String loginId, HttpHeaders headers);

    AddContactsResult addContact(String loginId, Contacts c, HttpHeaders headers);

    DeleteContactsResult deleteContact(String loginId, DeleteContactsInfo dci, HttpHeaders headers);

    ModifyContactsResult modifyContact(String loginId, ModifyContactsInfo mci, HttpHeaders headers);

    ////////////////////////////station///////////////////////////////
    GetAllStationResult getAllStations(String loginId, HttpHeaders headers);

    boolean addStation(Station s, HttpHeaders headers);

    boolean deleteStation( Station s, HttpHeaders headers);

    boolean modifyStation( Station s, HttpHeaders headers);

    ////////////////////////////train///////////////////////////////
    GetAllTrainResult getAllTrains(String loginId, HttpHeaders headers);

    boolean addTrain(TrainType t, HttpHeaders headers);

    boolean deleteTrain(TrainInfo2 t, HttpHeaders headers);

    boolean modifyTrain( TrainType t, HttpHeaders headers);

    ////////////////////////////config///////////////////////////////
    GetAllConfigResult getAllConfigs(String loginId, HttpHeaders headers);

    String addConfig(Config c, HttpHeaders headers);

    String deleteConfig(ConfigInfo2 ci, HttpHeaders headers);

    String modifyConfig( Config c, HttpHeaders headers);

    ////////////////////////////price///////////////////////////////
    GetAllPriceResult getAllPrices(String loginId, HttpHeaders headers);

    ReturnSinglePriceConfigResult addPrice(PriceInfo pi, HttpHeaders headers);

    boolean deletePrice(PriceInfo pi, HttpHeaders headers);

    boolean modifyPrice(PriceInfo pi, HttpHeaders headers);

//    Contacts login(String name, String password);

}
