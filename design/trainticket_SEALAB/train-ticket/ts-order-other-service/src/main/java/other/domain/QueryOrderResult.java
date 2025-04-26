package other.domain;

import java.util.ArrayList;

public class QueryOrderResult {

    private boolean status;

    private String message;

    private ArrayList<Order> orders;

    public QueryOrderResult() {
        //Default Constructor
    }

    public QueryOrderResult(boolean status, String message, ArrayList<Order> orders) {
        this.status = status;
        this.message = message;
        this.orders = orders;
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
