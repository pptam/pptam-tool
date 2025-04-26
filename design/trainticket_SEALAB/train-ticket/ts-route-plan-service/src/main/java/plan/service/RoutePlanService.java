package plan.service;

import org.springframework.http.HttpHeaders;
import plan.domain.GetRoutePlanInfo;
import plan.domain.RoutePlanResults;

public interface RoutePlanService {

    RoutePlanResults searchCheapestResult(GetRoutePlanInfo info,HttpHeaders headers);

    RoutePlanResults searchQuickestResult(GetRoutePlanInfo info,HttpHeaders headers);

    RoutePlanResults searchMinStopStations(GetRoutePlanInfo info,HttpHeaders headers);

}
