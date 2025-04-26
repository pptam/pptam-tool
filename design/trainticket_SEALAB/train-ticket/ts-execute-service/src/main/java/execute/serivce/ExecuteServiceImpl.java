package execute.serivce;

import execute.domain.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class ExecuteServiceImpl implements ExecuteService{

    @Autowired
    private RestTemplate restTemplate;

    @Override
    public TicketExecuteResult ticketExecute(TicketExecuteInfo info, HttpHeaders headers){
        //1.获取订单信息
        GetOrderByIdInfo getOrderByIdInfo = new GetOrderByIdInfo();
        getOrderByIdInfo.setOrderId(info.getOrderId());
        GetOrderResult resultFromOrder = getOrderByIdFromOrder(getOrderByIdInfo, headers);
        TicketExecuteResult result = new TicketExecuteResult();
        Order order;
        if(resultFromOrder.isStatus() == true){
            order = resultFromOrder.getOrder();
            //2.检查订单是否可以进站
            if(order.getStatus() != OrderStatus.COLLECTED.getCode()){
                result.setStatus(false);
                result.setMessage("Order Status Wrong");
                return result;
            }
            //3.确认进站 请求修改订单信息
            ModifyOrderStatusInfo executeInfo = new ModifyOrderStatusInfo();
            executeInfo.setOrderId(info.getOrderId());
            executeInfo.setStatus(OrderStatus.USED.getCode());
            ModifyOrderStatusResult resultExecute = executeOrder(executeInfo, headers);
            if(resultExecute.isStatus() == true){
                result.setStatus(true);
                result.setMessage("Success.");
                return result;
            }else{
                result.setStatus(false);
                result.setMessage(resultExecute.getMessage());
                return result;
            }
        }else{
            resultFromOrder = getOrderByIdFromOrderOther(getOrderByIdInfo, headers);
            if(resultFromOrder.isStatus() == true){
                order = resultFromOrder.getOrder();
                //2.检查订单是否可以进站
                if(order.getStatus() != OrderStatus.COLLECTED.getCode()){
                    result.setStatus(false);
                    result.setMessage("Order Status Wrong");
                    return result;
                }
                //3.确认进站 请求修改订单信息
                ModifyOrderStatusInfo executeInfo = new  ModifyOrderStatusInfo();
                executeInfo.setOrderId(info.getOrderId());
                executeInfo.setStatus(OrderStatus.USED.getCode());
                ModifyOrderStatusResult resultExecute = executeOrderOther(executeInfo, headers);
                if(resultExecute.isStatus() == true){
                    result.setStatus(true);
                    result.setMessage("Success.");
                    return result;
                }else{
                    result.setStatus(false);
                    result.setMessage(resultExecute.getMessage());
                    return result;
                }
            }else{
                result.setStatus(false);
                result.setMessage("Order Not Found");
                return result;
            }
        }
    }

    @Override
    public TicketExecuteResult ticketCollect(TicketExecuteInfo info, HttpHeaders headers){
        //1.获取订单信息
        GetOrderByIdInfo getOrderByIdInfo = new GetOrderByIdInfo();
        getOrderByIdInfo.setOrderId(info.getOrderId());
        GetOrderResult resultFromOrder = getOrderByIdFromOrder(getOrderByIdInfo, headers);
        TicketExecuteResult result = new TicketExecuteResult();
        Order order;
        if(resultFromOrder.isStatus() == true){
            order = resultFromOrder.getOrder();
            //2.检查订单是否可以进站
            if(order.getStatus() != OrderStatus.PAID.getCode()){
                result.setStatus(false);
                result.setMessage("Order Status Wrong");
                return result;
            }
            //3.确认进站 请求修改订单信息
            ModifyOrderStatusInfo executeInfo = new ModifyOrderStatusInfo();
            executeInfo.setOrderId(info.getOrderId());
            executeInfo.setStatus(OrderStatus.COLLECTED.getCode());
            ModifyOrderStatusResult resultExecute = executeOrder(executeInfo, headers);
            if(resultExecute.isStatus() == true){
                result.setStatus(true);
                result.setMessage("Success.");
                return result;
            }else{
                result.setStatus(false);
                result.setMessage(resultExecute.getMessage());
                return result;
            }
        }else{
            resultFromOrder = getOrderByIdFromOrderOther(getOrderByIdInfo, headers);
            if(resultFromOrder.isStatus() == true){
                order = resultFromOrder.getOrder();
                //2.检查订单是否可以进站
                if(order.getStatus() != OrderStatus.PAID.getCode()){
                    result.setStatus(false);
                    result.setMessage("Order Status Wrong");
                    return result;
                }
                //3.确认进站 请求修改订单信息
                ModifyOrderStatusInfo executeInfo = new ModifyOrderStatusInfo();
                executeInfo.setOrderId(info.getOrderId());
                executeInfo.setStatus(OrderStatus.COLLECTED.getCode());
                ModifyOrderStatusResult resultExecute = executeOrderOther(executeInfo, headers);
                if(resultExecute.isStatus() == true){
                    result.setStatus(true);
                    result.setMessage("Success.");
                    return result;
                }else{
                    result.setStatus(false);
                    result.setMessage(resultExecute.getMessage());
                    return result;
                }
            }else{
                result.setStatus(false);
                result.setMessage("Order Not Found");
                return result;
            }
        }
    }


    private ModifyOrderStatusResult executeOrder(ModifyOrderStatusInfo info, HttpHeaders headers){
        System.out.println("[Execute Service][Execute Order] Executing....");
        HttpEntity requestEntity = new HttpEntity(info, headers);
        ResponseEntity<ModifyOrderStatusResult> re = restTemplate.exchange(
                "http://ts-order-service:12031/order/modifyOrderStatus",
                HttpMethod.POST,
                requestEntity,
                ModifyOrderStatusResult.class);
        ModifyOrderStatusResult cor = re.getBody();
//        ModifyOrderStatusResult cor = restTemplate.postForObject(
//                "http://ts-order-service:12031/order/modifyOrderStatus"
//                ,info,ModifyOrderStatusResult.class);
        return cor;
    }

    private ModifyOrderStatusResult executeOrderOther(ModifyOrderStatusInfo info, HttpHeaders headers){
        System.out.println("[Execute Service][Execute Order] Executing....");
        HttpEntity requestEntity = new HttpEntity(info, headers);
        ResponseEntity<ModifyOrderStatusResult> re = restTemplate.exchange(
                "http://ts-order-other-service:12032/orderOther/modifyOrderStatus",
                HttpMethod.POST,
                requestEntity,
                ModifyOrderStatusResult.class);
        ModifyOrderStatusResult cor = re.getBody();
//        ModifyOrderStatusResult cor = restTemplate.postForObject(
//                "http://ts-order-other-service:12032/order/modifyOrderStatus"
//                ,info,ModifyOrderStatusResult.class);
        return cor;
    }

    private GetOrderResult getOrderByIdFromOrder(GetOrderByIdInfo info, HttpHeaders headers){
        System.out.println("[Execute Service][Get Order] Getting....");
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
        System.out.println("[Execute Service][Get Order] Getting....");
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
