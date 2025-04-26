package train.domain;

import org.springframework.data.annotation.Id;

import javax.validation.Valid;


public class Information {

    @Valid
    @Id
    private String id;

    @Valid
    private int economyClass;

    @Valid
    private int confortClass;

    private int averageSpeed;

    public Information(){
        //Default Constructor
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public int getEconomyClass() {
        return economyClass;
    }

    public void setEconomyClass(int economyClass) {
        this.economyClass = economyClass;
    }

    public int getConfortClass() {
        return confortClass;
    }

    public void setConfortClass(int confortClass) {
        this.confortClass = confortClass;
    }

    public int getAverageSpeed() {
        return averageSpeed;
    }

    public void setAverageSpeed(int averageSpeed) {
        this.averageSpeed = averageSpeed;
    }
}
