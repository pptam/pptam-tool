package travel.domain;

import javax.validation.Valid;
import javax.validation.constraints.NotNull;
import java.util.Date;


public class QueryInfo {

    @Valid
    @NotNull
    private String startingPlace;

    @Valid
    @NotNull
    private String endPlace;

    @Valid
    @NotNull
    private Date departureTime;

    public QueryInfo(){
        //Default Constructor
    }

    public String getStartingPlace() {
        return startingPlace;
    }

    public void setStartingPlace(String startingPlace) {
        this.startingPlace = startingPlace;
    }

    public String getEndPlace() {
        return endPlace;
    }

    public void setEndPlace(String endPlace) {
        this.endPlace = endPlace;
    }

    public Date getDepartureTime() {
        return departureTime;
    }

    public void setDepartureTime(Date departureTime) {
        this.departureTime = departureTime;
    }
}
