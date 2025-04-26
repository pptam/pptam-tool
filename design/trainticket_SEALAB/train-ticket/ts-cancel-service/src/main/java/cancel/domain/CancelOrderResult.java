package cancel.domain;

public class CancelOrderResult {

    private boolean status;

    private String message;

    public CancelOrderResult() {
        //Default Constructor
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
