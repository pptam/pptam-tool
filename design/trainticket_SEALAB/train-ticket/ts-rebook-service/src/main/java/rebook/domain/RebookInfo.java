package rebook.domain;

import javax.validation.Valid;
import javax.validation.constraints.NotNull;
import java.util.Date;


public class RebookInfo {

    @Valid
    @NotNull
    private String orderId;

    @Valid
    @NotNull
    private String oldTripId;

    @Valid
    @NotNull
    private String tripId;

    @Valid
    @NotNull
    private int seatType;

    @Valid
    @NotNull
    private Date date;//具体到哪一天

    public RebookInfo(){
        //Default Constructor
    }

    public String getOrderId() {
        return orderId;
    }

    public void setOrderId(String orderId) {
        this.orderId = orderId;
    }

    public String getTripId() {
        return tripId;
    }

    public void setTripId(String tripId) {
        this.tripId = tripId;
    }

    public int getSeatType() {
        return seatType;
    }

    public void setSeatType(int seatType) {
        this.seatType = seatType;
    }

    public Date getDate() {
        return date;
    }

    public void setDate(Date date) {
        this.date = date;
    }

    public String getOldTripId() {
        return oldTripId;
    }

    public void setOldTripId(String oldTripId) {
        this.oldTripId = oldTripId;
    }
}
