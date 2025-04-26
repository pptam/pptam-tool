package consignprice.repository;

import consignprice.domain.PriceConfig;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.stereotype.Repository;


@Repository
public interface ConsignPriceConfigRepository extends MongoRepository<PriceConfig, String> {
    @Query("{ 'index': ?0 }")
    PriceConfig findByIndex(int index);

}
