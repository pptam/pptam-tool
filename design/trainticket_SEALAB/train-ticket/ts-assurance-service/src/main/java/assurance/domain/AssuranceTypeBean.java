package assurance.domain;

import java.io.Serializable;

public class AssuranceTypeBean implements Serializable{

    //index of assurance type
    private  int index;
    //the assurance type name
    private String name;
    //the price of this type of assurence
    private double price;

    public int getIndex() {
        return index;
    }

    public void setIndex(int index) {
        this.index = index;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public double getPrice() {
        return price;
    }

    public void setPrice(double price) {
        this.price = price;
    }




}
