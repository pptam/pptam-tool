package train.service;

import org.springframework.http.HttpHeaders;
import train.domain.Information;
import train.domain.Information2;
import train.domain.TrainType;

import java.util.List;

public interface TrainService {
    //CRUD
    boolean create(Information info, HttpHeaders headers);

    TrainType retrieve(Information2 info,HttpHeaders headers);

    boolean update(Information info,HttpHeaders headers);

    boolean delete(Information2 info,HttpHeaders headers);

    List<TrainType> query(HttpHeaders headers);
}
