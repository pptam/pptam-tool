package food.domain;

import java.util.List;

public class GetTrainFoodListResult {

    private boolean status;

    private String message;

    private List<TrainFood> trainFoodList;

    public GetTrainFoodListResult(){

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

}
