package train.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.stereotype.Service;
import train.domain.Information;
import train.domain.Information2;
import train.domain.TrainType;
import train.repository.TrainTypeRepository;
import java.util.List;

@Service
public class TrainServiceImpl implements TrainService {

    @Autowired
    private TrainTypeRepository repository;

    //private static final Logger log = LoggerFactory.getLogger(Application.class);

    public boolean create(Information info, HttpHeaders headers){
        boolean result = false;
        if(repository.findById(info.getId()) == null){
            TrainType type = new TrainType(info.getId(),info.getEconomyClass(),info.getConfortClass());
            type.setAverageSpeed(info.getAverageSpeed());
            repository.save(type);
            result = true;
        }
        return result;
    }

    public TrainType retrieve(Information2 info,HttpHeaders headers){
       if(repository.findById(info.getId()) == null){
           //log.info("ts-train-service:retireve "+id+ " and there is no TrainType with the id:" +id);
           return null;
       }else{
           return repository.findById(info.getId());
       }
    }

    public boolean update(Information info,HttpHeaders headers){
        boolean result = false;
        if(repository.findById(info.getId()) != null){
            TrainType type = new TrainType(info.getId(),info.getEconomyClass(),info.getConfortClass());
            type.setAverageSpeed(info.getAverageSpeed());
            repository.save(type);
            result = true;
        }else{
            TrainType type = new TrainType(info.getId(),info.getEconomyClass(),info.getConfortClass());
            type.setAverageSpeed(info.getAverageSpeed());
            repository.save(type);
            //log.info("ts-train-service:update "+id+ " and there doesn't exist TrainType with the id:" +id);
            //log.info("ts-train-service:update "+id+ " create now!");
            result = true;
        }
        return result;
    }

    public boolean delete(Information2 info,HttpHeaders headers){
        boolean result = false;
        if(repository.findById(info.getId()) == null){
            //log.info("ts-train-service:delete " + id +" and there doesn't exist TrainType with the id:" +id);
        }else{
            repository.deleteById(info.getId());
            result = true;
        }
        return result;
    }

    @Override
    public List<TrainType> query(HttpHeaders headers){
        return repository.findAll();
    }

}
