package admintravel.domain.response;

public class ResponseBean {
    private String message;
    private boolean status;

    public ResponseBean(){

    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public boolean isStatus() {
        return status;
    }

    public void setStatus(boolean status) {
        this.status = status;
    }
}
