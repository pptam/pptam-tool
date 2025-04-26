package consign.repository;

import consign.domain.ConsignRecord;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.UUID;

@Repository
public interface ConsignRepository extends MongoRepository<ConsignRecord,String> {
    ArrayList<ConsignRecord> findByAccountId(UUID accountId);

    ArrayList<ConsignRecord> findByConsignee(String consignee);

    ConsignRecord findById(UUID id);
}
