package food.repository;


import food.domain.TrainFood;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface TrainFoodRepository extends MongoRepository<TrainFood, String> {

    TrainFood findById(UUID id);

    List<TrainFood> findAll();

    @Query("{ 'tripId' : ?0 }")
    List<TrainFood> findByTripId(String tripId);

    void deleteById(UUID id);
}
