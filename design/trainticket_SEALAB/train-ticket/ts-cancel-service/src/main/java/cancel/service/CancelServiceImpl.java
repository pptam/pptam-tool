package cancel.service;

import cancel.domain.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import java.text.DecimalFormat;
import java.util.Calendar;
import java.util.Date;

@Service
public class CancelServiceImpl implements CancelService{

    @Autowired
    private RestTemplate restTemplate;

    @Override
    public CancelOrderResult cancelOrder(CancelOrderInfo info,String loginToken,String loginId, HttpHeaders headers) throws Exception{
        GetOrderByIdInfo getFromOrderInfo = new GetOrderByIdInfo();
        getFromOrderInfo.setOrderId(info.getOrderId());
        GetOrderResult orderResult = getOrderByIdFromOrder(getFromOrderInfo, headers);
        if(orderResult.isStatus() == true){
            System.out.println("[Cancel Order Service][Cancel Order] Order found G|H");
            Order order = orderResult.getOrder();
            if(order.getStatus() == OrderStatus.NOTPAID.getCode()
                    || order.getStatus() == OrderStatus.PAID.getCode() || order.getStatus() == OrderStatus.CHANGE.getCode()){

                order.setStatus(OrderStatus.CANCEL.getCode());
                ChangeOrderInfo changeOrderInfo = new ChangeOrderInfo();
                changeOrderInfo.setLoginToken(loginToken);
                changeOrderInfo.setOrder(order);

                ChangeOrderResult changeOrderResult = cancelFromOrder(changeOrderInfo, headers);
                if(changeOrderResult.isStatus() == true){
                    CancelOrderResult finalResult = new CancelOrderResult();
                    finalResult.setStatus(true);
                    finalResult.setMessage("Success.");
                    System.out.println("[Cancel Order Service][Cancel Order] Success.");
                    //Draw back money
                    String money = calculateRefund(order);
                    boolean status = drawbackMoney(money,loginId, headers);
                    if(status == true){
                        System.out.println("[Cancel Order Service][Draw Back Money] Success.");

                        GetAccountByIdInfo getAccountByIdInfo = new GetAccountByIdInfo();
                        getAccountByIdInfo.setAccountId(order.getAccountId().toString());
                        GetAccountByIdResult result = getAccount(getAccountByIdInfo, headers);
                        if(result.isStatus() == false){
                            return null;
                        }

                        NotifyInfo notifyInfo = new NotifyInfo();
                        notifyInfo.setDate(new Date().toString());


                        notifyInfo.setEmail(result.getAccount().getEmail());
                        notifyInfo.setStartingPlace(order.getFrom());
                        notifyInfo.setEndPlace(order.getTo());
                        notifyInfo.setUsername(result.getAccount().getName());
                        notifyInfo.setSeatNumber(order.getSeatNumber());
                        notifyInfo.setOrderNumber(order.getId().toString());
                        notifyInfo.setPrice(order.getPrice());
                        notifyInfo.setSeatClass(SeatClass.getNameByCode(order.getSeatClass()));
                        notifyInfo.setStartingTime(order.getTravelTime().toString());

                        sendEmail(notifyInfo, headers);

                    }else{
                        System.out.println("[Cancel Order Service][Draw Back Money] Fail.");
                    }

                    return finalResult;
                }else{
                    CancelOrderResult finalResult = new CancelOrderResult();
                    finalResult.setStatus(false);
                    finalResult.setMessage(changeOrderResult.getMessage());
                    System.out.println("[Cancel Order Service][Cancel Order] Fail.Reason:" + changeOrderResult.getMessage());
                    return finalResult;
                }

            }else{
                CancelOrderResult result = new CancelOrderResult();
                result.setStatus(false);
                result.setMessage("Order Status Cancel Not Permitted");
                System.out.println("[Cancel Order Service][Cancel Order] Order Status Not Permitted.");
                return result;
            }
        }else{
            GetOrderByIdInfo getFromOtherOrderInfo = new GetOrderByIdInfo();
            getFromOtherOrderInfo.setOrderId(info.getOrderId());
            GetOrderResult orderOtherResult = getOrderByIdFromOrderOther(getFromOtherOrderInfo, headers);
            if(orderOtherResult.isStatus() == true){
                System.out.println("[Cancel Order Service][Cancel Order] Order found Z|K|Other");

                Order order = orderOtherResult.getOrder();
                if(order.getStatus() == OrderStatus.NOTPAID.getCode()
                        || order.getStatus() == OrderStatus.PAID.getCode() || order.getStatus() == OrderStatus.CHANGE.getCode()){

                    System.out.println("[Cancel Order Service][Cancel Order] Order status ok");

                    order.setStatus(OrderStatus.CANCEL.getCode());
                    ChangeOrderInfo changeOrderInfo = new ChangeOrderInfo();
                    changeOrderInfo.setLoginToken(loginToken);
                    changeOrderInfo.setOrder(order);
                    ChangeOrderResult changeOrderResult = cancelFromOtherOrder(changeOrderInfo, headers);

                    if(changeOrderResult.isStatus() == true){
                        CancelOrderResult finalResult = new CancelOrderResult();
                        finalResult.setStatus(true);
                        finalResult.setMessage("Success.");
                        System.out.println("[Cancel Order Service][Cancel Order] Success.");
                        //Draw back money
                        String money = calculateRefund(order);
                        boolean status = drawbackMoney(money,loginId, headers);
                        if(status == true){
                            System.out.println("[Cancel Order Service][Draw Back Money] Success.");
                        }else{
                            System.out.println("[Cancel Order Service][Draw Back Money] Fail.");
                        }
                        return finalResult;
                    }else{
                        CancelOrderResult finalResult = new CancelOrderResult();
                        finalResult.setStatus(false);
                        finalResult.setMessage(changeOrderResult.getMessage());
                        System.out.println("[Cancel Order Service][Cancel Order] Fail.Reason:" + changeOrderResult.getMessage());
                        return finalResult;
                    }
                }else{
                    CancelOrderResult result = new CancelOrderResult();
                    result.setStatus(false);
                    result.setMessage("Order Status Cancel Not Permitted");
                    System.out.println("[Cancel Order Service][Cancel Order] Order Status Not Permitted.");
                    return result;
                }
            }else{
                CancelOrderResult result = new CancelOrderResult();
                result.setStatus(false);
                result.setMessage("Order Not Found");
                System.out.println("[Cancel Order Service][Cancel Order] Order Not Found.");
                return result;
            }
        }
    }

    public boolean sendEmail(NotifyInfo notifyInfo, HttpHeaders headers ){
        System.out.println("[Cancel Order Service][Send Email]");
        HttpEntity requestEntity = new HttpEntity(notifyInfo, headers);
        ResponseEntity<Boolean> re = restTemplate.exchange(
                "http://ts-notification-service:17853/notification/order_cancel_success",
                HttpMethod.POST,
                requestEntity,
                Boolean.class);
        boolean result = re.getBody();
//        boolean result = restTemplate.postForObject(
//                "http://ts-notification-service:17853/notification/order_cancel_success",
//                notifyInfo,
//                Boolean.class
//        );
        return result;
    }

    @Override
    public CalculateRefundResult calculateRefund(CancelOrderInfo info, HttpHeaders headers){
        GetOrderByIdInfo getFromOrderInfo = new GetOrderByIdInfo();
        getFromOrderInfo.setOrderId(info.getOrderId());
        GetOrderResult orderResult = getOrderByIdFromOrder(getFromOrderInfo, headers);
        if(orderResult.isStatus() == true){
            Order order = orderResult.getOrder();
            if(order.getStatus() == OrderStatus.NOTPAID.getCode()
                    || order.getStatus() == OrderStatus.PAID.getCode()){
                if(order.getStatus() == OrderStatus.NOTPAID.getCode()){
                    CalculateRefundResult result = new CalculateRefundResult();
                    result.setStatus(true);
                    result.setMessage("Success");
                    result.setRefund("0");
                    System.out.println("[Cancel Order][Refund Price] From Order Service.Not Paid.");
                    return result;
                }else{
                    CalculateRefundResult result = new CalculateRefundResult();
                    result.setStatus(true);
                    result.setMessage("Success");
                    result.setRefund(calculateRefund(order));
                    System.out.println("[Cancel Order][Refund Price] From Order Service.Paid.");
                    return result;
                }
            }else{
                CalculateRefundResult result = new CalculateRefundResult();
                result.setStatus(false);
                result.setMessage("Order Status Cancel Not Permitted");
                result.setRefund("error");
                System.out.println("[Cancel Order][Refund Price] Order. Cancel Not Permitted.");

                return result;
            }
        }else{
            GetOrderByIdInfo getFromOtherOrderInfo = new GetOrderByIdInfo();
            getFromOtherOrderInfo.setOrderId(info.getOrderId());
            GetOrderResult orderOtherResult = getOrderByIdFromOrderOther(getFromOtherOrderInfo, headers);
            if(orderOtherResult.isStatus() == true){
                Order order = orderOtherResult.getOrder();
                if(order.getStatus() == OrderStatus.NOTPAID.getCode()
                        || order.getStatus() == OrderStatus.PAID.getCode()){
                    if(order.getStatus() == OrderStatus.NOTPAID.getCode()){
                        CalculateRefundResult result = new CalculateRefundResult();
                        result.setStatus(true);
                        result.setMessage("Success");
                        result.setRefund("0");
                        System.out.println("[Cancel Order][Refund Price] From Order Other Service.Not Paid.");
                        return result;
                    }else{
                        CalculateRefundResult result = new CalculateRefundResult();
                        result.setStatus(true);
                        result.setMessage("Success");
                        result.setRefund(calculateRefund(order));
                        System.out.println("[Cancel Order][Refund Price] From Order Other Service.Paid.");
                        return result;
                    }
                }else{
                    CalculateRefundResult result = new CalculateRefundResult();
                    result.setStatus(false);
                    result.setMessage("Order Status Cancel Not Permitted");
                    result.setRefund("error");
                    System.out.println("[Cancel Order][Refund Price] Order Other. Cancel Not Permitted.");
                    return result;
                }
            }else{
                CalculateRefundResult result = new CalculateRefundResult();
                result.setStatus(false);
                result.setMessage("Order Not Found");
                result.setRefund("error");
                System.out.println("[Cancel Order][Refund Price] Order not found.");
                return result;
            }
        }
    }

    private String calculateRefund(Order order){
        if(order.getStatus() == OrderStatus.NOTPAID.getCode()){
            return "0.00";
        }
        System.out.println("[Cancel Order] Order Travel Date:" + order.getTravelDate().toString());
        Date nowDate = new Date();
        Calendar cal = Calendar.getInstance();
        cal.setTime(order.getTravelDate());
        int year = cal.get(Calendar.YEAR);
        int month = cal.get(Calendar.MONTH);
        int day = cal.get(Calendar.DAY_OF_MONTH);
        Calendar cal2 = Calendar.getInstance();
        cal2.setTime(order.getTravelTime());
        int hour = cal2.get(Calendar.HOUR);
        int minute = cal2.get(Calendar.MINUTE);
        int second = cal2.get(Calendar.SECOND);
        Date startTime = new Date(year,
                                  month,
                                  day,
                                  hour,
                                  minute,
                                  second);
        System.out.println("[Cancel Order] nowDate  :" + nowDate.toString());
        System.out.println("[Cancel Order] startTime:" + startTime.toString());
        if(nowDate.after(startTime)){
            System.out.println("[Cancel Order] Ticket expire refund 0");
            return "0";
        }else{
            double totalPrice = Double.parseDouble(order.getPrice());
            double price = totalPrice * 0.8;
            DecimalFormat priceFormat = new java.text.DecimalFormat("0.00");
            String str = priceFormat.format(price);
            System.out.println("[Cancel Order]calculate refund - " + str);
            return str;
        }
    }


    private ChangeOrderResult cancelFromOrder(ChangeOrderInfo info,  HttpHeaders headers){
        System.out.println("[Cancel Order Service][Change Order Status] Changing....");
        ChangeOrderResult result = restTemplate.postForObject("http://ts-order-service:12031/order/update",info,ChangeOrderResult.class);
        return result;
    }

    private ChangeOrderResult cancelFromOtherOrder(ChangeOrderInfo info, HttpHeaders headers){
        System.out.println("[Cancel Order Service][Change Order Status] Changing....");
        HttpEntity requestEntity = new HttpEntity(info, headers);
        ResponseEntity<ChangeOrderResult> re = restTemplate.exchange(
                "http://ts-order-other-service:12032/orderOther/update",
                HttpMethod.POST,
                requestEntity,
                ChangeOrderResult.class);
        ChangeOrderResult result = re.getBody();
//        ChangeOrderResult result = restTemplate.postForObject("http://ts-order-other-service:12032/orderOther/update",info,ChangeOrderResult.class);
        return result;
    }

    public boolean drawbackMoney(String money,String userId, HttpHeaders headers){
        System.out.println("[Cancel Order Service][Draw Back Money] Draw back money...");
        DrawBackInfo info = new DrawBackInfo();
        info.setMoney(money);
        info.setUserId(userId);
        HttpEntity requestEntity = new HttpEntity(info, headers);
        ResponseEntity<String> re = restTemplate.exchange(
                "http://ts-inside-payment-service:18673/inside_payment/drawBack",
                HttpMethod.POST,
                requestEntity,
               String.class);
        String result = re.getBody();
//        String result = restTemplate.postForObject("http://ts-inside-payment-service:18673/inside_payment/drawBack",info,String.class);
        if(result.equals("true")){
            return true;
        }else{
            return false;
        }
    }

    public GetAccountByIdResult getAccount(GetAccountByIdInfo info, HttpHeaders headers){
        System.out.println("[Cancel Order Service][Get By Id]");
        HttpEntity requestEntity = new HttpEntity(info, headers);
        ResponseEntity<GetAccountByIdResult> re = restTemplate.exchange(
                "http://ts-sso-service:12349/account/findById",
                HttpMethod.POST,
                requestEntity,
                GetAccountByIdResult.class);
        GetAccountByIdResult result = re.getBody();
//        GetAccountByIdResult result = restTemplate.postForObject(
//                "http://ts-sso-service:12349/account/findById",
//                info,
//                GetAccountByIdResult.class
//        );
        return result;
    }

    private GetOrderResult getOrderByIdFromOrder(GetOrderByIdInfo info, HttpHeaders headers){
        System.out.println("[Cancel Order Service][Get Order] Getting....");
        HttpEntity requestEntity = new HttpEntity(info, headers);
        ResponseEntity<GetOrderResult> re = restTemplate.exchange(
                "http://ts-order-service:12031/order/getById/",
                HttpMethod.POST,
                requestEntity,
                GetOrderResult.class);
        GetOrderResult cor = re.getBody();
//        GetOrderResult cor = restTemplate.postForObject(
//                "http://ts-order-service:12031/order/getById/"
//                ,info,GetOrderResult.class);
        return cor;
    }

    private GetOrderResult getOrderByIdFromOrderOther(GetOrderByIdInfo info, HttpHeaders headers){
        System.out.println("[Cancel Order Service][Get Order] Getting....");
        HttpEntity requestEntity = new HttpEntity(info, headers);
        ResponseEntity<GetOrderResult> re = restTemplate.exchange(
                "http://ts-order-other-service:12032/orderOther/getById/",
                HttpMethod.POST,
                requestEntity,
                GetOrderResult.class);
        GetOrderResult cor = re.getBody();
//        GetOrderResult cor = restTemplate.postForObject(
//                "http://ts-order-other-service:12032/orderOther/getById/"
//                ,info,GetOrderResult.class);
        return cor;
    }

}
