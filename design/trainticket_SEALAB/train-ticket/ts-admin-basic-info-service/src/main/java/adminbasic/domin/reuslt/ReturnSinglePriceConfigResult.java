package adminbasic.domin.reuslt;

import adminbasic.domin.info.PriceInfo;

public class ReturnSinglePriceConfigResult {

    private boolean status;

    private String message;

    private PriceInfo priceConfig;

    public ReturnSinglePriceConfigResult() {
        //Empty Constructor
    }

    public ReturnSinglePriceConfigResult(boolean status, String message, PriceInfo priceConfig) {
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

    public PriceInfo getPriceConfig() {
        return priceConfig;
    }

    public void setPriceConfig(PriceInfo priceConfig) {
        this.priceConfig = priceConfig;
    }
}
