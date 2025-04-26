package adminorder.domain.response;

import adminorder.domain.bean.Order;

import java.util.ArrayList;

public class GetAllOrderResult {
    private boolean status;

    private String message;

    private ArrayList<Order> orders;

    public GetAllOrderResult(){

    }

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

    public ArrayList<Order> getOrders() {
        return orders;
    }

    public void setOrders(ArrayList<Order> orders) {
        this.orders = orders;
    }
}
