package other.domain;

import java.util.Date;

public class GetOrderInfoForSecurity {

    private Date checkDate;

    private String accountId;

    public GetOrderInfoForSecurity() {
        //Default Constructor
    }

    public Date getCheckDate() {
        return checkDate;
    }

    public void setCheckDate(Date checkDate) {
        this.checkDate = checkDate;
    }

    public String getAccountId() {
        return accountId;
    }

    public void setAccountId(String accountId) {
        this.accountId = accountId;
    }
}
