package fdse.microservice.service;

import fdse.microservice.domain.*;
import org.springframework.http.HttpHeaders;

/**
 * Created by Chenjie Xu on 2017/6/6.
 */
public interface BasicService {
    ResultForTravel queryForTravel(QueryForTravel info, HttpHeaders headers);
    String queryForStationId(QueryStation info, HttpHeaders headers);
}
