package adminuser.domain.request;

import adminuser.domain.bean.ModifyAccountInfo;

public class UpdateAccountRequest {
    private String loginId;
    private ModifyAccountInfo modifyAccountInfo;

    public UpdateAccountRequest(){

    }

    public String getLoginId() {
        return loginId;
    }

    public void setLoginId(String loginId) {
        this.loginId = loginId;
    }

    public ModifyAccountInfo getModifyAccountInfo() {
        return modifyAccountInfo;
    }

    public void setModifyAccountInfo(ModifyAccountInfo modifyAccountInfo) {
        this.modifyAccountInfo = modifyAccountInfo;
    }
}
