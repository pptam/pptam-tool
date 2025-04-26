package inside_payment.domain;


public class QueryOrder {

    private String orderId;

    public QueryOrder(){}

    public QueryOrder(String orderId) {
        this.orderId = orderId;
    }

    public String getOrderId() {
        return orderId;
    }

    public void setOrderId(String orderId) {
        this.orderId = orderId;
    }

}
