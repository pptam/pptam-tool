package preserve.domain;

public class QueryPriceInfo {

    private String startingPlaceId;

    private String endPlaceId;

    private String trainTypeId;

    private String seatClass;

    public QueryPriceInfo(){
        //Default Constructor
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

}
