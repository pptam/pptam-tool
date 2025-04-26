package adminroute.domain.request;

public class DeleteRouteRequest {
    private String loginId;

    private String routeId;

    public DeleteRouteRequest() {
        //Default Constructor
    }

    public DeleteRouteRequest(String routeId) {
        this.routeId = routeId;
    }

    public String getLoginId() {
        return loginId;
    }

    public void setLoginId(String loginId) {
        this.loginId = loginId;
    }

    public String getRouteId() {
        return routeId;
    }

    public void setRouteId(String routeId) {
        this.routeId = routeId;
    }
}
