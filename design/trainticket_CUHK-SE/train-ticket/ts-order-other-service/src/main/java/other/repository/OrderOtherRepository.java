package other.repository;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import other.entity.Order;
import org.springframework.stereotype.Repository;
import java.util.ArrayList;
import java.util.Date;
import java.util.Optional;
import java.util.UUID;

/**
 * @author fdse
 */
@Repository
public interface OrderOtherRepository extends CrudRepository<Order, String> {

    /**
     * find order by id
     *
     * @param id id
     * @return Order
     */
//    @Query("{ 'id': ?0 }")
    @Override
    Optional<Order> findById(String id);

    /**
     * find all orders
     *
     * @return ArrayList<Order>
     */
    @Override
    ArrayList<Order> findAll();

    /**
     * find orders by account id
     *
     * @param accountId account id
     * @return ArrayList<Order>
     */
//    @Query("{ 'accountId' : ?0 }")
    ArrayList<Order> findByAccountId(String accountId);

    /**
     * find orders by travel date and train number
     *
     * @param travelDate travel date
     * @param trainNumber train number
     * @return ArrayList<Order>
     */
//    @Query("{ 'travelDate' : ?0 , trainNumber : ?1 }")
    ArrayList<Order> findByTravelDateAndTrainNumber(String travelDate, String trainNumber);

    /**
     * delete order by id
     *
     * @param id id
     * @return null
     */
    @Override
    void deleteById(String id);
}
