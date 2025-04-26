package adminorder.service;

import adminorder.domain.bean.DeleteOrderInfo;
import adminorder.domain.bean.Order;
import adminorder.domain.request.AddOrderRequest;
import adminorder.domain.request.DeleteOrderRequest;
import adminorder.domain.request.UpdateOrderRequest;
import adminorder.domain.response.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.ArrayList;

@Service
public class AdminOrderServiceImpl implements AdminOrderService {
    @Autowired
    private RestTemplate restTemplate;

    @Override
    public GetAllOrderResult getAllOrders(String id, HttpHeaders headers) {
        if(checkId(id)){
            System.out.println("[Admin Order Service][Get All Orders]");
            //Get all of the orders
            ArrayList<Order> orders = new ArrayList<Order>();
            //From ts-order-service
            HttpEntity requestEntity = new HttpEntity(headers);
            ResponseEntity<QueryOrderResult> re = restTemplate.exchange(
                    "http://ts-order-service:12031/order/findAll",
                    HttpMethod.GET,
                    requestEntity,
                    QueryOrderResult.class);
            QueryOrderResult result = re.getBody();
//            QueryOrderResult result = restTemplate.getForObject(
//                    "http://ts-order-service:12031/order/findAll",
//                    QueryOrderResult.class);
            if(result.isStatus()){
                System.out.println("[Admin Order Service][Get Orders From ts-order-service successfully!]");
                orders.addAll(result.getOrders());
            }
            else
                System.out.println("[Admin Order Service][Get Orders From ts-order-service fail!]");
            //From ts-order-other-service
            HttpEntity requestEntity2 = new HttpEntity(headers);
            ResponseEntity<QueryOrderResult> re2 = restTemplate.exchange(
                    "http://ts-order-other-service:12032/orderOther/findAll",
                    HttpMethod.GET,
                    requestEntity2,
                    QueryOrderResult.class);
            result = re2.getBody();
//            result = restTemplate.getForObject(
//                    "http://ts-order-other-service:12032/orderOther/findAll",
//                    QueryOrderResult.class);
            if(result.isStatus()){
                System.out.println("[Admin Order Service][Get Orders From ts-order-other-service successfully!]");
                orders.addAll(result.getOrders());
            }
            else
                System.out.println("[Admin Order Service][Get Orders From ts-order-other-service fail!]");
            //Return orders
            GetAllOrderResult getAllOrderResult = new GetAllOrderResult();
            getAllOrderResult.setStatus(true);
            getAllOrderResult.setMessage("Get the orders successfully!");
            getAllOrderResult.setOrders(orders);
            return getAllOrderResult;
        }
        else{
            System.out.println("[Admin Order Service][Wrong Admin ID]");
            GetAllOrderResult result = new GetAllOrderResult();
            result.setStatus(false);
            result.setMessage("The loginId is Wrong: " + id);
            return result;
        }
    }

    @Override
    public DeleteOrderResult deleteOrder(DeleteOrderRequest request, HttpHeaders headers) {
        if(checkId(request.getLoginid())){
            DeleteOrderResult deleteOrderResult ;

            DeleteOrderInfo deleteOrderInfo = new DeleteOrderInfo();
            deleteOrderInfo.setOrderId(request.getOrderId());

            if(request.getTrainNumber().startsWith("G") || request.getTrainNumber().startsWith("D") ){
                System.out.println("[Admin Order Service][Delete Order]");
                HttpEntity requestEntity = new HttpEntity(deleteOrderInfo, headers);
                ResponseEntity<DeleteOrderResult> re = restTemplate.exchange(
                        "http://ts-order-service:12031/order/delete",
                        HttpMethod.POST,
                        requestEntity,
                        DeleteOrderResult.class);
                deleteOrderResult = re.getBody();
//                deleteOrderResult = restTemplate.postForObject(
//                        "http://ts-order-service:12031/order/delete", deleteOrderInfo,DeleteOrderResult.class);
            }
            else{
                System.out.println("[Admin Order Service][Delete Order Other]");
                HttpEntity requestEntity = new HttpEntity(deleteOrderInfo, headers);
                ResponseEntity<DeleteOrderResult> re = restTemplate.exchange(
                        "http://ts-order-other-service:12032/orderOther/delete",
                        HttpMethod.POST,
                        requestEntity,
                        DeleteOrderResult.class);
                deleteOrderResult = re.getBody();
//                deleteOrderResult = restTemplate.postForObject(
//                        "http://ts-order-other-service:12032/orderOther/delete", deleteOrderInfo,DeleteOrderResult.class);
            }
            return deleteOrderResult;
        }
        else{
            System.out.println("[Admin Order Service][Wrong Admin ID]");
            DeleteOrderResult result = new DeleteOrderResult();
            result.setStatus(false);
            result.setMessage("The loginId is Wrong: " + request.getLoginid());
            return result;
        }
    }

    @Override
    public UpdateOrderResult updateOrder(UpdateOrderRequest request, HttpHeaders headers) {
        if(checkId(request.getLoginid())){
            UpdateOrderResult updateOrderResult ;
            if(request.getOrder().getTrainNumber().startsWith("G") || request.getOrder().getTrainNumber().startsWith("D") ){
                System.out.println("[Admin Order Service][Update Order]");
                HttpEntity requestEntity = new HttpEntity(request.getOrder(), headers);
                ResponseEntity<UpdateOrderResult> re = restTemplate.exchange(
                        "http://ts-order-service:12031/order/adminUpdate",
                        HttpMethod.POST,
                        requestEntity,
                        UpdateOrderResult.class);
                updateOrderResult = re.getBody();
//                updateOrderResult = restTemplate.postForObject(
//                        "http://ts-order-service:12031/order/adminUpdate", request.getOrder() ,UpdateOrderResult.class);
            }
            else{
                System.out.println("[Admin Order Service][Add New Order Other]");
                HttpEntity requestEntity = new HttpEntity(request.getOrder(), headers);
                ResponseEntity<UpdateOrderResult> re = restTemplate.exchange(
                        "http://ts-order-other-service:12032/orderOther/adminUpdate",
                        HttpMethod.POST,
                        requestEntity,
                        UpdateOrderResult.class);
                updateOrderResult = re.getBody();
//                updateOrderResult = restTemplate.postForObject(
//                        "http://ts-order-other-service:12032/orderOther/adminUpdate", request.getOrder() ,UpdateOrderResult.class);
            }
            return updateOrderResult;
        }
        else{
            System.out.println("[Admin Order Service][Wrong Admin ID]");
            UpdateOrderResult result = new UpdateOrderResult();
            result.setStatus(false);
            result.setMessage("The loginId is Wrong: " + request.getLoginid());
            return result;
        }
    }

    @Override
    public AddOrderResult addOrder(AddOrderRequest request, HttpHeaders headers) {
        if(checkId(request.getLoginid())){
            AddOrderResult addOrderResult;
            if(request.getOrder().getTrainNumber().startsWith("G") || request.getOrder().getTrainNumber().startsWith("D") ){
                System.out.println("[Admin Order Service][Add New Order]");
                HttpEntity requestEntity = new HttpEntity(request.getOrder(), headers);
                ResponseEntity< AddOrderResult> re = restTemplate.exchange(
                        "http://ts-order-service:12031/order/adminAddOrder",
                        HttpMethod.POST,
                        requestEntity,
                        AddOrderResult.class);
                addOrderResult = re.getBody();
//                addOrderResult = restTemplate.postForObject(
//                        "http://ts-order-service:12031/order/adminAddOrder", request.getOrder() ,AddOrderResult.class);
            }
            else{
                System.out.println("[Admin Order Service][Add New Order Other]");
                HttpEntity requestEntity = new HttpEntity(request.getOrder(), headers);
                ResponseEntity< AddOrderResult> re = restTemplate.exchange(
                        "http://ts-order-other-service:12032/orderOther/adminAddOrder",
                        HttpMethod.POST,
                        requestEntity,
                        AddOrderResult.class);
                addOrderResult = re.getBody();
//                addOrderResult = restTemplate.postForObject(
//                        "http://ts-order-other-service:12032/orderOther/adminAddOrder", request.getOrder() ,AddOrderResult.class);
            }
            return addOrderResult;
        }
        else{
            System.out.println("[Admin Order Service][Wrong Admin ID]");
            AddOrderResult result = new AddOrderResult();
            result.setStatus(false);
            result.setMessage("The loginId is Wrong: " + request.getLoginid());
            return result;
        }
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
