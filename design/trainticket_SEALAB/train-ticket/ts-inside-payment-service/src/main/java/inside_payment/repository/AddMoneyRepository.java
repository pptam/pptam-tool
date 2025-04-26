package inside_payment.repository;

import inside_payment.domain.AddMoney;
import org.springframework.data.repository.CrudRepository;

import java.util.List;


public interface AddMoneyRepository extends CrudRepository<AddMoney,String> {
    List<AddMoney> findByUserId(String userId);
    List<AddMoney> findAll();
}
