package security.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.stereotype.Repository;
import security.domain.SecurityConfig;
import java.util.ArrayList;
import java.util.UUID;

@Repository
public interface SecurityRepository extends MongoRepository<SecurityConfig,String>{

    @Query("{ 'name': ?0 }")
    SecurityConfig findByName(String name);

    @Query("{ 'id': ?0 }")
    SecurityConfig findById(UUID id);

    ArrayList<SecurityConfig> findAll();

    void deleteById(UUID id);
}
