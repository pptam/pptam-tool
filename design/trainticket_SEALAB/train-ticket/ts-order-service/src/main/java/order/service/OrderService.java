package order.service;

import order.domain.*;
import org.springframework.http.HttpHeaders;

import java.util.ArrayList;
import java.util.UUID;

public interface OrderService {

    Order findOrderById(UUID id, HttpHeaders headers);

    CreateOrderResult create(Order newOrder, HttpHeaders headers);

    ChangeOrderResult saveChanges(Order order, HttpHeaders headers);

    CancelOrderResult cancelOrder(CancelOrderInfo coi, HttpHeaders headers);

    ArrayList<Order> queryOrders(QueryInfo qi,String accountId, HttpHeaders headers);

    ArrayList<Order> queryOrdersForRefresh(QueryInfo qi,String accountId, HttpHeaders headers);

    OrderAlterResult alterOrder(OrderAlterInfo oai, HttpHeaders headers);

    CalculateSoldTicketResult queryAlreadySoldOrders(CalculateSoldTicketInfo csti, HttpHeaders headers);

    QueryOrderResult getAllOrders(HttpHeaders headers);

    ModifyOrderStatusResult modifyOrder(ModifyOrderStatusInfo info, HttpHeaders headers);

    GetOrderPriceResult getOrderPrice(GetOrderPrice info, HttpHeaders headers);

    PayOrderResult payOrder(PayOrderInfo info, HttpHeaders headers);

    GetOrderResult getOrderById(GetOrderByIdInfo info, HttpHeaders headers);

    GetOrderInfoForSecurityResult checkSecurityAboutOrder(GetOrderInfoForSecurity info, HttpHeaders headers);

    void initOrder(Order order, HttpHeaders headers);

    DeleteOrderResult deleteOrder(DeleteOrderInfo info, HttpHeaders headers);

    LeftTicketInfo getSoldTickets(SeatRequest seatRequest, HttpHeaders headers);

    AddOrderResult addNewOrder(Order order, HttpHeaders headers);

    UpdateOrderResult updateOrder(Order order, HttpHeaders headers);
}
