package admintravel.controller;

import admintravel.domain.request.AddAndModifyTravelRequest;
import admintravel.domain.request.DeleteTravelRequest;
import admintravel.domain.response.AdminFindAllResult;
import admintravel.domain.response.ResponseBean;
import admintravel.service.AdminTravelService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.*;

@RestController
public class AdminTravelController {
    @Autowired
    AdminTravelService adminTravelService;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home(@RequestHeader HttpHeaders headers) {
        return "Welcome to [ AdminTravel Service ] !";
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/admintravel/findAll/{id}", method = RequestMethod.GET)
    public AdminFindAllResult getAllTravels(@PathVariable String id, @RequestHeader HttpHeaders headers){
        return adminTravelService.getAllTravels(id, headers);
    }

    @RequestMapping(value = "/admintravel/addTravel", method= RequestMethod.POST)
    public ResponseBean addTravel(@RequestBody AddAndModifyTravelRequest request, @RequestHeader HttpHeaders headers){
        return adminTravelService.addTravel(request, headers);
    }

    @RequestMapping(value = "/admintravel/updateTravel", method= RequestMethod.POST)
    public ResponseBean updateTravel(@RequestBody AddAndModifyTravelRequest request, @RequestHeader HttpHeaders headers){
        return adminTravelService.updateTravel(request, headers);
    }

    @RequestMapping(value = "/admintravel/deleteTravel", method= RequestMethod.POST)
    public ResponseBean deleteTravel(@RequestBody DeleteTravelRequest request, @RequestHeader HttpHeaders headers){
        return adminTravelService.deleteTravel(request, headers);
    }
}
