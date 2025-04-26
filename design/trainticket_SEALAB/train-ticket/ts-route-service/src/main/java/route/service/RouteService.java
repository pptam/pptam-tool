package route.service;

import org.springframework.http.HttpHeaders;
import route.domain.*;

public interface RouteService {

    GetRoutesListlResult getRouteByStartAndTerminal(GetRouteByStartAndTerminalInfo info,HttpHeaders headers);

    GetRoutesListlResult getAllRoutes(HttpHeaders headers);

    GetRouteByIdResult getRouteById(String routeId,HttpHeaders headers);

    DeleteRouteResult deleteRoute(DeleteRouteInfo info,HttpHeaders headers);

    CreateAndModifyRouteResult createAndModify(CreateAndModifyRouteInfo info,HttpHeaders headers);

}
