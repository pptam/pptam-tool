package preserve.domain;

public class QueryContactsInfo {

    private String loginToken;

    private String accountId;

    public QueryContactsInfo() {
        //Default Constructor
    }

    public String getLoginToken() {
        return loginToken;
    }

    public void setLoginToken(String loginToken) {
        this.loginToken = loginToken;
    }

    public String getAccountId() {
        return accountId;
    }

    public void setAccountId(String accountId) {
        this.accountId = accountId;
    }
}
