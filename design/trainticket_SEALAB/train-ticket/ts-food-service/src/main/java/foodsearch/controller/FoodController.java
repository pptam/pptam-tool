package foodsearch.controller;

import foodsearch.domain.*;
import foodsearch.service.FoodService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.List;

@RestController
public class FoodController {

    @Autowired
    FoodService foodService;

    @Autowired
    private RestTemplate restTemplate;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home() {
        return "Welcome to [ Food Service ] !";
    }

    @RequestMapping(path = "/food/getFood", method = RequestMethod.POST)
    public GetAllFoodOfTripResult getFood(@RequestBody GetAllFoodOfTripInfo gati, @RequestHeader HttpHeaders headers){
        System.out.println("[Food Service]Get the Get Food Request!");
        return foodService.getAllFood(gati.getDate(), gati.getStartStation(), gati.getEndStation(), gati.getTripId(), headers);
    }

    @RequestMapping(path = "/food/createFoodOrder", method = RequestMethod.POST)
    public AddFoodOrderResult createFoodOrder(@RequestBody AddFoodOrderInfo afoi, @RequestHeader HttpHeaders headers){
        System.out.println("[Food Service]Try to Create a FoodOrder!");
        return foodService.createFoodOrder(afoi, headers);
    }

    @RequestMapping(path = "/food/cancelFoodOrder", method = RequestMethod.POST)
    public CancelFoodOrderResult cancelFoodOrder(@RequestBody CancelFoodOrderInfo cfoi, @RequestHeader HttpHeaders headers){
        System.out.println("[Food Service]Try to Cancel a FoodOrder!");
        return foodService.cancelFoodOrder(cfoi, headers);
    }

    @RequestMapping(path = "/food/updateFoodOrder", method = RequestMethod.POST)
    public UpdateFoodOrderResult updateFoodOrder(@RequestBody UpdateFoodOrderInfo ufoi, @RequestHeader HttpHeaders headers){
        System.out.println("[Food Service]Try to Update a FoodOrder!");
        return foodService.updateFoodOrder(ufoi, headers);
    }

    @RequestMapping(path = "/food/findAllFoodOrder", method = RequestMethod.GET)
    public List<FoodOrder> findAllFoodOrder(@RequestHeader HttpHeaders headers){
        System.out.println("[Food Service]Try to Find all FoodOrder!");
        return foodService.findAllFoodOrder(headers);
    }

    @RequestMapping(path = "/food/findFoodOrderByOrderId", method = RequestMethod.POST)
    public FindByOrderIdResult findFoodOrderByOrderId(@RequestBody FindByOrderIdInfo foi, @RequestHeader HttpHeaders headers){
        System.out.println("[Food Service]Try to Find all FoodOrder!");
        return foodService.findByOrderId(foi.getOrderId(), headers);
    }

}
