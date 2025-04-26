package adminbasic.domin.reuslt;

import adminbasic.domin.bean.Station;

import java.util.List;

public class GetAllStationResult {

    private boolean status;

    private String message;

    private List<Station> stationList;

    public List<Station> getStationList() {
        return stationList;
    }

    public void setStationList(List<Station> stationList) {
        this.stationList = stationList;
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
