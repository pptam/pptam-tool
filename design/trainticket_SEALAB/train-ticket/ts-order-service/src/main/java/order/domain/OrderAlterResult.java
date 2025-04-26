package order.domain;

public class OrderAlterResult {

    private boolean status;

    private String message;

    private Order oldOrder;

    private Order newOrder;

    public boolean isStatus() {
        return status;
    }

    public void setStatus(boolean status) {
        this.status = status;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public Order getOldOrder() {
        return oldOrder;
    }

    public void setOldOrder(Order oldOrder) {
        this.oldOrder = oldOrder;
    }

    public Order getNewOrder() {
        return newOrder;
    }

    public void setNewOrder(Order newOrder) {
        this.newOrder = newOrder;
    }
}
