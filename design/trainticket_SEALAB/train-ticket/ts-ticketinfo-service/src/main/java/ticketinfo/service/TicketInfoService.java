package ticketinfo.service;

import org.springframework.http.HttpHeaders;
import ticketinfo.domain.QueryForStationId;
import ticketinfo.domain.QueryForTravel;
import ticketinfo.domain.ResultForTravel;

/**
 * Created by Chenjie Xu on 2017/6/6.
 */
public interface TicketInfoService {
    ResultForTravel queryForTravel(QueryForTravel info,HttpHeaders headers);
    String queryForStationId(QueryForStationId info,HttpHeaders headers);
}
