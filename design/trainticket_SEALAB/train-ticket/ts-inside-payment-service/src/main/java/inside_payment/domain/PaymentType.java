package inside_payment.domain;

import java.io.Serializable;


public enum  PaymentType implements Serializable {
    P("Payment",1), D("Difference",2),O("Outside Payment",3),E("Difference & Outside Payment",4);

    private String name;
    private int index;

    PaymentType(String name, int index) {
        this.name = name;
        this.index = index;
    }

    public static String getName(int index) {
        for (PaymentType type : PaymentType.values()) {
            if (type.getIndex() == index) {
                return type.name;
            }
        }
        return null;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getIndex() {
        return index;
    }

    public void setIndex(int index) {
        this.index = index;
    }
}
