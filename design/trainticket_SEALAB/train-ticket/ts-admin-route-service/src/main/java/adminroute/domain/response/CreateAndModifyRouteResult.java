package adminroute.domain.response;

import adminroute.domain.bean.Route;

public class CreateAndModifyRouteResult {

    private boolean status;

    private String message;

    private Route route;

    public CreateAndModifyRouteResult() {
        //Default Constructor
    }

    public CreateAndModifyRouteResult(boolean status, String message, Route route) {
        this.status = status;
        this.message = message;
        this.route = route;
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

    public Route getRoute() {
        return route;
    }

    public void setRoute(Route route) {
        this.route = route;
    }
}
