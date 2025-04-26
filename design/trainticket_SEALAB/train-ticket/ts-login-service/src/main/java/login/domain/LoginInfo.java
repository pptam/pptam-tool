package login.domain;

public class LoginInfo {

    private String email;

    private String password;

    private String verificationCode;

    public LoginInfo() {
        this.email = "";
        this.password = "";
        this.verificationCode = "";
    }

    public String getVerificationCode() {
        return verificationCode;
    }

    public void setVerificationCode(String verificationCode) {
        this.verificationCode = verificationCode;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }
}
