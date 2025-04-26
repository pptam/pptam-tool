package preserveOther.service;

import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.RequestHeader;
import preserveOther.domain.OrderTicketsInfo;
import preserveOther.domain.OrderTicketsResult;

public interface PreserveOtherService {

    OrderTicketsResult preserve(OrderTicketsInfo oti,String accountId,String loginToken, HttpHeaders headers);

}
