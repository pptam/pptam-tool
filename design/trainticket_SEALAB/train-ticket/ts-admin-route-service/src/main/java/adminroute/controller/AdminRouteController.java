package adminroute.controller;

import adminroute.domain.request.CreateAndModifyRouteRequest;
import adminroute.domain.request.DeleteRouteRequest;
import adminroute.domain.response.CreateAndModifyRouteResult;
import adminroute.domain.response.DeleteRouteResult;
import adminroute.domain.response.GetRoutesListlResult;
import adminroute.service.AdminRouteService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.*;

@RestController
public class AdminRouteController {
    @Autowired
    AdminRouteService adminRouteService;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home(@RequestHeader HttpHeaders headers) {
        return "Welcome to [ AdminRoute Service ] !";
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/adminroute/findAll/{id}", method = RequestMethod.GET)
    public GetRoutesListlResult getAllRoutes(@PathVariable String id, @RequestHeader HttpHeaders headers){
        return adminRouteService.getAllRoutes(id, headers);
    }

    @RequestMapping(value = "/adminroute/createAndModifyRoute", method= RequestMethod.POST)
    public CreateAndModifyRouteResult addRoute(@RequestBody CreateAndModifyRouteRequest request, @RequestHeader HttpHeaders headers){
        return adminRouteService.createAndModifyRoute(request, headers);
    }

    @RequestMapping(value = "/adminroute/deleteRoute", method= RequestMethod.POST)
    public DeleteRouteResult deleteRoute(@RequestBody DeleteRouteRequest request, @RequestHeader HttpHeaders headers){
        return adminRouteService.deleteRoute(request, headers);
    }
}
