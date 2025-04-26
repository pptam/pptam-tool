package plan.domain;

import java.util.ArrayList;

public class QueryTripResponsePackage {

    public boolean status;

    public String message;

    public ArrayList<TripResponse> responses;

    public QueryTripResponsePackage() {
    }

    public QueryTripResponsePackage(boolean status, String message, ArrayList<TripResponse> responses) {
        this.status = status;
        this.message = message;
        this.responses = responses;
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

    public ArrayList<TripResponse> getResponses() {
        return responses;
    }

    public void setResponses(ArrayList<TripResponse> responses) {
        this.responses = responses;
    }
}
