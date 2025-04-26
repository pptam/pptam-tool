package price.domain;

public class QueryPriceConfigByTrainAndRoute {

    private String routeId;

    private String trainType;

    public QueryPriceConfigByTrainAndRoute() {
        //Default Constructor
    }

    public QueryPriceConfigByTrainAndRoute(String routeId, String trainType) {
        this.routeId = routeId;
        this.trainType = trainType;
    }

    public String getRouteId() {
        return routeId;
    }

    public void setRouteId(String routeId) {
        this.routeId = routeId;
    }

    public String getTrainType() {
        return trainType;
    }

    public void setTrainType(String trainType) {
        this.trainType = trainType;
    }
}
