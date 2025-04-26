package security.domain;

public class UpdateSecurityConfigResult {

    private boolean status;

    private String message;

    private SecurityConfig result;

    public UpdateSecurityConfigResult() {
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

    public SecurityConfig getResult() {
        return result;
    }

    public void setResult(SecurityConfig result) {
        this.result = result;
    }
}
