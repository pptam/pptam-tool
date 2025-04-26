package adminbasic.domin.reuslt;

import adminbasic.domin.bean.PriceConfig;

import java.util.List;

public class GetAllPriceResult {

    private boolean status;

    private String message;

    private List<PriceConfig> priceConfig;

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

    public List<PriceConfig> getPriceConfig() {
        return priceConfig;
    }

    public void setPriceConfig(List<PriceConfig> priceConfig) {
        this.priceConfig = priceConfig;
    }

}
