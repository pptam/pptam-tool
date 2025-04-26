package travelplan.domain;

public class QueryByStationIdForName {

    private String stationId;

    public QueryByStationIdForName() {
        //Default Constructor
    }

    public QueryByStationIdForName(String stationId) {
        this.stationId = stationId;
    }

    public String getStationId() {
        return stationId;
    }

    public void setStationId(String stationId) {
        this.stationId = stationId;
    }
}
