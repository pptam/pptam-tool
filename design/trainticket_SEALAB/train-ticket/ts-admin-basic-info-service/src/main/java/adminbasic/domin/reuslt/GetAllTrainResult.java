package adminbasic.domin.reuslt;

import adminbasic.domin.bean.TrainType;

import java.util.List;

public class GetAllTrainResult {

    private boolean status;

    private String message;

    private List<TrainType> trainList;

    public List<TrainType> getTrainList() {
        return trainList;
    }

    public void setTrainList(List<TrainType> trainList) {
        this.trainList = trainList;
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


}
