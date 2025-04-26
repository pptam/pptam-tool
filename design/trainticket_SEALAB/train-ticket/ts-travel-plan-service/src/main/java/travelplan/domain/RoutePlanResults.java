package travelplan.domain;

import java.util.ArrayList;

public class RoutePlanResults {

    private boolean status;

    private String message;

    private ArrayList<RoutePlanResultUnit> results;

    public RoutePlanResults() {
        //Default Constructor
    }

    public RoutePlanResults(boolean status, String message, ArrayList<RoutePlanResultUnit> results) {
        this.status = status;
        this.message = message;
        this.results = results;
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

    public ArrayList<RoutePlanResultUnit> getResults() {
        return results;
    }

    public void setResults(ArrayList<RoutePlanResultUnit> results) {
        this.results = results;
    }
}
