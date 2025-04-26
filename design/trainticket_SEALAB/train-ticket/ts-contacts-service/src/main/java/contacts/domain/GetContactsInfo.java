package contacts.domain;

public class GetContactsInfo {

    private String loginToken;

    private String contactsId;

    public GetContactsInfo(){
        //Default Constructor
    }

    public String getLoginToken() {
        return loginToken;
    }

    public void setLoginToken(String loginToken) {
        this.loginToken = loginToken;
    }

    public String getContactsId() {
        return contactsId;
    }

    public void setContactsId(String contactsId) {
        this.contactsId = contactsId;
    }
}

