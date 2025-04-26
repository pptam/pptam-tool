package order.repository;

import order.entity.Order;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.ArrayList;
import java.util.Date;
import java.util.Optional;
import java.util.UUID;
import java.util.List;

/**
 * @author fdse
 */
@Repository
public interface OrderRepository extends JpaRepository<Order, String> {

    @Override
    Optional<Order> findById(String id);

    @Override
    ArrayList<Order> findAll();

    ArrayList<Order> findByAccountId(String accountId);

    ArrayList<Order> findByTravelDateAndTrainNumber(String travelDate, String trainNumber);
    
    // New method for checking duplicate orders
    ArrayList<Order> findByAccountIdAndTrainNumberAndTravelDate(String accountId, String trainNumber, String travelDate);
    
    // Method for filtered queries
    @Query("SELECT o FROM Order o WHERE o.accountId = :accountId " +
           "AND (:status IS NULL OR o.status = :status) " +
           "AND (:boughtDateStart IS NULL OR o.boughtDate >= :boughtDateStart) " +
           "AND (:boughtDateEnd IS NULL OR o.boughtDate <= :boughtDateEnd) " +
           "AND (:travelDateStart IS NULL OR o.travelDate >= :travelDateStart) " +
           "AND (:travelDateEnd IS NULL OR o.travelDate <= :travelDateEnd)")
    ArrayList<Order> findOrdersWithFilters(
            @Param("accountId") String accountId,
            @Param("status") Integer status,
            @Param("boughtDateStart") String boughtDateStart,
            @Param("boughtDateEnd") String boughtDateEnd,
            @Param("travelDateStart") String travelDateStart,
            @Param("travelDateEnd") String travelDateEnd);
    
    // Methods for counting
    @Query("SELECT COUNT(o) FROM Order o WHERE o.accountId = :accountId AND o.boughtDate > :boughtDate")
    int countOrdersAfterTime(@Param("accountId") String accountId, @Param("boughtDate") String boughtDate);
    
    @Query("SELECT COUNT(o) FROM Order o WHERE o.accountId = :accountId AND o.status IN :statuses")
    int countOrdersByAccountIdAndStatusIn(@Param("accountId") String accountId, @Param("statuses") List<Integer> statuses);
    
    // Method for sold tickets aggregation
    @Query("SELECT o.seatClass, COUNT(o) FROM Order o " +
           "WHERE o.travelDate = :travelDate AND o.trainNumber = :trainNumber " +
           "AND o.status < :changeStatus GROUP BY o.seatClass")
    List<Object[]> countSeatClassesByTravelDateAndTrainNumber(
            @Param("travelDate") String travelDate, 
            @Param("trainNumber") String trainNumber,
            @Param("changeStatus") int changeStatus);

    @Override
    void deleteById(String id);
}
