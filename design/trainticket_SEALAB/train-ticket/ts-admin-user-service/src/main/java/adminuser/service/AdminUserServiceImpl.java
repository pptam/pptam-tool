package adminuser.service;

import adminuser.domain.request.AddAccountRequest;
import adminuser.domain.request.AdminDeleteAccountRequest;
import adminuser.domain.request.DeleteAccountRequest;
import adminuser.domain.request.UpdateAccountRequest;
import adminuser.domain.response.DeleteAccountResult;
import adminuser.domain.response.FindAllAccountResult;
import adminuser.domain.response.ModifyAccountResult;
import adminuser.domain.response.RegisterResult;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class AdminUserServiceImpl implements AdminUserService {
    @Autowired
    private RestTemplate restTemplate;

    @Override
    public FindAllAccountResult getAllUsers(String id, HttpHeaders headers) {
        FindAllAccountResult result = new FindAllAccountResult();
        if(checkId(id)){
            System.out.println("[Admin User Service][Get All Users]");
            HttpEntity requestEntity = new HttpEntity(headers);
            ResponseEntity<FindAllAccountResult> re = restTemplate.exchange(
                    "http://ts-sso-service:12349/account/findAll",
                    HttpMethod.GET,
                    requestEntity,
                    FindAllAccountResult.class);
            result = re.getBody();
//            result = restTemplate.getForObject(
//                    "http://ts-sso-service:12349/account/findAll",
//                    FindAllAccountResult.class);
        }else{
            System.out.println("[Admin User Service][Wrong Admin ID]");
            result.setStatus(false);
            result.setMessage("The loginId is Wrong: " + id);
        }
        return result;
    }

    @Override
    public DeleteAccountResult deleteUser(DeleteAccountRequest request, HttpHeaders headers) {
        DeleteAccountResult result = new DeleteAccountResult();
        if(checkId(request.getLoginId())){
            AdminDeleteAccountRequest adminDeleteAccountRequest = new AdminDeleteAccountRequest();
            adminDeleteAccountRequest.setAccountId(request.getAccountId());
            HttpEntity requestEntity = new HttpEntity(adminDeleteAccountRequest, headers);
            ResponseEntity<DeleteAccountResult> re = restTemplate.exchange(
                    "http://ts-sso-service:12349/account/admindelete",
                    HttpMethod.POST,
                    requestEntity,
                    DeleteAccountResult.class);
            result = re.getBody();
//            result = restTemplate.postForObject(
//                    "http://ts-sso-service:12349/account/admindelete", adminDeleteAccountRequest,DeleteAccountResult.class);
        }
        else{
            System.out.println("[Admin User Service][Wrong Admin ID]");
            result.setStatus(false);
            result.setMessage("The loginId is Wrong: " + request.getLoginId());
        }
        return result;
    }

    @Override
    public ModifyAccountResult updateUser(UpdateAccountRequest request, HttpHeaders headers) {
        ModifyAccountResult result = new ModifyAccountResult();
        if(checkId(request.getLoginId())){
            HttpEntity requestEntity = new HttpEntity(request.getModifyAccountInfo(), headers);
            ResponseEntity<ModifyAccountResult> re = restTemplate.exchange(
                    "http://ts-sso-service:12349/account/modify",
                    HttpMethod.POST,
                    requestEntity,
                    ModifyAccountResult.class);
            result = re.getBody();
//            result = restTemplate.postForObject(
//                    "http://ts-sso-service:12349/account/modify", request.getModifyAccountInfo() ,ModifyAccountResult.class);
        }
        else{
            System.out.println("[Admin User Service][Wrong Admin ID]");
            result.setStatus(false);
            result.setMessage("The loginId is Wrong: " + request.getLoginId());
        }
        return result;
    }

    @Override
    public RegisterResult addUser(AddAccountRequest request, HttpHeaders headers) {
        RegisterResult result = new RegisterResult();
        if(checkId(request.getLoginId())){
            HttpEntity requestEntity = new HttpEntity(request, headers);
            ResponseEntity<RegisterResult> re = restTemplate.exchange(
                    "http://ts-sso-service:12349/account/register",
                    HttpMethod.POST,
                    requestEntity,
                    RegisterResult.class);
            result = re.getBody();
//            result = restTemplate.postForObject(
//                    "http://ts-sso-service:12349/account/register", request ,RegisterResult.class);
        }
        else{
            System.out.println("[Admin User Service][Wrong Admin ID]");
            result.setStatus(false);
            result.setMessage("The loginId is Wrong: " + request.getLoginId());
        }
        return result;
    }

    private boolean checkId(String id){
        if("1d1a11c1-11cb-1cf1-b1bb-b11111d1da1f".equals(id)){
            return true;
        }
        else{
            return false;
        }
    }
}
