package order.domain;

public class PayOrderInfo {

    //Set order status to paid.
    private String orderId;

    public PayOrderInfo() {
        //Default Constructor
    }

    public String getOrderId() {
        return orderId;
    }

    public void setOrderId(String orderId) {
        this.orderId = orderId;
    }
}
