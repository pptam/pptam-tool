package foodsearch.domain;

import java.util.List;

public class GetFoodStoresListResult {

    private boolean status;

    private String message;

    private List<FoodStore> foodStoreList;

    public GetFoodStoresListResult(){

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

    public List<FoodStore> getFoodStoreList() {
        return foodStoreList;
    }

    public void setFoodStoreList(List<FoodStore> foodStoreList) {
        this.foodStoreList = foodStoreList;
    }


}
