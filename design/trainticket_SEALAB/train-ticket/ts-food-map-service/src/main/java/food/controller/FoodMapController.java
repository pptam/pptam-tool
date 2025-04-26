package food.controller;

import food.domain.GetFoodStoresListResult;
import food.domain.GetTrainFoodListResult;
import food.domain.QueryFoodStoresInfo;
import food.domain.QueryTrainFoodInfo;
import food.service.FoodMapService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.HttpHeaders;

@RestController
public class FoodMapController {

    @Autowired
    FoodMapService foodMapService;

    @Autowired
    private RestTemplate restTemplate;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home() {
        return "Welcome to [ Food Map Service ] !";
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/foodmap/getAllFoodStores", method = RequestMethod.GET)
    public GetFoodStoresListResult getAllFoodStores(@RequestHeader HttpHeaders headers){
        System.out.println("[Food Map Service][Get All FoodStores]");
        return foodMapService.listFoodStores(headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/foodmap/getAllTrainFood", method = RequestMethod.GET)
    public GetTrainFoodListResult getAllTrainFood(@RequestHeader HttpHeaders headers){
        System.out.println("[Food Map Service][Get All TrainFoods]");
        return foodMapService.listTrainFood(headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/foodmap/getFoodStoresOfStation", method = RequestMethod.POST)
    public GetFoodStoresListResult getFoodStoresOfStation(@RequestBody QueryFoodStoresInfo qfs, @RequestHeader HttpHeaders headers){
        System.out.println("[Food Map Service][Get FoodStores By StationId]");
        return foodMapService.listFoodStoresByStationId(qfs.getStationId(),headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/foodmap/getTrainFoodOfTrip", method = RequestMethod.POST)
    public GetTrainFoodListResult getTrainFoodOfTrip(@RequestBody QueryTrainFoodInfo qtf, @RequestHeader HttpHeaders headers){
        System.out.println("[Food Map Service][Get TrainFoods By TripId]");
        return foodMapService.listTrainFoodByTripId(qtf.getTripId(),headers);
    }


}
