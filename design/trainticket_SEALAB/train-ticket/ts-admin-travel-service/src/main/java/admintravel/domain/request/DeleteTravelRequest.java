package admintravel.domain.request;

import org.springframework.data.annotation.Id;

import javax.validation.Valid;


public class DeleteTravelRequest {
    private String loginId;

    @Valid
    @Id
    private String tripId;

    public DeleteTravelRequest(){
        //Default Constructor
    }

    public String getLoginId() {
        return loginId;
    }

    public void setLoginId(String loginId) {
        this.loginId = loginId;
    }

    public String getTripId() {
        return tripId;
    }

    public void setTripId(String tripId) {
        this.tripId = tripId;
    }
}
