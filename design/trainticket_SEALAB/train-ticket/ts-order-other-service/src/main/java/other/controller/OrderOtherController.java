package other.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import other.domain.*;
import other.service.OrderOtherService;
import java.util.ArrayList;

@RestController
public class OrderOtherController {

    @Autowired
    private OrderOtherService orderService;

    @Autowired
    private RestTemplate restTemplate;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home() {
        return "Welcome to [ Order Other Service ] !";
    }

    /***************************For Normal Use***************************/

    @RequestMapping(value="/orderOther/getTicketListByDateAndTripId", method = RequestMethod.POST)
    public LeftTicketInfo getTicketListByDateAndTripId(@RequestBody SeatRequest seatRequest, @RequestHeader HttpHeaders headers){
        System.out.println("[Order Other Service][Get Sold Ticket] Date:" + seatRequest.getTravelDate().toString());
        return orderService.getSoldTickets(seatRequest, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/orderOther/create", method = RequestMethod.POST)
    public CreateOrderResult createNewOrder(@RequestBody CreateOrderInfo coi, @RequestHeader HttpHeaders headers){
        System.out.println("[Order Other Service][Create Order] Create Order form " + coi.getOrder().getFrom() + " --->"
                + coi.getOrder().getTo() + " at " + coi.getOrder().getTravelDate());
        VerifyResult tokenResult = verifySsoLogin(coi.getLoginToken(), headers);
        if(tokenResult.isStatus() == true){
            System.out.println("[Order Other Service][Verify Login] Success");
            return orderService.create(coi.getOrder(), headers);
        }else{
            System.out.println("[Order Other Service][Verify Login] Fail");
            CreateOrderResult cor = new CreateOrderResult();
            cor.setStatus(false);
            cor.setMessage("Not Login");
            cor.setOrder(null);
            return cor;
        }
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/orderOther/adminAddOrder", method = RequestMethod.POST)
    public AddOrderResult addcreateNewOrder(@RequestBody Order order, @RequestHeader HttpHeaders headers){
        return orderService.addNewOrder(order, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/orderOther/query", method = RequestMethod.POST)
    public ArrayList<Order> queryOrders(@RequestBody QueryInfo qi,@CookieValue String loginId,@CookieValue String loginToken, @RequestHeader HttpHeaders headers){
        System.out.println("[Order Other Service][Query Orders] Query Orders for " + loginId);
        VerifyResult tokenResult = verifySsoLogin(loginToken, headers);
        if(tokenResult.isStatus() == true){
            System.out.println("[Order Other Service][Verify Login] Success");
            return orderService.queryOrders(qi,loginId, headers);
        }else{
            System.out.println("[Order Other Service][Verify Login] Fail");
            return new ArrayList<Order>();
        }
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/orderOther/queryForRefresh", method = RequestMethod.POST)
    public ArrayList<Order> queryOrdersForRefresh(@RequestBody QueryInfo qi,@CookieValue String loginId,@CookieValue String loginToken, @RequestHeader HttpHeaders headers){
        System.out.println("[Order Other Service][Query Orders] Query Orders for " + loginId);
        VerifyResult tokenResult = verifySsoLogin(loginToken, headers);
        if(tokenResult.isStatus() == true){
            System.out.println("[Order Other Service][Verify Login] Success");
            return orderService.queryOrdersForRefresh(qi,loginId, headers);
        }else{
            System.out.println("[Order Other Service][Verify Login] Fail");
            return new ArrayList<Order>();
        }
    }


    @CrossOrigin(origins = "*")
    @RequestMapping(path="/orderOther/calculate", method = RequestMethod.POST)
    public CalculateSoldTicketResult calculateSoldTicket(@RequestBody CalculateSoldTicketInfo csti, @RequestHeader HttpHeaders headers){
        System.out.println("[Order Other Service][Calculate Sold Tickets] Date:" + csti.getTravelDate() + " TrainNumber:"
                + csti.getTrainNumber());
        return orderService.queryAlreadySoldOrders(csti, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path="/orderOther/price", method = RequestMethod.POST)
    public GetOrderPriceResult getOrderPrice(@RequestBody GetOrderPrice info, @RequestHeader HttpHeaders headers){
        System.out.println("[Order Other Service][Get Order Price] Order Id:" + info.getOrderId());
        return orderService.getOrderPrice(info, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path="/orderOther/payOrder", method = RequestMethod.POST)
    public PayOrderResult payOrder(@RequestBody PayOrderInfo info, @RequestHeader HttpHeaders headers){
        System.out.println("[Order Other Service][Pay Order] Order Id:" + info.getOrderId());
        return orderService.payOrder(info, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path="/orderOther/getById", method = RequestMethod.POST)
    public GetOrderResult getOrderById(@RequestBody GetOrderByIdInfo info, @RequestHeader HttpHeaders headers){
        System.out.println("[Order Other Service][Get Order By Id] Order Id:" + info.getOrderId());
        return orderService.getOrderById(info, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path="/orderOther/modifyOrderStatus", method = RequestMethod.POST)
    public ModifyOrderStatusResult modifyOrder(@RequestBody ModifyOrderStatusInfo info, @RequestHeader HttpHeaders headers){
        System.out.println("[Order Other Service][Modify Order Status] Order Id:" + info.getOrderId());
        return orderService.modifyOrder(info, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path="/getOrderOtherInfoForSecurity", method = RequestMethod.POST)
    public GetOrderInfoForSecurityResult securityInfoCheck(@RequestBody GetOrderInfoForSecurity info, @RequestHeader HttpHeaders headers){
        System.out.println("[Order Other Service][Security Info Get]");
        return orderService.checkSecurityAboutOrder(info, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/orderOther/update", method = RequestMethod.POST)
    public ChangeOrderResult saveOrderInfo(@RequestBody ChangeOrderInfo orderInfo, @RequestHeader HttpHeaders headers){
        VerifyResult tokenResult = verifySsoLogin(orderInfo.getLoginToken(),headers);
        if(tokenResult.isStatus() == true){
            System.out.println("[Order Other Service][Verify Login] Success");
            return orderService.saveChanges(orderInfo.getOrder(), headers);
        }else{
            System.out.println("[Order Other Service][Verify Login] Fail");
            ChangeOrderResult cor = new ChangeOrderResult();
            cor.setStatus(false);
            cor.setMessage("Not Login");
            cor.setOrder(null);
            return cor;
        }
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path = "/orderOther/adminUpdate", method = RequestMethod.POST)
    public UpdateOrderResult updateOrder(@RequestBody Order order, @RequestHeader HttpHeaders headers){
        return orderService.updateOrder(order, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(path="/orderOther/delete",method = RequestMethod.POST)
    public DeleteOrderResult deleteOrder(@RequestBody DeleteOrderInfo info, @RequestHeader HttpHeaders headers){
        System.out.println("[Order Other Service][Delete Order] Order Id:" + info.getOrderId());
        return orderService.deleteOrder(info, headers);
    }


    /***************For super admin(Single Service Test*******************/

    @CrossOrigin(origins = "*")
    @RequestMapping(path="/orderOther/findAll", method = RequestMethod.GET)
    public QueryOrderResult findAllOrder(@RequestHeader HttpHeaders headers){
        System.out.println("[Order Other Service][Find All Order]");
        return orderService.getAllOrders(headers);
    }

    private VerifyResult verifySsoLogin(String loginToken, @RequestHeader HttpHeaders headers){
        System.out.println("[Order Service][Verify Login] Verifying....");

        HttpEntity requestTokenResult = new HttpEntity(null,headers);
        ResponseEntity<VerifyResult> reTokenResult  = restTemplate.exchange(
                "http://ts-sso-service:12349/verifyLoginToken/" + loginToken,
                HttpMethod.GET,
                requestTokenResult,
                VerifyResult.class);
        VerifyResult tokenResult = reTokenResult.getBody();
//        VerifyResult tokenResult = restTemplate.getForObject(
//                "http://ts-sso-service:12349/verifyLoginToken/" + loginToken,
//                VerifyResult.class);


        return tokenResult;
    }
}
