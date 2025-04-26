package travel.domain;

import java.util.ArrayList;

public class GetTripsByRouteIdResult {

    private boolean status;

    private String message;

    private ArrayList<ArrayList<Trip>> tripsSet;

    public GetTripsByRouteIdResult() {
        //Default Constructor
    }

    public GetTripsByRouteIdResult(boolean status, String message, ArrayList<ArrayList<Trip>> tripsSet) {
        this.status = status;
        this.message = message;
        this.tripsSet = tripsSet;
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

    public ArrayList<ArrayList<Trip>> getTripsSet() {
        return tripsSet;
    }

    public void setTripsSet(ArrayList<ArrayList<Trip>> tripsSet) {
        this.tripsSet = tripsSet;
    }
}
