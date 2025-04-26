package other.domain;

public class GetOrderInfoForSecurityResult {

    private int orderNumInLastOneHour;

    private int orderNumOfValidOrder;

    public GetOrderInfoForSecurityResult() {
        //Default Constructor
    }

    public int getOrderNumInLastOneHour() {
        return orderNumInLastOneHour;
    }

    public void setOrderNumInLastOneHour(int orderNumInLastOneHour) {
        this.orderNumInLastOneHour = orderNumInLastOneHour;
    }

    public int getOrderNumOfValidOrder() {
        return orderNumOfValidOrder;
    }

    public void setOrderNumOfValidOrder(int orderNumOfValidOrder) {
        this.orderNumOfValidOrder = orderNumOfValidOrder;
    }
}
