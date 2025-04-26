package inside_payment.domain;

import javax.validation.Valid;
import javax.validation.constraints.NotNull;


public class Balance {
    @Valid
    @NotNull
    private String userId;

    @Valid
    @NotNull
    private String balance;

    public Balance(){}

    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public String getBalance() {
        return balance;
    }

    public void setBalance(String balance) {
        this.balance = balance;
    }
}
