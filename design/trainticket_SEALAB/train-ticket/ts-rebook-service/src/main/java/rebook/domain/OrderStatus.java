package rebook.domain;

public enum OrderStatus {

    NOTPAID   (0,"Not Paid"),
    PAID      (1,"Paid & Not Collected"),
    COLLECTED (2,"Collected"),
    CHANGE    (3,"Cancel & Rebook"),
    CANCEL    (4,"Cancel"),
    REFUNDS   (5,"Refunded"),
    USED      (6,"Used");

    private int code;
    private String name;

    OrderStatus(int code, String name){
        this.code = code;
        this.name = name;
    }

    public int getCode(){
        return code;
    }

    public String getName() {
        return name;
    }

    public static String getNameByCode(int code){
        OrderStatus[] orderStatusSet = OrderStatus.values();
        for(OrderStatus orderStatus : orderStatusSet){
            if(orderStatus.getCode() == code){
                return orderStatus.getName();
            }
        }
        return orderStatusSet[0].getName();
    }

}
