package train.repository;

import org.springframework.data.repository.CrudRepository;
import train.domain.TrainType;

import java.util.List;


public interface TrainTypeRepository extends CrudRepository<TrainType,String>{

    TrainType findById(String id);
    List<TrainType> findAll();
    //void save(TrainType trainType);
    void deleteById(String id);
    //void update();
}
