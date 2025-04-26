package rebook.domain;


public class QueryOrder {

    private String orderId;

    public QueryOrder(){
        //Default Constructor
    }

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
