package rebook.domain;


public class DrawBackInfo {

    private String userId;
    private String money;

    public DrawBackInfo(){
        //Default Constructor
    }

    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public String getMoney() {
        return money;
    }

    public void setMoney(String money) {
        this.money = money;
    }
}
