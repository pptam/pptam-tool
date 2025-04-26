package security.domain;

import java.util.ArrayList;

public class GetAllSecurityConfigResult {

    private boolean status;

    private String message;

    private ArrayList<SecurityConfig> result;

    public GetAllSecurityConfigResult() {
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

    public ArrayList<SecurityConfig> getResult() {
        return result;
    }

    public void setResult(ArrayList<SecurityConfig> result) {
        this.result = result;
    }
}
