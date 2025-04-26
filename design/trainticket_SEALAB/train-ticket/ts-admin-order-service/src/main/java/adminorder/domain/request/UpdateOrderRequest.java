package adminorder.domain.request;

import adminorder.domain.bean.Order;

public class UpdateOrderRequest {
    private String loginid;
    private Order order;

    public UpdateOrderRequest(){

    }

    public String getLoginid() {
        return loginid;
    }

    public void setLoginid(String loginid) {
        this.loginid = loginid;
    }

    public Order getOrder() {
        return order;
    }

    public void setOrder(Order order) {
        this.order = order;
    }
}
