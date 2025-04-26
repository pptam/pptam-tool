package fdse.microservice.domain;

import javax.management.Query;


public class QueryPriceInfo {
    private String startingPlaceId;
    private String endPlaceId;
    private String trainTypeId;
    private String seatClass;

    public QueryPriceInfo(){}



    public String getTrainTypeId() {
        return trainTypeId;
    }

    public void setTrainTypeId(String trainTypeId) {
        this.trainTypeId = trainTypeId;
    }

    public String getSeatClass() {
        return seatClass;
    }

    public void setSeatClass(String seatClass) {
        this.seatClass = seatClass;
    }

    public String getStartingPlaceId() {
        return startingPlaceId;
    }

    public void setStartingPlaceId(String startingPlaceId) {
        this.startingPlaceId = startingPlaceId;
    }

    public String getEndPlaceId() {
        return endPlaceId;
    }

    public void setEndPlaceId(String endPlaceId) {
        this.endPlaceId = endPlaceId;
    }
}
