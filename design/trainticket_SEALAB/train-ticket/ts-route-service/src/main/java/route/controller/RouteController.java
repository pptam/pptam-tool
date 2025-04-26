package route.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.*;
import route.domain.*;
import route.service.RouteService;

@RestController
public class RouteController {

    @Autowired
    private RouteService routeService;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home() {
        return "Welcome to [ Route Service ] !";
    }

    @RequestMapping(path = "/route/createAndModify", method = RequestMethod.POST)
    public CreateAndModifyRouteResult createAndModifyRoute(@RequestBody CreateAndModifyRouteInfo createAndModifyRouteInfo,@RequestHeader HttpHeaders headers){
        return routeService.createAndModify(createAndModifyRouteInfo, headers);
    }

    @RequestMapping(path = "/route/delete", method = RequestMethod.POST)
    public DeleteRouteResult deleteRoute(@RequestBody DeleteRouteInfo deleteRouteInfo,@RequestHeader HttpHeaders headers){
        return routeService.deleteRoute(deleteRouteInfo, headers);
    }

    @RequestMapping(path = "/route/queryById/{routeId}", method = RequestMethod.GET)
    public GetRouteByIdResult queryById(@PathVariable String routeId,@RequestHeader HttpHeaders headers){
        return routeService.getRouteById(routeId, headers);
    }

    @RequestMapping(path = "/route/queryAll", method = RequestMethod.GET)
    public GetRoutesListlResult queryAll(@RequestHeader HttpHeaders headers){
        return routeService.getAllRoutes(headers);
    }

    @RequestMapping(path = "/route/queryByStartAndTerminal", method = RequestMethod.POST)
    public GetRoutesListlResult queryByStartAndTerminal(@RequestBody GetRouteByStartAndTerminalInfo getRouteByStartAndTerminalInfo,@RequestHeader HttpHeaders headers){
        return routeService.getRouteByStartAndTerminal(getRouteByStartAndTerminalInfo, headers);
    }

}