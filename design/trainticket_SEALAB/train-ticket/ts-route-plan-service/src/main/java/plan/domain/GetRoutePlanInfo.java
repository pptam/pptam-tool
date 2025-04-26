package plan.domain;

import java.util.Date;

public class GetRoutePlanInfo {

    private String formStationName;

    private String toStationName;

    private Date travelDate;

    private int num;

    public GetRoutePlanInfo() {
        //Empty Constructor
    }

    public GetRoutePlanInfo(String formStationName, String toStationName, Date travelDate, int num) {
        this.formStationName = formStationName;
        this.toStationName = toStationName;
        this.travelDate = travelDate;
        this.num = num;
    }

    public String getFormStationName() {
        return formStationName;
    }

    public void setFormStationName(String formStationName) {
        this.formStationName = formStationName;
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

    public int getNum() {
        return num;
    }

    public void setNum(int num) {
        this.num = num;
    }
}
