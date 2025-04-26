package assurance.repository;

import assurance.domain.Assurance;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.stereotype.Repository;
import java.util.ArrayList;
import java.util.UUID;

@Repository
public interface AssuranceRepository  extends MongoRepository<Assurance, String> {

    Assurance findById(UUID id);

    @Query("{ 'orderId' : ?0 }")
    Assurance findByOrderId(UUID orderId);

    void deleteById(UUID id);

    void removeAssuranceByOrderId(UUID orderId);

    ArrayList<Assurance> findAll();
}
