package fdse.microservice.service;
import fdse.microservice.domain.*;
import org.springframework.http.HttpHeaders;

import java.util.ArrayList;
import java.util.List;

public interface StationService {
    //CRUD
    boolean create(Information info,HttpHeaders headers);
    boolean exist(QueryStation info,HttpHeaders headers);
    boolean update(Information info,HttpHeaders headers);
    boolean delete(Information info,HttpHeaders headers);
    List<Station> query(HttpHeaders headers);


    String queryForId(QueryForId info,HttpHeaders headers);
    ArrayList<String> queryForIdBatch(QueryForIdBatch queryForIdBatch, HttpHeaders headers);

    QueryStation queryById(String stationId,HttpHeaders headers);
    ArrayList<String> queryByIdBatch(QueryByIdBatch queryByIdBatch, HttpHeaders headers);

}
