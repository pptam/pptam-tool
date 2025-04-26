package preserveOther.domain;

import java.io.Serializable;

public enum AssuranceType implements Serializable{

    TRAFFIC_ACCIDENT (1, "Traffic Accident Assurance", 3.0);

    //index of assurance type
    private  int index;
    //the assurance type name
    private String name;
    //the price of this type of assurence
    private double price;

     AssuranceType(int index, String name, double price){
         this.index = index;
        this.name = name;
        this.price  = price;
    }

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

    public static AssuranceType getTypeByIndex(int index){
         AssuranceType[] ats = AssuranceType.values();
         for(AssuranceType at : ats){
             if(at.getIndex() == index){
                 return at;
             }
         }
         return null;
    }


}
