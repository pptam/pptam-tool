package travel2.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.*;
import travel2.domain.*;
import travel2.service.Travel2Service;
import java.util.ArrayList;
import java.util.List;

@RestController
public class Travel2Controller {

    @Autowired
    private Travel2Service service;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home(@RequestHeader HttpHeaders headers) {
        return "Welcome to [ Travle2 Service ] !";
    }

    @RequestMapping(value="/travel2/getTrainTypeByTripId/{tripId}", method = RequestMethod.GET)
    public GetTrainTypeResult getTrainTypeByTripId(@PathVariable String tripId,@RequestHeader HttpHeaders headers){
        return service.getTrainTypeByTripId(tripId, headers);
    }

    @RequestMapping(value = "/travel2/getRouteByTripId/{tripId}", method = RequestMethod.GET)
    public GetRouteResult getRouteByTripId(@PathVariable String tripId,@RequestHeader HttpHeaders headers){
        System.out.println("[Get Route By Trip ID] TripId:" + tripId);
        return service.getRouteByTripId(tripId, headers);
    }

    @RequestMapping(value = "/travel2/getTripsByRouteId", method = RequestMethod.POST)
    public GetTripsByRouteIdResult getTripsByRouteId(@RequestBody GetTripsByRouteIdInfo info, @RequestHeader HttpHeaders headers){
        return service.getTripByRoute(info, headers);
    }


    @RequestMapping(value="/travel2/create", method= RequestMethod.POST)
    public String create(@RequestBody Information info, @RequestHeader HttpHeaders headers){
        return service.create(info, headers);
    }

    //只返回Trip，不会返回票数信息
    @RequestMapping(value="/travel2/retrieve", method= RequestMethod.POST)
    public Trip retrieve(@RequestBody Information2 info, @RequestHeader HttpHeaders headers){
        return service.retrieve(info, headers);
    }

    @RequestMapping(value="/travel2/update", method= RequestMethod.POST)
    public String update(@RequestBody Information info, @RequestHeader HttpHeaders headers){
        return service.update(info, headers);
    }

    @RequestMapping(value="/travel2/delete", method= RequestMethod.POST)
    public String delete(@RequestBody Information2 info, @RequestHeader HttpHeaders headers){
        return service.delete(info, headers);
    }

    //返回Trip以及剩余票数
    @RequestMapping(value="/travel2/query", method= RequestMethod.POST)
    public ArrayList<TripResponse> query(@RequestBody QueryInfo info,@RequestHeader HttpHeaders headers){
        if(info.getStartingPlace() == null || info.getStartingPlace().length() == 0 ||
                info.getEndPlace() == null || info.getEndPlace().length() == 0 ||
                info.getDepartureTime() == null){
            System.out.println("[Travel Other Service][Travel Query] Fail.Something null.");
            ArrayList<TripResponse> errorList = new ArrayList<>();
            return errorList;
        }
        System.out.println("[Travel2 Service] Query TripResponse");
        return service.query(info,headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(value="/travel2/queryWithPackage", method= RequestMethod.POST)
    public QueryTripResponsePackage queryPackage(@RequestBody QueryInfo info,@RequestHeader HttpHeaders headers){
        if(info.getStartingPlace() == null || info.getStartingPlace().length() == 0 ||
                info.getEndPlace() == null || info.getEndPlace().length() == 0 ||
                info.getDepartureTime() == null){
            System.out.println("[Travel Other Service][Travel Query] Fail.Something null.");
            ArrayList<TripResponse> errorList = new ArrayList<>();
            return new QueryTripResponsePackage(false,"Fail.",errorList);
        }
        System.out.println("[Travel Other Servicee] Query TripResponse");
        ArrayList<TripResponse> responses = service.query(info,headers);
        return new QueryTripResponsePackage(true,"Success.",responses);
    }

    //返回Trip以及剩余票数
    @CrossOrigin(origins = "*")
    @RequestMapping(value="/travel2/getTripAllDetailInfo", method= RequestMethod.POST)
    public GetTripAllDetailResult getTripAllDetailInfo(@RequestBody GetTripAllDetailInfo gtdi,@RequestHeader HttpHeaders headers){
        return service.getTripAllDetailInfo(gtdi,headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(value="/travel2/queryAll", method= RequestMethod.GET)
    public List<Trip> queryAll(@RequestHeader HttpHeaders headers){
        return service.queryAll(headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(value="/travel2/adminQueryAll", method= RequestMethod.GET)
    public AdminFindAllResult adminQueryAll(@RequestHeader HttpHeaders headers){
        return service.adminQueryAll(headers);
    }
}
