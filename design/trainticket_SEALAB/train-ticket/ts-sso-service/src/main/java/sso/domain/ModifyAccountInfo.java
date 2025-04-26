package sso.domain;

public class ModifyAccountInfo {

    private String accountId;

    private String newEmail;

    private String newPassword;

    private String newName;

    private int newGender;

    private int newDocumentType;

    private String newDocumentNumber;

    public ModifyAccountInfo() {
        //Default Constructor
    }

    public String getAccountId() {
        return accountId;
    }

    public void setAccountId(String accountId) {
        this.accountId = accountId;
    }

    public String getNewEmail() {
        return newEmail;
    }

    public void setNewEmail(String newEmail) {
        this.newEmail = newEmail;
    }

    public String getNewPassword() {
        return newPassword;
    }

    public void setNewPassword(String newPassword) {
        this.newPassword = newPassword;
    }

    public String getNewName() {
        return newName;
    }

    public void setNewName(String newName) {
        this.newName = newName;
    }

    public int getNewGender() {
        return newGender;
    }

    public void setNewGender(int newGender) {
        this.newGender = newGender;
    }

    public int getNewDocumentType() {
        return newDocumentType;
    }

    public void setNewDocumentType(int newDocumentType) {
        this.newDocumentType = newDocumentType;
    }

    public String getNewDocumentNumber() {
        return newDocumentNumber;
    }

    public void setNewDocumentNumber(String newDocumentNumber) {
        this.newDocumentNumber = newDocumentNumber;
    }
}
