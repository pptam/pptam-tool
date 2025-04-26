package sso.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.stereotype.Service;
import sso.domain.*;
import sso.repository.AccountRepository;
import sso.repository.LoginUserListRepository;
import java.util.ArrayList;
import java.util.UUID;

@Service
public class AccountSsoServiceImpl implements AccountSsoService{

    @Autowired
    private AccountRepository accountRepository;

    @Autowired
    private LoginUserListRepository loginUserListRepository;

    //private static HashMap<String,String > loginUserList = new HashMap<>();

    @Override
    public Account createAccount(Account account, HttpHeaders headers){

        if(accountRepository.findById(account.getId()) != null){
            System.out.println("[SSO Service][Init Account] Account Already Exists.");
            return account;
        }
        System.out.println("[SSO Service][Init Account] Before:" + account.getId());
        Account resultAcc = accountRepository.save(account);
        Account oldAcc = accountRepository.findByEmail(account.getEmail());
        System.out.println("[SSO Service][Init Account] After:" + oldAcc.getId());
        return resultAcc;
    }

    @Override
    public RegisterResult create(RegisterInfo ri, HttpHeaders headers){
        Account oldAcc = accountRepository.findByEmail(ri.getEmail());
        if(oldAcc != null){
            RegisterResult rr = new RegisterResult();
            rr.setStatus(false);
            rr.setMessage("Account Already Exists");
            rr.setAccount(null);
            System.out.println("[SSO Service][Register] Fail.Account already exists.");
            System.out.println("[SSO Service][Register] Register Email:" + ri.getEmail() + " Exist Email:" + oldAcc.getEmail());
            return rr;
        }
        Account account = new Account();
        account.setId(UUID.randomUUID());
        account.setEmail(ri.getEmail());
        account.setPassword(ri.getPassword());
        account.setName(ri.getName());
        account.setDocumentNum(ri.getDocumentNum());
        account.setDocumentType(ri.getDocumentType());
        account.setGender(ri.getGender());
        Account resultAcc = accountRepository.save(account);
        resultAcc.setPassword("");
        System.out.println("[SSO Service][Register] Success.");
        RegisterResult rr = new RegisterResult();
        rr.setStatus(true);
        rr.setMessage("Success");
        rr.setAccount(account);
        return rr;
    }

    @Override
    public LoginResult login(LoginInfo li, HttpHeaders headers){
        if(li == null){
            System.out.println("[SSO Service][Login] Fail.Account not found.");
            LoginResult lr = new LoginResult();
            lr.setStatus(false);
            lr.setMessage("Account Not Found");
            lr.setAccount(null);
            return lr;
        }
        Account result = accountRepository.findByEmail(li.getEmail());
        if(result != null &&
                result.getPassword() != null && li.getPassword() != null
                && result.getPassword().equals(li.getPassword())){
            result.setPassword("");
            System.out.println("[SSO Service][Login] Success.");
            LoginResult lr = new LoginResult();
            lr.setStatus(true);
            lr.setMessage("Success");
            lr.setAccount(result);
            return lr;
        }else{
            LoginResult lr = new LoginResult();
            lr.setStatus(false);
            lr.setAccount(null);
            if(result == null){
                lr.setMessage("Account Not Exist");
                System.out.println("[SSO Service][Login] Fail.Account Not Exist.");
            }else{
                lr.setMessage("Password Wrong");
                System.out.println("[SSO Service][Login] Fail.Wrong Password.");
            }
            return lr;
        }
    }

    @Override
    public PutLoginResult loginPutToken(String loginId){
        PutLoginResult plr = new PutLoginResult();
        LoginValue loginValue = loginUserListRepository.findById(loginId);

        //if(loginUserList.keySet().contains(loginId)){
        if(loginValue != null){
            System.out.println("[SSO Service][Login] Already Login. Old login session will be kick off");
//            plr.setStatus(false);
//            plr.setLoginId(loginId);
//            plr.setMsg("Already Login");
//            plr.setToken(null);
            String token = UUID.randomUUID().toString();
            loginUserListRepository.save(new LoginValue(loginId,token));
            //loginUserList.put(loginId,token);
            plr.setStatus(true);
            plr.setLoginId(loginId);
            plr.setMsg("Success.Other login session has been kick off.");
            plr.setToken(token);

        }else{
            String token = UUID.randomUUID().toString();
            loginUserListRepository.save(new LoginValue(loginId,token));
            //loginUserList.put(loginId,token);
            System.out.println("[SSO Service][Login] Login Success. Id:" + loginId + " Token:" + token);
            plr.setStatus(true);
            plr.setLoginId(loginId);
            plr.setMsg("Success");
            plr.setToken(token);
        }
        return plr;
    }

    @Override
    public LogoutResult logoutDeleteToken(LogoutInfo li, HttpHeaders headers){
        LogoutResult lr = new LogoutResult();
        if(loginUserListRepository.findById(li.getId()) == null){
            System.out.println("[SSO Service][Logout] Already Logout. LogoutId:" + li.getId());
           lr.setStatus(false);
           lr.setMessage("Not Login");
        }else{
            String savedToken = loginUserListRepository.findById(li.getId()).getLoginToken();
            if(savedToken.equals(li.getToken())){
                loginUserListRepository.delete(li.getId());
                //loginUserList.remove(li.getId());
                lr.setStatus(true);
                lr.setMessage("Success");
            }else{
                lr.setStatus(false);
                lr.setMessage("Token Wrong");
            }
        }
        return lr;
    }

    @Override
    public VerifyResult verifyLoginToken(String verifyToken, HttpHeaders headers){
        System.out.println("[SSO Service][Verify] Verify token:" + verifyToken);
        VerifyResult vr = new VerifyResult();
        if(loginUserListRepository.findByloginToken(verifyToken) != null || verifyToken.equals("admin")){
            vr.setStatus(true);
            vr.setMessage("Verify Success.");
            System.out.println("[SSO Service][Verify] Success.Token:" + verifyToken);
        }else{
            vr.setStatus(false);
            vr.setMessage("Verify Fail.");
            System.out.println("[SSO Service][Verify] Fail.Token:" + verifyToken);
        }
        return vr;
    }

    @Override
    public FindAllAccountResult findAllAccount(HttpHeaders headers){
        FindAllAccountResult findAllAccountResult = new FindAllAccountResult();
        ArrayList<Account> accounts = accountRepository.findAll();
        for(int i = 0;i < accounts.size();i++){
            System.out.println("[SSO Service][Find All Account]" + accounts.get(i).getId());
        }
        findAllAccountResult.setStatus(true);
        findAllAccountResult.setMessage("Success.");
        findAllAccountResult.setAccountArrayList(accounts);
        return findAllAccountResult;
    }

    @Override
    public GetLoginAccountList findAllLoginAccount(HttpHeaders headers){
        ArrayList<LoginAccountValue> values = new ArrayList<>();
        for(LoginValue lv : loginUserListRepository.findAll()){
            LoginAccountValue value = new LoginAccountValue(lv.getId(),lv.getLoginToken());
            values.add(value);
        }
        GetLoginAccountList getLoginAccountList = new GetLoginAccountList();
        getLoginAccountList.setStatus(true);
        getLoginAccountList.setMessage("Success");
        getLoginAccountList.setLoginAccountList(values);
        return getLoginAccountList;
    }

    @Override
    public ModifyAccountResult saveChanges(ModifyAccountInfo modifyAccountInfo, HttpHeaders headers){
        Account existAccount = accountRepository.findByEmail(modifyAccountInfo.getNewEmail());
        ModifyAccountResult result = new ModifyAccountResult();
        if(existAccount != null && !modifyAccountInfo.getAccountId().equals(existAccount.getId().toString())){
            System.out.println("[SSO Service][Modify Info] Email exists.");
            result.setStatus(false);
            result.setMessage("Email Has Been Occupied.");
            return result;
        }

        System.out.println("[SSO Service][Modify Info] Account Id:" + modifyAccountInfo.getAccountId());
        Account oldAccount = accountRepository.findById(UUID.fromString(modifyAccountInfo.getAccountId()));

        if(oldAccount == null){
            System.out.println("[SSO Service][Modify Info] Fail.Can not found account.");
            result.setStatus(false);
            result.setMessage("Account Not Found.");
        }else{
            oldAccount.setEmail(modifyAccountInfo.getNewEmail());
            oldAccount.setPassword(modifyAccountInfo.getNewPassword());
            oldAccount.setName(modifyAccountInfo.getNewName());
            oldAccount.setGender(modifyAccountInfo.getNewGender());
            oldAccount.setDocumentType(modifyAccountInfo.getNewDocumentType());
            oldAccount.setDocumentNum(modifyAccountInfo.getNewDocumentNumber());
            accountRepository.save(oldAccount);
            //oldAccount.setPassword("");
            System.out.println("[SSO Service][ModifyInfo] Success.");
            result.setStatus(true);
            result.setMessage("Success.");
        }
        return result;
    }

    public GetAccountByIdResult getAccountById(GetAccountByIdInfo info, HttpHeaders headers){
        Account account = accountRepository.findById(UUID.fromString(info.getAccountId()));
        GetAccountByIdResult result = new GetAccountByIdResult();
        if(account == null){
            result.setStatus(false);
            result.setMessage("Order Not Found");
            result.setAccount(null);
        }else{
            result.setStatus(true);
            result.setMessage("Success");
            result.setAccount(account);
        }
        return result;
    }

    @Override
    public Contacts adminLogin(String name, String password, HttpHeaders headers) {
        Contacts c = null;
        if("adminroot".equals(name) && "adminroot".equals(password)){
            c = new Contacts();
            c.setId(UUID.fromString("1d1a11c1-11cb-1cf1-b1bb-b11111d1da1f"));
            c.setName("adminroot");
            System.out.println("[SSO Service][Admin Login successfully!]");
        }else{
            System.out.println("[SSO Service][Admin Login fail!]");
        }
        return c;
    }

    @Override
    public DeleteAccountResult deleteAccount(String accountId, HttpHeaders headers) {
        Account account = accountRepository.findById(UUID.fromString(accountId));
        DeleteAccountResult result = new DeleteAccountResult();
        if(account == null){
            result.setStatus(false);
            result.setMessage("Delete account failed!");
            result.setAccount(null);
        }
        else{
            accountRepository.deleteById(account.getId());
            result.setStatus(true);
            result.setMessage("Delete account successfully!");
            result.setAccount(account);
        }
        return result;
    }
}

