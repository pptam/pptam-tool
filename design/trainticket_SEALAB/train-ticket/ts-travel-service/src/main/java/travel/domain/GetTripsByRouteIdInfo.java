package travel.domain;

import java.util.ArrayList;

public class GetTripsByRouteIdInfo {

    private ArrayList<String> routeIds;

    public GetTripsByRouteIdInfo() {
        //Default Constructor
    }

    public GetTripsByRouteIdInfo(ArrayList<String> routeIds) {
        this.routeIds = routeIds;
    }

    public ArrayList<String> getRouteIds() {
        return routeIds;
    }

    public void setRouteIds(ArrayList<String> routeIds) {
        this.routeIds = routeIds;
    }
}
