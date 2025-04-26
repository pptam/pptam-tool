package adminbasic.domin.bean;

import javax.validation.Valid;
import javax.validation.constraints.NotNull;


public class Station {

    private String id;

    @Valid
    @NotNull
    private String name;

    private int stayTime;

    private String loginId;

    public Station(){
        //Default Constructor
    }

    public String getLoginId() {
        return loginId;
    }

    public void setLoginId(String loginId) {
        this.loginId = loginId;
    }

    public Station(String id, String name) {
        this.id = id;
        this.name = name;
    }


    public Station(String id, String name, int stayTime) {
        this.id = id;
        this.name = name;
        this.stayTime = stayTime;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getStayTime() {
        return stayTime;
    }

    public void setStayTime(int stayTime) {
        this.stayTime = stayTime;
    }
}
