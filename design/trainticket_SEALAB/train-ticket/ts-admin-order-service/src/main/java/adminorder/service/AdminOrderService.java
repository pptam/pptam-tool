package adminorder.service;

import adminorder.domain.request.AddOrderRequest;
import adminorder.domain.request.DeleteOrderRequest;
import adminorder.domain.request.UpdateOrderRequest;
import adminorder.domain.response.AddOrderResult;
import adminorder.domain.response.DeleteOrderResult;
import adminorder.domain.response.GetAllOrderResult;
import adminorder.domain.response.UpdateOrderResult;
import org.springframework.http.HttpHeaders;

public interface AdminOrderService {
    GetAllOrderResult getAllOrders(String id, HttpHeaders headers);
    DeleteOrderResult deleteOrder(DeleteOrderRequest request, HttpHeaders headers);
    UpdateOrderResult updateOrder(UpdateOrderRequest request, HttpHeaders headers);
    AddOrderResult addOrder(AddOrderRequest request, HttpHeaders headers);
}
