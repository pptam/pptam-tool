package price.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.stereotype.Repository;
import price.domain.PriceConfig;
import java.util.ArrayList;
import java.util.UUID;

@Repository
public interface PriceConfigRepository extends MongoRepository<PriceConfig, String> {

    @Query("{ 'id': ?0 }")
    PriceConfig findById(UUID id);

    @Query("{ 'routeId': ?0 , 'trainType': ?1 }")
    PriceConfig findByRouteIdAndTrainType(String routeId,String trainType);

    ArrayList<PriceConfig> findAll();

}
