package food.init;

import food.domain.Food;
import food.domain.FoodStore;
import food.domain.TrainFood;
import food.service.FoodMapService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Component
public class InitData implements CommandLineRunner{

    @Autowired
    FoodMapService service;

    String foodStoresPath = "/foodstores.txt";
    String trainFoodPath = "/trainfood.txt";

    @Override
    public void run(String... args) throws Exception {

//        File foodStores = new File(foodStoresPath);
//        FileReader fr1 = new FileReader(foodStores);
        BufferedReader br1 = new BufferedReader(new InputStreamReader(this.getClass().getResourceAsStream(foodStoresPath)));
        try{
            String line = br1.readLine();
            while( line != null ){
                if( !line.trim().equals("") ){
                    FoodStore fs = new FoodStore();
                    fs.setId(UUID.randomUUID());
                    String[] lineTemp = line.trim().split("=");
                    fs.setStationId(lineTemp[1]);
//                    System.out.println("stationId=" + lineTemp[1]);
                    lineTemp = br1.readLine().trim().split("=");
                    fs.setStoreName(lineTemp[1]);
//                    System.out.println("storeName=" + lineTemp[1]);
                    lineTemp = br1.readLine().trim().split("=");
                    fs.setTelephone(lineTemp[1]);
//                    System.out.println("teltphone=" + lineTemp[1]);
                    lineTemp = br1.readLine().trim().split("=");
                    fs.setBusinessTime(lineTemp[1]);
//                    System.out.println("businessTime=" + lineTemp[1]);
                    lineTemp = br1.readLine().trim().split("=");
                    fs.setDeliveryFee( Double.parseDouble(lineTemp[1]) );
//                    System.out.println("deliveryFee=" + lineTemp[1]);
                    lineTemp = br1.readLine().trim().split("=");
//                    System.out.println("foodList=" + lineTemp[1]);
                    fs.setFoodList(toFoodList(lineTemp[1]));
                    service.createFoodStore(fs,null);
                }
                line = br1.readLine();
            }

        } catch(Exception e){
            System.out.println("the foodstores.txt has format error!");
            e.printStackTrace();
            System.exit(1);
        }

//        File trainFood = new File(trainFoodPath);
//        FileReader fr2 = new FileReader(trainFood);
        BufferedReader br2 = new BufferedReader(new InputStreamReader(this.getClass().getResourceAsStream(trainFoodPath)));
        try{
            String line2 = br2.readLine();
            while( line2 != null ){
                if( !line2.trim().equals("") ){
                    TrainFood tf = new TrainFood();
                    tf.setId(UUID.randomUUID());
                    String[] lineTemp = line2.trim().split("=");
                    tf.setTripId(lineTemp[1]);
                    lineTemp = br2.readLine().trim().split("=");
                    tf.setFoodList(toFoodList(lineTemp[1]));
                    service.createTrainFood(tf,null);
                }
                line2 = br2.readLine();
            }

        } catch(Exception e){
            System.out.println("the trainfood.txt has format error!");
            e.printStackTrace();
            System.exit(1);
        }


//        Food food1 = new Food();
//        food1.setFoodName("Hamburger");
//        food1.setPrice(10);
//        Food food2 = new Food();
//        food2.setFoodName("Pork Chop with rice");
//        food2.setPrice(30);
//        List<Food> foodList1 = new ArrayList<Food>();
//        foodList1.add(food1);
//        List<Food> foodList2 = new ArrayList<Food>();
//        foodList2.add(food2);
//
//        FoodStore fs1 = new FoodStore();
//        fs1.setId(UUID.randomUUID());
//        fs1.setStationId("Shanghai");
//        fs1.setStoreName("KFC");
//        fs1.setTelephone("01-234567");
//        fs1.setBusinessTime("10:00-20:00");
//        fs1.setDeliveryFee(20);
//        fs1.setFoodList(foodList1);
//        service.createFoodStore(fs1);
//
//        TrainFood tf1 = new TrainFood();
//        tf1.setId(UUID.randomUUID());
//        tf1.setTripId("G1234");
//        tf1.setFoodList(foodList2);
//        service.createTrainFood(tf1);


    }

    private List<Food> toFoodList(String s){
        System.out.println("s=" + s);
        String[] foodstring = s.split("_");
        List<Food> foodList = new ArrayList<Food>();
        for(int i = 0; i< foodstring.length; i++){
            String[] foodTemp = foodstring[i].split(",");
            Food food = new Food();
            food.setFoodName(foodTemp[0]);
//            System.out.println("foodTemp[0]=" + foodTemp[0]);
            food.setPrice(Double.parseDouble(foodTemp[1]));
//            System.out.println("foodTemp[0]=" + foodTemp[1]);
            foodList.add(food);
        }
        return foodList;
    }
}
