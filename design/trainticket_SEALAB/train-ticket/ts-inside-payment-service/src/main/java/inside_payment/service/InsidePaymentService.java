package inside_payment.service;

import inside_payment.domain.*;
import org.springframework.http.HttpHeaders;

import javax.servlet.http.HttpServletRequest;
import java.util.List;

/**
 * Created by Administrator on 2017/6/20.
 */
public interface InsidePaymentService {

    boolean pay(PaymentInfo info, HttpServletRequest request, HttpHeaders headers);

    boolean createAccount(CreateAccountInfo info, HttpHeaders headers);

    boolean addMoney(AddMoneyInfo info, HttpHeaders headers);

    List<Payment> queryPayment(HttpHeaders headers);

    List<Balance> queryAccount(HttpHeaders headers);

    boolean drawBack(DrawBackInfo info, HttpHeaders headers);

    boolean payDifference(PaymentDifferenceInfo info, HttpServletRequest request, HttpHeaders headers);

    List<AddMoney> queryAddMoney(HttpHeaders headers);

    void initPayment(Payment payment, HttpHeaders headers);

}
