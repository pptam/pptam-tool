package adminuser.controller;

import adminuser.domain.request.AddAccountRequest;
import adminuser.domain.request.DeleteAccountRequest;
import adminuser.domain.request.UpdateAccountRequest;
import adminuser.domain.response.DeleteAccountResult;
import adminuser.domain.response.FindAllAccountResult;
import adminuser.domain.response.ModifyAccountResult;
import adminuser.domain.response.RegisterResult;
import adminuser.service.AdminUserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.*;

@RestController
public class AdminUserController {
    @Autowired
    AdminUserService adminUserService;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home(@RequestHeader HttpHeaders headers) {
        return "Welcome to [ AdminUser Service ] !";
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/adminuser/findAll/{id}", method = RequestMethod.GET)
    public FindAllAccountResult getAllUsers(@PathVariable String id, @RequestHeader HttpHeaders headers){
        return adminUserService.getAllUsers(id, headers);
    }

    @RequestMapping(value = "/adminuser/addUser", method= RequestMethod.POST)
    public RegisterResult addUser(@RequestBody AddAccountRequest request, @RequestHeader HttpHeaders headers){
        return adminUserService.addUser(request, headers);
    }

    @RequestMapping(value = "/adminuser/updateUser", method= RequestMethod.POST)
    public ModifyAccountResult updateOrder(@RequestBody UpdateAccountRequest request, @RequestHeader HttpHeaders headers){
        return adminUserService.updateUser(request, headers);
    }

    @RequestMapping(value = "/adminuser/deleteUser", method= RequestMethod.POST)
    public DeleteAccountResult deleteOrder(@RequestBody DeleteAccountRequest request, @RequestHeader HttpHeaders headers){
        return adminUserService.deleteUser(request, headers);
    }
}
