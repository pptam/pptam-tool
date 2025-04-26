package sso.domain;

import java.util.ArrayList;

public class GetLoginAccountList {

    private boolean status;

    private String message;

    private ArrayList<LoginAccountValue> loginAccountList;

    public GetLoginAccountList() {
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

    public ArrayList<LoginAccountValue> getLoginAccountList() {
        return loginAccountList;
    }

    public void setLoginAccountList(ArrayList<LoginAccountValue> loginAccountList) {
        this.loginAccountList = loginAccountList;
    }
}
