package travelplan.service;

import org.springframework.http.HttpHeaders;
import travelplan.domain.*;

public interface TravelPlanService {

    TransferTravelSearchResult getTransferSearch(TransferTravelSearchInfo info, HttpHeaders headers);

    TravelAdvanceResult getCheapest(QueryInfo info, HttpHeaders headers);

    TravelAdvanceResult getQuickest(QueryInfo info, HttpHeaders headers);

    TravelAdvanceResult getMinStation(QueryInfo info, HttpHeaders headers);

}
