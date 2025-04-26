package price.domain;

import java.util.ArrayList;

public class ReturnManyPriceConfigResult {

    private boolean status;

    private String message;

    private ArrayList<PriceConfig> priceConfig;

    public ReturnManyPriceConfigResult() {
        //Default Constructor
    }

    public ReturnManyPriceConfigResult(boolean status, String message, ArrayList<PriceConfig> priceConfig) {
        this.status = status;
        this.message = message;
        this.priceConfig = priceConfig;
    }

    public boolean isStatus() {
        return status;
    }

    public void setStatus(boolean status) {
        this.status = status;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public ArrayList<PriceConfig> getPriceConfig() {
        return priceConfig;
    }

    public void setPriceConfig(ArrayList<PriceConfig> priceConfig) {
        this.priceConfig = priceConfig;
    }
}
