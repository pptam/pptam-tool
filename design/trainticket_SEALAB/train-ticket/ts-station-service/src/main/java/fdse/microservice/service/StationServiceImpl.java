package fdse.microservice.service;

import fdse.microservice.domain.*;
import fdse.microservice.repository.StationRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class StationServiceImpl implements StationService {

    @Autowired
    private StationRepository repository;

    @Override
    public boolean create(Information info, HttpHeaders headers){
        boolean result = false;
        if(repository.findById(info.getId()) == null){
            Station station = new Station(info.getId(), info.getName());
            station.setStayTime(info.getStayTime());
            repository.save(station);
            result = true;
        }

        return result;
    }

    @Override
    public boolean exist(QueryStation info,HttpHeaders headers){
        boolean result = false;
        if(repository.findByName(info.getName()) != null){
            result = true;
        }
        return result;
    }

    @Override
    public boolean update(Information info,HttpHeaders headers){
        boolean result = false;

        Station station = new Station(info.getId(), info.getName());
        station.setStayTime(info.getStayTime());
        repository.save(station);
        result = true;

        return result;
    }

    @Override
    public boolean delete(Information info,HttpHeaders headers){
        boolean result = false;
        if(repository.findById(info.getId()) != null){
            Station station = new Station(info.getId(),info.getName());
            repository.delete(station);
            result = true;
        }
        return result;
    }

    @Override
    public List<Station> query(HttpHeaders headers){
        return repository.findAll();
    }

    @Override
    public String queryForId(QueryForId info,HttpHeaders headers){
        Station station = repository.findByName(info.getName());
        return station.getId();
    }


    @Override
    public ArrayList<String> queryForIdBatch(QueryForIdBatch queryForIdBatch, HttpHeaders headers) {
        ArrayList<String> result = new ArrayList<>();
        ArrayList<String> nameList = queryForIdBatch.getNameList();
        for(int i = 0; i < nameList.size(); i++) {
            Station station = repository.findByName(nameList.get(i));
            if(station == null) {
                result.add("Not Exist");
            }else{
                result.add(station.getId());
            }
        }
        return result;
    }

    @Override
    public QueryStation queryById(String stationId,HttpHeaders headers){
        Station station = repository.findById(stationId);
        if(station != null){
            return new QueryStation(station.getName());
        }else{
            return new QueryStation("Station Not Found");
        }
    }

    @Override
    public ArrayList<String> queryByIdBatch(QueryByIdBatch queryByIdBatch, HttpHeaders headers) {
        ArrayList<String> result = new ArrayList<>();
        ArrayList<String> idList = queryByIdBatch.getStationIdList();
        for(int i = 0; i < idList.size(); i++) {
            Station station = repository.findById(idList.get(i));
            if(station == null) {
                result.add("Not Exist");
            }else{
                result.add(station.getName());
            }
        }
        return result;
    }
}
