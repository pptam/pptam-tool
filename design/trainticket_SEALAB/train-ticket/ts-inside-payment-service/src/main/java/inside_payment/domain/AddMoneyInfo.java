package inside_payment.domain;

import javax.xml.ws.soap.Addressing;


public class AddMoneyInfo {
    private String userId;
    private String money;


    public AddMoneyInfo(){}

    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public String getMoney() {
        return money;
    }

    public void setMoney(String money) {
        this.money = money;
    }

}
