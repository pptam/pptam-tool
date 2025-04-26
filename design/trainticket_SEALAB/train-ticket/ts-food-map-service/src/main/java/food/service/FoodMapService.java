package food.service;

import food.domain.*;
import org.springframework.http.HttpHeaders;

public interface FoodMapService {

    FoodStore createFoodStore(FoodStore fs, HttpHeaders headers);

    TrainFood createTrainFood(TrainFood tf, HttpHeaders headers);

    GetFoodStoresListResult listFoodStores(HttpHeaders headers);

    GetTrainFoodListResult listTrainFood(HttpHeaders headers);

    GetFoodStoresListResult listFoodStoresByStationId(String stationId, HttpHeaders headers);

    GetTrainFoodListResult listTrainFoodByTripId(String tripId, HttpHeaders headers);



}
