package price.domain;

public class ReturnSinglePriceConfigResult {

    private boolean status;

    private String message;

    private PriceConfig priceConfig;

    public ReturnSinglePriceConfigResult() {
        //Empty Constructor
    }

    public ReturnSinglePriceConfigResult(boolean status, String message, PriceConfig priceConfig) {
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

    public PriceConfig getPriceConfig() {
        return priceConfig;
    }

    public void setPriceConfig(PriceConfig priceConfig) {
        this.priceConfig = priceConfig;
    }
}
