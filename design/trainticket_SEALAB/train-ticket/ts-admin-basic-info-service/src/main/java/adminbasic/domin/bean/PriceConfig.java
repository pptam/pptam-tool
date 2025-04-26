package adminbasic.domin.bean;

public class PriceConfig {

    private String id;

    private String trainType;

    private String routeId;

    private double basicPriceRate;

    private double firstClassPriceRate;

    public PriceConfig() {
        //Empty Constructor
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getTrainType() {
        return trainType;
    }

    public void setTrainType(String trainType) {
        this.trainType = trainType;
    }

    public String getRouteId() {
        return routeId;
    }

    public void setRouteId(String routeId) {
        this.routeId = routeId;
    }

    public double getBasicPriceRate() {
        return basicPriceRate;
    }

    public void setBasicPriceRate(double basicPriceRate) {
        this.basicPriceRate = basicPriceRate;
    }

    public double getFirstClassPriceRate() {
        return firstClassPriceRate;
    }

    public void setFirstClassPriceRate(double firstClassPriceRate) {
        this.firstClassPriceRate = firstClassPriceRate;
    }
}
