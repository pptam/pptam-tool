package travelplan.domain;

import java.util.ArrayList;

public class TravelAdvanceResult {

    private boolean status;

    private String message;

    private ArrayList<TravelAdvanceResultUnit> travelAdvanceResultUnits;

    public TravelAdvanceResult() {
        //Default Constructor
    }

    public TravelAdvanceResult(boolean status, String message, ArrayList<TravelAdvanceResultUnit> travelAdvanceResultUnits) {
        this.status = status;
        this.message = message;
        this.travelAdvanceResultUnits = travelAdvanceResultUnits;
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

    public ArrayList<TravelAdvanceResultUnit> getTravelAdvanceResultUnits() {
        return travelAdvanceResultUnits;
    }

    public void setTravelAdvanceResultUnits(ArrayList<TravelAdvanceResultUnit> travelAdvanceResultUnits) {
        this.travelAdvanceResultUnits = travelAdvanceResultUnits;
    }
}
