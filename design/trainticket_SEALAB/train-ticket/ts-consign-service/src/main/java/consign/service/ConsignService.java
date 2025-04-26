package consign.service;

import consign.domain.ConsignRecord;
import consign.domain.ConsignRequest;
import consign.domain.InsertConsignRecordResult;
import org.springframework.http.HttpHeaders;

import java.util.ArrayList;
import java.util.UUID;

public interface ConsignService {
    InsertConsignRecordResult insertConsignRecord(ConsignRequest consignRequest, HttpHeaders headers);
    boolean updateConsignRecord(ConsignRequest consignRequest, HttpHeaders headers);
    ArrayList<ConsignRecord> queryByAccountId(UUID accountId, HttpHeaders headers);
    ArrayList<ConsignRecord> queryByConsignee(String consignee, HttpHeaders headers);
}
