package travelplan.domain;

import java.util.ArrayList;
import java.util.Date;

public class TravelAdvanceResultUnit {

    private String tripId;

    private String trainTypeId;

    private String fromStationName;

    private String toStationName;

    private ArrayList<String> stopStations;

    private String priceForSecondClassSeat;

    private int numberOfRestTicketSecondClass;

    private String priceForFirstClassSeat;

    private int numberOfRestTicketFirstClass;

    private Date startingTime;

    private Date endTime;

    public TravelAdvanceResultUnit() {
        //Default Constructor
    }

    public String getTripId() {
        return tripId;
    }

    public void setTripId(String tripId) {
        this.tripId = tripId;
    }

    public String getTrainTypeId() {
        return trainTypeId;
    }

    public void setTrainTypeId(String trainTypeId) {
        this.trainTypeId = trainTypeId;
    }

    public String getFromStationName() {
        return fromStationName;
    }

    public void setFromStationName(String fromStationName) {
        this.fromStationName = fromStationName;
    }

    public String getToStationName() {
        return toStationName;
    }

    public void setToStationName(String toStationName) {
        this.toStationName = toStationName;
    }

    public ArrayList<String> getStopStations() {
        return stopStations;
    }

    public void setStopStations(ArrayList<String> stopStations) {
        this.stopStations = stopStations;
    }

    public String getPriceForSecondClassSeat() {
        return priceForSecondClassSeat;
    }

    public void setPriceForSecondClassSeat(String priceForSecondClassSeat) {
        this.priceForSecondClassSeat = priceForSecondClassSeat;
    }

    public int getNumberOfRestTicketSecondClass() {
        return numberOfRestTicketSecondClass;
    }

    public void setNumberOfRestTicketSecondClass(int numberOfRestTicketSecondClass) {
        this.numberOfRestTicketSecondClass = numberOfRestTicketSecondClass;
    }

    public String getPriceForFirstClassSeat() {
        return priceForFirstClassSeat;
    }

    public void setPriceForFirstClassSeat(String priceForFirstClassSeat) {
        this.priceForFirstClassSeat = priceForFirstClassSeat;
    }

    public int getNumberOfRestTicketFirstClass() {
        return numberOfRestTicketFirstClass;
    }

    public void setNumberOfRestTicketFirstClass(int numberOfRestTicketFirstClass) {
        this.numberOfRestTicketFirstClass = numberOfRestTicketFirstClass;
    }

    public Date getStartingTime() {
        return startingTime;
    }

    public void setStartingTime(Date startingTime) {
        this.startingTime = startingTime;
    }

    public Date getEndTime() {
        return endTime;
    }

    public void setEndTime(Date endTime) {
        this.endTime = endTime;
    }
}
