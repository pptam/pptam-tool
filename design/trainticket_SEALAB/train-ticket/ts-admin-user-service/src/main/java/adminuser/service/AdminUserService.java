package adminuser.service;

import adminuser.domain.request.AddAccountRequest;
import adminuser.domain.request.DeleteAccountRequest;
import adminuser.domain.request.UpdateAccountRequest;
import adminuser.domain.response.DeleteAccountResult;
import adminuser.domain.response.FindAllAccountResult;
import adminuser.domain.response.ModifyAccountResult;
import adminuser.domain.response.RegisterResult;
import org.springframework.http.HttpHeaders;

public interface AdminUserService {
    FindAllAccountResult getAllUsers(String id, HttpHeaders headers);
    DeleteAccountResult deleteUser(DeleteAccountRequest request, HttpHeaders headers);
    ModifyAccountResult updateUser(UpdateAccountRequest request, HttpHeaders headers);
    RegisterResult addUser(AddAccountRequest request, HttpHeaders headers);
}
