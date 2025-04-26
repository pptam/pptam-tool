package travelplan.domain;

import java.util.Date;

public class TransferTravelSearchInfo {

    private String fromStationName;

    private String viaStationName;

    private String toStationName;

    private Date travelDate;

    private String trainType;

    public TransferTravelSearchInfo() {
        //Empty Constructor
    }

    public TransferTravelSearchInfo(String fromStationName, String viaStationName, String toStationName, Date travelDate, String trainType) {
        this.fromStationName = fromStationName;
        this.viaStationName = viaStationName;
        this.toStationName = toStationName;
        this.travelDate = travelDate;
        this.trainType = trainType;
    }

    public String getFromStationName() {
        return fromStationName;
    }

    public void setFromStationName(String fromStationName) {
        this.fromStationName = fromStationName;
    }

    public String getViaStationName() {
        return viaStationName;
    }

    public void setViaStationName(String viaStationName) {
        this.viaStationName = viaStationName;
    }

    public String getToStationName() {
        return toStationName;
    }

    public void setToStationName(String toStationName) {
        this.toStationName = toStationName;
    }

    public Date getTravelDate() {
        return travelDate;
    }

    public void setTravelDate(Date travelDate) {
        this.travelDate = travelDate;
    }

    public String getTrainType() {
        return trainType;
    }

    public void setTrainType(String trainType) {
        this.trainType = trainType;
    }
}
