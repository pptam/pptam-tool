package sso.domain;

public class AdminDeleteAccountRequest {
    private String accountId;

    public AdminDeleteAccountRequest(){

    }

    public String getAccountId() {
        return accountId;
    }

    public void setAccountId(String accountId) {
        this.accountId = accountId;
    }
}
