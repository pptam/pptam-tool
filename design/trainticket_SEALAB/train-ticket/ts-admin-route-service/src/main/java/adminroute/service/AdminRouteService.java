package adminroute.service;

import adminroute.domain.request.CreateAndModifyRouteRequest;
import adminroute.domain.request.DeleteRouteRequest;
import adminroute.domain.response.CreateAndModifyRouteResult;
import adminroute.domain.response.DeleteRouteResult;
import adminroute.domain.response.GetRoutesListlResult;
import org.springframework.http.HttpHeaders;

public interface AdminRouteService {
    GetRoutesListlResult getAllRoutes(String id, HttpHeaders headers);
    CreateAndModifyRouteResult createAndModifyRoute(CreateAndModifyRouteRequest request, HttpHeaders headers);
    DeleteRouteResult deleteRoute(DeleteRouteRequest request, HttpHeaders headers);
}
