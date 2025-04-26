package route.domain;

public class DeleteRouteResult {

    private boolean status;

    private String message;

    public DeleteRouteResult() {
        //Default Constructor
    }

    public DeleteRouteResult(boolean status, String message) {
        this.status = status;
        this.message = message;
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
}
