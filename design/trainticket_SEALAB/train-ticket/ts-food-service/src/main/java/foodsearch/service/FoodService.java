package foodsearch.service;

import foodsearch.domain.*;
import org.springframework.http.HttpHeaders;

import java.util.List;

public interface FoodService {

    GetAllFoodOfTripResult getAllFood(String date, String startStation, String endStation, String tripId, HttpHeaders headers);

    AddFoodOrderResult createFoodOrder(AddFoodOrderInfo afoi, HttpHeaders headers);

    CancelFoodOrderResult cancelFoodOrder(CancelFoodOrderInfo cfoi, HttpHeaders headers);

    UpdateFoodOrderResult updateFoodOrder(UpdateFoodOrderInfo ufoi, HttpHeaders headers);

    List<FoodOrder> findAllFoodOrder(HttpHeaders headers);

    FindByOrderIdResult findByOrderId(String orderId, HttpHeaders headers);
}
