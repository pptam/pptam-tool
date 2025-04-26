package travel.domain;

import java.util.Date;

public class QuerySoldTicket {

    private Date travelDate;

    private String trainNumber;

    public QuerySoldTicket(){
        //Default Constructor
    }

    public QuerySoldTicket(Date travelDate, String trainNumber) {
        this.travelDate = travelDate;
        this.trainNumber = trainNumber;
    }

    public Date getTravelDate() {
        return travelDate;
    }

    public void setTravelDate(Date travelDate) {
        this.travelDate = travelDate;
    }

    public String getTrainNumber() {
        return trainNumber;
    }

    public void setTrainNumber(String trainNumber) {
        this.trainNumber = trainNumber;
    }
}
