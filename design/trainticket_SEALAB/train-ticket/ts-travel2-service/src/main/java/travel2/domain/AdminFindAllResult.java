package travel2.domain;

import java.util.ArrayList;

public class AdminFindAllResult {
    private boolean status;

    private String message;

    private ArrayList<AdminTrip> trips;

    public AdminFindAllResult(){

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

    public ArrayList<AdminTrip> getTrips() {
        return trips;
    }

    public void setTrips(ArrayList<AdminTrip> trips) {
        this.trips = trips;
    }
}
