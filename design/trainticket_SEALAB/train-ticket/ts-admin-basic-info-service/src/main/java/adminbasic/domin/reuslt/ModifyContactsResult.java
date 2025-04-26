package adminbasic.domin.reuslt;

import adminbasic.domin.bean.Contacts;

public class ModifyContactsResult {

    private boolean status;

    private String message;

    private Contacts contacts;

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

    public Contacts getContacts() {
        return contacts;
    }

    public void setContacts(Contacts contacts) {
        this.contacts = contacts;
    }

}
