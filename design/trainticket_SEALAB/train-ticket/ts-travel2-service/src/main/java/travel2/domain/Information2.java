package travel2.domain;

import org.springframework.data.annotation.Id;

import javax.validation.Valid;


public class Information2 {
    @Valid
    @Id
    private String tripId;

    public Information2(){
        //Default Constructor
    }

    public String getTripId() {
        return tripId;
    }

    public void setTripId(String tripId) {
        this.tripId = tripId;
    }
}
