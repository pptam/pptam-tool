package rebook.domain;


public class ChangeOrderInfo {

    private Order order;

    private String loginToken;

    public ChangeOrderInfo() {
        //Default Constructor
    }

    public Order getOrder() {
        return order;
    }

    public void setOrder(Order order) {
        this.order = order;
    }

    public String getLoginToken() {
        return loginToken;
    }

    public void setLoginToken(String loginToken) {
        this.loginToken = loginToken;
    }
}
