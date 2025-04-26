package foodsearch.domain;

import java.util.List;
import java.util.Map;

public class GetAllFoodOfTripResult {

    boolean status;

    private String message;

    private List<TrainFood> trainFoodList;

    private Map<String, List<FoodStore>>  foodStoreListMap;

    public GetAllFoodOfTripResult(){

    }

    public boolean isStatus() {
        return status;
    }

    public void setStatus(boolean status) {
        this.status = status;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public List<TrainFood> getTrainFoodList() {
        return trainFoodList;
    }

    public void setTrainFoodList(List<TrainFood> trainFoodList) {
        this.trainFoodList = trainFoodList;
    }

    public Map<String, List<FoodStore>> getFoodStoreListMap() {
        return foodStoreListMap;
    }

    public void setFoodStoreListMap(Map<String, List<FoodStore>> foodStoreListMap) {
        this.foodStoreListMap = foodStoreListMap;
    }

}
