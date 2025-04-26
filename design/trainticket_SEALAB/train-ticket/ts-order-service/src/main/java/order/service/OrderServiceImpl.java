package order.service;

import order.domain.*;
import order.repository.OrderRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.*;

@Service
public class OrderServiceImpl implements OrderService{

    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private RestTemplate restTemplate;

    @Override
    public LeftTicketInfo getSoldTickets(SeatRequest seatRequest, HttpHeaders headers){
        ArrayList<Order> list = orderRepository.findByTravelDateAndTrainNumber(seatRequest.getTravelDate(),
                seatRequest.getTrainNumber());
        Set ticketSet = new HashSet();
        for(Order tempOrder : list){
            Ticket ticket = new Ticket();
            ticket.setSeatNo(Integer.parseInt(tempOrder.getSeatNumber()));
            ticket.setStartStation(tempOrder.getFrom());
            ticket.setDestStation(tempOrder.getTo());
            ticketSet.add(ticket);
        }
        LeftTicketInfo leftTicketInfo = new LeftTicketInfo();
        leftTicketInfo.setSoldTickets(ticketSet);
        return leftTicketInfo;
    }

    @Override
    public Order findOrderById(UUID id, HttpHeaders headers){
        return orderRepository.findById(id);
    }

    @Override
    public CreateOrderResult create(Order order, HttpHeaders headers){
        System.out.println("[Order Service][Create Order] Ready Create Order.");
        ArrayList<Order> accountOrders = orderRepository.findByAccountId(order.getAccountId());
        CreateOrderResult cor = new CreateOrderResult();
        if(accountOrders.contains(order)){
            System.out.println("[Order Service][Order Create] Fail.Order already exists.");
            cor.setStatus(false);
            cor.setMessage("Order already exist");
            cor.setOrder(null);
        }else{
            order.setId(UUID.randomUUID());
            orderRepository.save(order);
            System.out.println("[Order Service][Order Create] Success.");
            System.out.println("[Order Service][Order Create] Price:" + order.getPrice());
            cor.setStatus(true);
            cor.setMessage("Success");
            cor.setOrder(order);
        }
        return cor;
    }

    @Override
    public OrderAlterResult alterOrder(OrderAlterInfo oai, HttpHeaders headers){
        OrderAlterResult oar = new OrderAlterResult();
        UUID oldOrderId = oai.getPreviousOrderId();
        Order oldOrder = findOrderById(oldOrderId, headers);
        if(oldOrder == null){
            System.out.println("[Order Service][Alter Order] Fail.Order do not exist.");
            oar.setStatus(false);
            oar.setMessage("Old Order Does Not Exists");
            oar.setOldOrder(null);
            oar.setNewOrder(null);
            return oar;
        }
        oldOrder.setStatus(OrderStatus.CANCEL.getCode());
        saveChanges(oldOrder,headers);
        Order newOrder = oai.getNewOrderInfo();
        newOrder.setId(UUID.randomUUID());
        CreateOrderResult cor = create(oai.getNewOrderInfo(), headers);
        if(cor.isStatus() == true){
            oar.setStatus(true);
            oar.setMessage("Success");
            oar.setOldOrder(oldOrder);
            oar.setNewOrder(newOrder);
            System.out.println("[Order Service][Alter Order] Success.");
        }else{
            oar.setStatus(false);
            oar.setMessage(cor.getMessage());
            oar.setOldOrder(null);
            oar.setNewOrder(null);
        }
        return oar;
    }

    @Override
    public ArrayList<Order> queryOrders(QueryInfo qi,String accountId, HttpHeaders headers){
        //1.Get all orders of the user
        ArrayList<Order> list = orderRepository.findByAccountId(UUID.fromString(accountId));
        System.out.println("[Order Service][Query Order][Step 1] Get Orders Number of Account:" + list.size());
        //2.Check is these orders fit the requirement/
        if(qi.isEnableStateQuery() || qi.isEnableBoughtDateQuery() || qi.isEnableTravelDateQuery()){
            ArrayList<Order> finalList = new ArrayList<>();
            for(Order tempOrder : list){
                boolean statePassFlag = false;
                boolean boughtDatePassFlag = false;
                boolean travelDatePassFlag = false;
                //3.Check order state requirement.
                if(qi.isEnableStateQuery()){
                    if(tempOrder.getStatus() != qi.getState()){
                        statePassFlag = false;
                    }else{
                        statePassFlag = true;
                    }
                }else{
                    statePassFlag = true;
                }
                System.out.println("[Order Service][Query Order][Step 2][Check Status Fits End]");
                //4.Check order travel date requirement.
                if(qi.isEnableTravelDateQuery()){
                    if(tempOrder.getTravelDate().before(qi.getTravelDateEnd()) &&
                            tempOrder.getTravelDate().after(qi.getBoughtDateStart())){
                        travelDatePassFlag = true;
                    }else{
                        travelDatePassFlag = false;
                    }
                }else{
                    travelDatePassFlag = true;
                }
                System.out.println("[Order Service][Query Order][Step 2][Check Travel Date End]");
                //5.Check order bought date requirement.
                if(qi.isEnableBoughtDateQuery()){
                    if(tempOrder.getBoughtDate().before(qi.getBoughtDateEnd()) &&
                            tempOrder.getBoughtDate().after(qi.getBoughtDateStart())){
                        boughtDatePassFlag = true;
                    }else{
                        boughtDatePassFlag = false;
                    }
                }else{
                    boughtDatePassFlag = true;
                }
                System.out.println("[Order Service][Query Order][Step 2][Check Bought Date End]");
                //6.check if all requirement fits.
                if(statePassFlag && boughtDatePassFlag && travelDatePassFlag){
                    finalList.add(tempOrder);
                }
                System.out.println("[Order Service][Query Order][Step 2][Check All Requirement End]");
            }
            System.out.println("[Order Service][Query Order] Get order num:" + finalList.size());
            return finalList;
        }else{
            System.out.println("[Order Service][Query Order] Get order num:" + list.size());
            return list;
        }
    }

    @Override
    public ArrayList<Order> queryOrdersForRefresh(QueryInfo qi,String accountId, HttpHeaders headers){
        ArrayList<Order> orders = queryOrders(qi, accountId, headers);
        ArrayList<String> stationIds = new ArrayList<>();
        for(Order order : orders){
            stationIds.add(order.getFrom());
            stationIds.add(order.getTo());
        }
        ArrayList<String> names = queryForStationId(stationIds, headers);
        for(int i = 0; i < orders.size();i++){
            orders.get(i).setFrom(names.get(i * 2));
            orders.get(i).setTo(names.get(i * 2 + 1));
        }
        return orders;
    }

    public ArrayList<String> queryForStationId(ArrayList<String> ids, HttpHeaders headers){
        QueryByIdBatch batch = new QueryByIdBatch(ids);
        HttpEntity requestEntity = new HttpEntity(batch, headers);
        ResponseEntity<QueryByIdBatchResult> re = restTemplate.exchange(
                "http://ts-station-service:12345/station/queryByIdBatch",
                HttpMethod.POST,
                requestEntity,
                QueryByIdBatchResult.class);
        QueryByIdBatchResult names = re.getBody();
        return names.getStationNameList();
    }

    @Override
    public ChangeOrderResult saveChanges(Order order, HttpHeaders headers){
        Order oldOrder = findOrderById(order.getId(),headers);
        ChangeOrderResult cor = new ChangeOrderResult();
        if(oldOrder == null){
            System.out.println("[Order Service][Modify Order] Fail.Order not found.");
            cor.setStatus(false);
            cor.setMessage("Order Not Found");
            cor.setOrder(null);
        }else{
            oldOrder.setAccountId(order.getAccountId());
            oldOrder.setBoughtDate(order.getBoughtDate());
            oldOrder.setTravelDate(order.getTravelDate());
            oldOrder.setTravelTime(order.getTravelTime());
            oldOrder.setCoachNumber(order.getCoachNumber());
            oldOrder.setSeatClass(order.getSeatClass());
            oldOrder.setSeatNumber(order.getSeatNumber());
            oldOrder.setFrom(order.getFrom());
            oldOrder.setTo(order.getTo());
            oldOrder.setStatus(order.getStatus());
            oldOrder.setTrainNumber(order.getTrainNumber());
            oldOrder.setPrice(order.getPrice());
            oldOrder.setContactsName(order.getContactsName());
            oldOrder.setContactsDocumentNumber(order.getContactsDocumentNumber());
            oldOrder.setDocumentType(order.getDocumentType());
            orderRepository.save(oldOrder);
            System.out.println("[Order Service] Success.");
            cor.setOrder(oldOrder);
            cor.setStatus(true);
            cor.setMessage("Success");
        }
        return cor;
    }

    @Override
    public CancelOrderResult cancelOrder(CancelOrderInfo coi, HttpHeaders headers){
        UUID orderId = coi.getOrderId();
        Order oldOrder = orderRepository.findById(orderId);
        CancelOrderResult cor = new CancelOrderResult();
        if(oldOrder == null){
            System.out.println("[Cancel Service][Cancel Order] Fail.Order not found.");
            cor.setStatus(false);
            cor.setMessage("Order Not Found");
            cor.setOrder(null);

        }else{
            oldOrder.setStatus(OrderStatus.CANCEL.getCode());
            orderRepository.save(oldOrder);
            System.out.println("[Cancel Service][Cancel Order] Success.");
            cor.setStatus(true);
            cor.setMessage("Success");
            cor.setOrder(oldOrder);
        }
        return cor;
    }

    @Override
    public  CalculateSoldTicketResult queryAlreadySoldOrders(CalculateSoldTicketInfo csti, HttpHeaders headers){
        ArrayList<Order> orders = orderRepository.findByTravelDateAndTrainNumber(csti.getTravelDate(),csti.getTrainNumber());
        CalculateSoldTicketResult cstr = new CalculateSoldTicketResult();
        cstr.setTravelDate(csti.getTravelDate());
        cstr.setTrainNumber(csti.getTrainNumber());
        System.out.println("[Order Service][Calculate Sold Ticket] Get Orders Number:" + orders.size());
        for(Order order : orders){
            if(order.getStatus() >= OrderStatus.CHANGE.getCode()){
                continue;
            }
            if(order.getSeatClass() == SeatClass.NONE.getCode()){
                cstr.setNoSeat(cstr.getNoSeat() + 1);
            }else if(order.getSeatClass() == SeatClass.BUSINESS.getCode()){
                cstr.setBusinessSeat(cstr.getBusinessSeat() + 1);
            }else if(order.getSeatClass() == SeatClass.FIRSTCLASS.getCode()){
                cstr.setFirstClassSeat(cstr.getFirstClassSeat() + 1);
            }else if(order.getSeatClass() == SeatClass.SECONDCLASS.getCode()){
                cstr.setSecondClassSeat(cstr.getSecondClassSeat() + 1);
            }else if(order.getSeatClass() == SeatClass.HARDSEAT.getCode()){
                cstr.setHardSeat(cstr.getHardSeat() + 1);
            }else if(order.getSeatClass() == SeatClass.SOFTSEAT.getCode()){
                cstr.setSoftSeat(cstr.getSoftSeat() + 1);
            }else if(order.getSeatClass() == SeatClass.HARDBED.getCode()){
                cstr.setHardBed(cstr.getHardBed() + 1);
            }else if(order.getSeatClass() == SeatClass.SOFTBED.getCode()){
                cstr.setSoftBed(cstr.getSoftBed() + 1);
            }else if(order.getSeatClass() == SeatClass.HIGHSOFTBED.getCode()){
                cstr.setHighSoftBed(cstr.getHighSoftBed() + 1);
            }else{
                System.out.println("[Order Service][Calculate Sold Tickets] Seat class not exists. Order ID:" + order.getId());
            }
        }
        return cstr;
    }

    @Override
    public QueryOrderResult getAllOrders(HttpHeaders headers){
        ArrayList<Order> orders = orderRepository.findAll();
        QueryOrderResult result = new QueryOrderResult(true,"Success.",orders);
        return result;
    }

    @Override
    public ModifyOrderStatusResult modifyOrder(ModifyOrderStatusInfo info, HttpHeaders headers){
        Order order = orderRepository.findById(UUID.fromString(info.getOrderId()));
        ModifyOrderStatusResult result = new ModifyOrderStatusResult();
        if(order == null){
            result.setStatus(false);
            result.setMessage("Order Not Found");
            result.setOrder(null);
        }else{
            order.setStatus(info.getStatus());
            orderRepository.save(order);
            result.setStatus(true);
            result.setMessage("Success");
            result.setOrder(order);
        }
        return result;
    }

    @Override
    public GetOrderPriceResult getOrderPrice(GetOrderPrice info, HttpHeaders headers){
        Order order = orderRepository.findById(UUID.fromString(info.getOrderId()));
        GetOrderPriceResult result = new GetOrderPriceResult();
        if(order == null){
            System.out.println("[Other Service][Get Order Price] Order Not Found.");
            result.setStatus(false);
            result.setMessage("Order Not Found");
            result.setPrice("-1.0");
        }else{
            result.setStatus(true);
            result.setMessage("Success");
            System.out.println("[Order Service][Get Order Price] Price:" + order.getPrice());
            result.setPrice(order.getPrice());
        }
        return result;
    }

    @Override
    public PayOrderResult payOrder(PayOrderInfo info, HttpHeaders headers){
        Order order = orderRepository.findById(UUID.fromString(info.getOrderId()));
        PayOrderResult result = new PayOrderResult();
        if(result == null){
            result.setStatus(false);
            result.setMessage("Order Not Found");
            result.setOrder(null);
        }else{
            order.setStatus(OrderStatus.PAID.getCode());
            orderRepository.save(order);
            result.setStatus(true);
            result.setMessage("Success.");
            result.setOrder(order);
        }
        return result;
    }

    @Override
    public GetOrderResult getOrderById(GetOrderByIdInfo info, HttpHeaders headers){
        Order order = orderRepository.findById(UUID.fromString(info.getOrderId()));
        GetOrderResult result = new GetOrderResult();
        if(order == null){
            result.setStatus(false);
            result.setMessage("Order Not Found");
            result.setOrder(null);
        }else{
            result.setStatus(true);
            result.setMessage("Success.");
            result.setOrder(order);
        }
        return result;
    }

    @Override
    public void initOrder(Order order, HttpHeaders headers){
        Order orderTemp = orderRepository.findById(order.getId());
        if(orderTemp == null){
            orderRepository.save(order);
        }else{
            System.out.println("[Order Service][Init Order] Order Already Exists ID:" + order.getId());
        }
    }

    @Override
    public GetOrderInfoForSecurityResult checkSecurityAboutOrder(GetOrderInfoForSecurity info, HttpHeaders headers){
        GetOrderInfoForSecurityResult result = new GetOrderInfoForSecurityResult();
        ArrayList<Order> orders = orderRepository.findByAccountId(UUID.fromString(info.getAccountId()));
        int countOrderInOneHour = 0;
        int countTotalValidOrder = 0;
        Date dateFrom = info.getCheckDate();
        Calendar ca = Calendar.getInstance();
        ca.setTime(dateFrom );
        ca.add(Calendar.HOUR_OF_DAY, -1);
        dateFrom = ca.getTime();
        for(Order order : orders){
            if(order.getStatus() == OrderStatus.NOTPAID.getCode() ||
                    order.getStatus() == OrderStatus.PAID.getCode() ||
                    order.getStatus() == OrderStatus.COLLECTED.getCode()){
                countTotalValidOrder += 1;
            }
            if(order.getBoughtDate().after(dateFrom)){
                countOrderInOneHour += 1;
            }
        }
        result.setOrderNumInLastOneHour(countOrderInOneHour);
        result.setOrderNumOfValidOrder(countTotalValidOrder);
        return result;
    }

    @Override
    public DeleteOrderResult deleteOrder(DeleteOrderInfo info, HttpHeaders headers){
        UUID orderUuid = UUID.fromString(info.getOrderId());
        Order order = orderRepository.findById(orderUuid);
        DeleteOrderResult result = new DeleteOrderResult();
        if(order == null){
            result.setStatus(false);
            result.setMessage("Order Not Exist.");
        }else{
            orderRepository.deleteById(orderUuid);
            result.setStatus(true);
            result.setMessage("Success.");
        }
        return result;
    }

    @Override
    public AddOrderResult addNewOrder(Order order, HttpHeaders headers) {
        System.out.println("[Order Service][Admin Add Order] Ready Add Order.");
        ArrayList<Order> accountOrders = orderRepository.findByAccountId(order.getAccountId());
        AddOrderResult result = new AddOrderResult();
        if(accountOrders.contains(order)){
            System.out.println("[Order Service][Admin Add Order] Fail.Order already exists.");
            result.setStatus(false);
            result.setMessage("Order already exist");
            result.setOrder(null);
        }else{
            order.setId(UUID.randomUUID());
            orderRepository.save(order);
            System.out.println("[Order Service][Admin Add Order] Success.");
            System.out.println("[Order Service][Admin Add Order] Price:" + order.getPrice());
            result.setStatus(true);
            result.setMessage("Success");
            result.setOrder(order);
        }
        return result;
    }

    @Override
    public UpdateOrderResult updateOrder(Order order, HttpHeaders headers) {
        Order oldOrder = findOrderById(order.getId(), headers);
        UpdateOrderResult result = new UpdateOrderResult();
        if(oldOrder == null){
            System.out.println("[Order Service][Admin Update Order] Fail.Order not found.");
            result.setStatus(false);
            result.setMessage("Order Not Found");
            result.setOrder(null);
        }else{
            oldOrder.setAccountId(order.getAccountId());
            oldOrder.setBoughtDate(order.getBoughtDate());
            oldOrder.setTravelDate(order.getTravelDate());
            oldOrder.setTravelTime(order.getTravelTime());
            oldOrder.setCoachNumber(order.getCoachNumber());
            oldOrder.setSeatClass(order.getSeatClass());
            oldOrder.setSeatNumber(order.getSeatNumber());
            oldOrder.setFrom(order.getFrom());
            oldOrder.setTo(order.getTo());
            oldOrder.setStatus(order.getStatus());
            oldOrder.setTrainNumber(order.getTrainNumber());
            oldOrder.setPrice(order.getPrice());
            oldOrder.setContactsName(order.getContactsName());
            oldOrder.setContactsDocumentNumber(order.getContactsDocumentNumber());
            oldOrder.setDocumentType(order.getDocumentType());
            orderRepository.save(oldOrder);
            System.out.println("[Order Service] [Admin Update Order] Success.");
            result.setOrder(oldOrder);
            result.setStatus(true);
            result.setMessage("Success");
        }
        return result;
    }
}

