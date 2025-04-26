package sso.domain;

public class LoginAccountValue {

    private String accountId;

    private String loginToken;

    public LoginAccountValue() {
        //Default Constructor
    }

    public LoginAccountValue(String accountId, String loginToken) {
        this.accountId = accountId;
        this.loginToken = loginToken;
    }

    public String getAccountId() {
        return accountId;
    }

    public void setAccountId(String accountId) {
        this.accountId = accountId;
    }

    public String getLoginToken() {
        return loginToken;
    }

    public void setLoginToken(String loginToken) {
        this.loginToken = loginToken;
    }
}
