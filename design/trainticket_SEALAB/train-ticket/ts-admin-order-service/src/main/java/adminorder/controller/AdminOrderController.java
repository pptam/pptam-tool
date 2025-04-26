package adminorder.controller;

import adminorder.domain.request.AddOrderRequest;
import adminorder.domain.request.DeleteOrderRequest;
import adminorder.domain.request.UpdateOrderRequest;
import adminorder.domain.response.AddOrderResult;
import adminorder.domain.response.DeleteOrderResult;
import adminorder.domain.response.GetAllOrderResult;
import adminorder.domain.response.UpdateOrderResult;
import adminorder.service.AdminOrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.*;

@RestController
public class AdminOrderController {

    @Autowired
    AdminOrderService adminOrderService;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home(@RequestHeader HttpHeaders headers) {
        return "Welcome to [ AdminOrder Service ] !";
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/adminorder/findAll/{id}", method = RequestMethod.GET)
    public GetAllOrderResult getAllOrders(@PathVariable String id, @RequestHeader HttpHeaders headers){
        return adminOrderService.getAllOrders(id, headers);
    }

    @RequestMapping(value = "/adminorder/addOrder", method= RequestMethod.POST)
    public AddOrderResult addOrder(@RequestBody AddOrderRequest request, @RequestHeader HttpHeaders headers){
        return adminOrderService.addOrder(request, headers);
    }

    @RequestMapping(value = "/adminorder/updateOrder", method= RequestMethod.POST)
    public UpdateOrderResult updateOrder(@RequestBody UpdateOrderRequest request, @RequestHeader HttpHeaders headers){
        return adminOrderService.updateOrder(request, headers);
    }

    @RequestMapping(value = "/adminorder/deleteOrder", method= RequestMethod.POST)
    public DeleteOrderResult deleteOrder(@RequestBody DeleteOrderRequest request, @RequestHeader HttpHeaders headers){
        return adminOrderService.deleteOrder(request, headers);
    }

}
