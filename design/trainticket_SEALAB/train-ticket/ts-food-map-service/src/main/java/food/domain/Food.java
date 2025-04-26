package food.domain;

//import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
//import org.springframework.data.annotation.Id;
//import org.springframework.data.mongodb.core.mapping.Document;

import java.io.Serializable;
//import java.util.UUID;

//@Document(collection = "foods")
//@JsonIgnoreProperties(ignoreUnknown = true)
public class Food implements Serializable{

    public Food(){

    }

//    @Id
//    private UUID id;
    private String foodName;
    private double price;


//    public UUID getId() {
//        return id;
//    }
//
//    public void setId(UUID id) {
//        this.id = id;
//    }

    public String getFoodName() {
        return foodName;
    }

    public void setFoodName(String foodName) {
        this.foodName = foodName;
    }

    public double getPrice() {
        return price;
    }

    public void setPrice(double price) {
        this.price = price;
    }

}
