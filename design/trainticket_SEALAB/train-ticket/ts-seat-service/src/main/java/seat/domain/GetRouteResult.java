package seat.domain;

public class GetRouteResult {

    private boolean status;

    private String message;

    private Route route;

    public GetRouteResult() {
        //Default Constructor
    }

    public GetRouteResult(boolean status, String message, Route route) {
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
