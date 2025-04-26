package travelplan.domain;

import java.util.ArrayList;

public class TransferTravelSearchResult {

    private boolean status;

    private String message;

    private ArrayList<TripResponse> firstSectionResult;

    private ArrayList<TripResponse> secondSectionResult;

    public TransferTravelSearchResult() {
        //Default Constructor
    }

    public TransferTravelSearchResult(boolean status, String message, ArrayList<TripResponse> firstSectionResult, ArrayList<TripResponse> secondSectionResult) {
        this.status = status;
        this.message = message;
        this.firstSectionResult = firstSectionResult;
        this.secondSectionResult = secondSectionResult;
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

    public ArrayList<TripResponse> getFirstSectionResult() {
        return firstSectionResult;
    }

    public void setFirstSectionResult(ArrayList<TripResponse> firstSectionResult) {
        this.firstSectionResult = firstSectionResult;
    }

    public ArrayList<TripResponse> getSecondSectionResult() {
        return secondSectionResult;
    }

    public void setSecondSectionResult(ArrayList<TripResponse> secondSectionResult) {
        this.secondSectionResult = secondSectionResult;
    }
}
