package consign.domain;

public class GetPriceDomain {
    private double weight;
    private boolean isWithinRegion;

    public GetPriceDomain(){

    }

    public double getWeight() {
        return weight;
    }

    public void setWeight(double weight) {
        this.weight = weight;
    }

    public boolean isWithinRegion() {
        return isWithinRegion;
    }

    public void setWithinRegion(boolean withinRegion) {
        isWithinRegion = withinRegion;
    }
}
