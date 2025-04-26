package cancel.service;

import cancel.domain.CalculateRefundResult;
import cancel.domain.CancelOrderInfo;
import cancel.domain.CancelOrderResult;
import org.springframework.http.HttpHeaders;

public interface CancelService {

    CancelOrderResult cancelOrder(CancelOrderInfo info,String loginToken,String loginId, HttpHeaders headers) throws Exception;

    CalculateRefundResult calculateRefund(CancelOrderInfo info, HttpHeaders headers);

}
