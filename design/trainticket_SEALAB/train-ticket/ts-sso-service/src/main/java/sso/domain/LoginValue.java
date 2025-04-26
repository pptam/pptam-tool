package sso.domain;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "login_user_list")
@JsonIgnoreProperties(ignoreUnknown = true)
public class LoginValue {

    @Id
    private String id;

    private String loginToken;

    public LoginValue(){
        //Default Constructor
    }

    public LoginValue(String loginId,String loginToken){
        this.id = loginId;
        this.loginToken = loginToken;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getLoginToken() {
        return loginToken;
    }

    public void setLoginToken(String loginToken) {
        this.loginToken = loginToken;
    }
}
