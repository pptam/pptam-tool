package other.domain;

import java.util.Date;

public class CalculateSoldTicketInfo {

    private Date travelDate;

    private String trainNumber;

    public Date getTravelDate() {
        return travelDate;
    }

    public void setTravelDate(int year,int month,int day){
        Date date = new Date(year,month,day,0,0,0);
        this.travelDate = date;
    }

    public String getTrainNumber() {
        return trainNumber;
    }

    public void setTrainNumber(String trainNumber) {
        this.trainNumber = trainNumber;
    }
}
