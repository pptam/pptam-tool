package route.domain;

public class DeleteRouteInfo {

    private String routeId;

    public DeleteRouteInfo() {
        //Default Constructor
    }

    public DeleteRouteInfo(String routeId) {
        this.routeId = routeId;
    }

    public String getRouteId() {
        return routeId;
    }

    public void setRouteId(String routeId) {
        this.routeId = routeId;
    }
}
