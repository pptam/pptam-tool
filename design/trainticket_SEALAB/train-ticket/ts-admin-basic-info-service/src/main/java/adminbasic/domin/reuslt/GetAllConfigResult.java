package adminbasic.domin.reuslt;

import adminbasic.domin.bean.Config;

import java.util.List;

public class GetAllConfigResult {

    private boolean status;

    private String message;

    private List<Config> configs;

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

    public List<Config> getConfigs() {
        return configs;
    }

    public void setConfigs(List<Config> configs) {
        this.configs = configs;
    }


}
