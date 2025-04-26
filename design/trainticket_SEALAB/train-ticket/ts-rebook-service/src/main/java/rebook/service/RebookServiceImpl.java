package rebook.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.integration.dsl.http.Http;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.client.RestTemplate;
import rebook.domain.*;
import rebook.domain.RebookInfo;
import rebook.domain.RebookResult;
import java.math.BigDecimal;
import java.util.Calendar;
import java.util.Date;

@Service
public class RebookServiceImpl implements RebookService{

    @Autowired
    private RestTemplate restTemplate;

    @Override
    public RebookResult rebook(RebookInfo info, String loginId, String loginToken, HttpHeaders httpHeaders){
        RebookResult rebookResult = new RebookResult();

        QueryOrderResult queryOrderResult = getOrderByRebookInfo(info, httpHeaders);

        if(!queryOrderResult.isStatus()){
            rebookResult.setStatus(false);
            rebookResult.setMessage(queryOrderResult.getMessage());
            rebookResult.setOrder(null);
            return rebookResult;
        }

        Order order = queryOrderResult.getOrder();
        int status = order.getStatus();
        if(status == OrderStatus.NOTPAID.getCode()){
            rebookResult.setStatus(false);
            rebookResult.setMessage("You haven't paid the original ticket!");
            rebookResult.setOrder(null);
            return rebookResult;
        }else if(status == OrderStatus.PAID.getCode()){
            // do nothing
        }else if(status == OrderStatus.CHANGE.getCode()){
            rebookResult.setStatus(false);
            rebookResult.setMessage("You have already changed your ticket and you can only change one time.");
            rebookResult.setOrder(null);
            return rebookResult;
        }else if(status == OrderStatus.COLLECTED.getCode()){
            rebookResult.setStatus(false);
            rebookResult.setMessage("You have already collected your ticket and you can change it now.");
            rebookResult.setOrder(null);
            return rebookResult;
        } else{
            rebookResult.setStatus(false);
            rebookResult.setMessage("You can't change your ticket.");
            rebookResult.setOrder(null);
            return rebookResult;
        }

        //查询当前时间和旧订单乘车时间，根据时间来判断能否改签，发车两小时后不能改签
        if(!checkTime(order.getTravelDate(),order.getTravelTime())){
            rebookResult.setStatus(false);
            rebookResult.setMessage("You can only change the ticket before the train start or within 2 hours after the train start.");
            rebookResult.setOrder(null);
            return rebookResult;
        }

        //改签不能更换出发地和目的地，只能更改车次、席位、时间
        //查询座位余票信息和车次的详情
        GetTripAllDetailInfo gtdi = new GetTripAllDetailInfo();
        gtdi.setFrom(queryForStationName(order.getFrom(), httpHeaders));
        gtdi.setTo(queryForStationName(order.getTo(), httpHeaders));
        gtdi.setTravelDate(info.getDate());
        gtdi.setTripId(info.getTripId());
        GetTripAllDetailResult gtdr = getTripAllDetailInformation(gtdi,info.getTripId(), httpHeaders);
        if(gtdr.isStatus() == false){
            rebookResult.setStatus(false);
            rebookResult.setMessage(gtdr.getMessage());
            rebookResult.setOrder(null);
            return rebookResult;
        }else{
            TripResponse tripResponse = gtdr.getTripResponse();
            if(info.getSeatType() == SeatClass.FIRSTCLASS.getCode()){
                if(tripResponse.getConfortClass() <= 0){
                    rebookResult.setStatus(false);
                    rebookResult.setMessage("Seat Not Enough");
                    rebookResult.setOrder(null);
                    return rebookResult;
                }
            }else{
                if(tripResponse.getEconomyClass() == SeatClass.SECONDCLASS.getCode()){
                    if(tripResponse.getConfortClass() <= 0){
                        rebookResult.setStatus(false);
                        rebookResult.setMessage("Seat Not Enough");
                        rebookResult.setOrder(null);
                    }
                }
            }
        }
        Trip trip = gtdr.getTrip();

        //处理差价，多退少补
        //退掉原有的票，让其他人可以订到对应的位置
//        QueryPriceInfo queryPriceInfo = new QueryPriceInfo();
//        queryPriceInfo.setStartingPlaceId(order.getFrom());
//        queryPriceInfo.setEndPlaceId(order.getTo());
//
//        if(info.getSeatType() == SeatClass.FIRSTCLASS.getCode()){
//            queryPriceInfo.setSeatClass("confortClass");
//        }else if(info.getSeatType() == SeatClass.SECONDCLASS.getCode()) {
//            queryPriceInfo.setSeatClass("economyClass");
//        }
//        queryPriceInfo.setTrainTypeId(trip.getTrainTypeId());
//
//        String ticketPrice = getPrice(queryPriceInfo);

        String ticketPrice =  "0";
        if(info.getSeatType() == SeatClass.FIRSTCLASS.getCode()){
            ticketPrice = gtdr.getTripResponse().getPriceForConfortClass();
        }else if(info.getSeatType() == SeatClass.SECONDCLASS.getCode()) {
            ticketPrice = gtdr.getTripResponse().getPriceForEconomyClass();
        }
        String oldPrice = order.getPrice();
        BigDecimal priceOld = new BigDecimal(oldPrice);
        BigDecimal priceNew = new BigDecimal(ticketPrice);
        if(priceOld.compareTo(priceNew) > 0){
            //退差价
            String difference = priceOld.subtract(priceNew).toString();
            if(!drawBackMoney(loginId,difference, httpHeaders)){
                rebookResult.setStatus(false);
                rebookResult.setMessage("Can't draw back the difference money, please try again!");
                rebookResult.setOrder(null);
                return rebookResult;
            }
            return updateOrder(order,info,gtdr,ticketPrice,loginId,loginToken,httpHeaders);

        }else if(priceOld.compareTo(priceNew) == 0){
            //do nothing
            return updateOrder(order,info,gtdr,ticketPrice,loginId,loginToken,httpHeaders);
        }else{
            //补差价
            String difference = priceNew.subtract(priceOld).toString();
            rebookResult.setStatus(false);
            rebookResult.setMessage("Please pay the different money!");
            rebookResult.setOrder(null);
            rebookResult.setPrice(difference);
            return rebookResult;
        }
    }

    @Override
    public RebookResult payDifference(RebookInfo info, String loginId, String loginToken, HttpHeaders httpHeaders){
        RebookResult rebookResult = new RebookResult();

        QueryOrderResult queryOrderResult = getOrderByRebookInfo(info, httpHeaders);
//        if(info.getOldTripId().startsWith("G") || info.getOldTripId().startsWith("D")){
//            queryOrderResult = restTemplate.postForObject(
//                    "http://ts-order-service:12031/order/getById", new QueryOrder(info.getOrderId()),QueryOrderResult.class);
//        }else{
//            queryOrderResult = restTemplate.postForObject(
//                    "http://ts-order-other-service:12032/orderOther/getById", new QueryOrder(info.getOrderId()),QueryOrderResult.class);
//        }

        if(!queryOrderResult.isStatus()){
            rebookResult.setStatus(false);
            rebookResult.setMessage(queryOrderResult.getMessage());
            rebookResult.setOrder(null);
            return rebookResult;
        }

        Order order = queryOrderResult.getOrder();

        GetTripAllDetailInfo gtdi = new GetTripAllDetailInfo();
        gtdi.setFrom(queryForStationName(order.getFrom(), httpHeaders));
        gtdi.setTo(queryForStationName(order.getTo(), httpHeaders));
        gtdi.setTravelDate(info.getDate());
        gtdi.setTripId(info.getTripId());
        GetTripAllDetailResult gtdr = getTripAllDetailInformation(gtdi,info.getTripId(), httpHeaders);

//        QueryPriceInfo queryPriceInfo = new QueryPriceInfo();
//        queryPriceInfo.setStartingPlaceId(order.getFrom());
//        queryPriceInfo.setEndPlaceId(order.getTo());
//        if(info.getSeatType() == SeatClass.FIRSTCLASS.getCode()){
//            queryPriceInfo.setSeatClass("confortClass");
//        }else if(info.getSeatType() == SeatClass.SECONDCLASS.getCode()) {
//            queryPriceInfo.setSeatClass("economyClass");
//        }
//        Trip trip = gtdr.getTrip();
//        queryPriceInfo.setTrainTypeId(trip.getTrainTypeId());

        //String ticketPrice = getPrice(queryPriceInfo);
        String ticketPrice =  "0";
        if(info.getSeatType() == SeatClass.FIRSTCLASS.getCode()){
            ticketPrice = gtdr.getTripResponse().getPriceForConfortClass();
        }else if(info.getSeatType() == SeatClass.SECONDCLASS.getCode()) {
            ticketPrice = gtdr.getTripResponse().getPriceForEconomyClass();
        }
        String oldPrice = order.getPrice();
        BigDecimal priceOld = new BigDecimal(oldPrice);
        BigDecimal priceNew = new BigDecimal(ticketPrice);

        if(payDifferentMoney(info.getOrderId(),info.getTripId(),loginId,priceNew.subtract(priceOld).toString(), httpHeaders)){
            return updateOrder(order,info,gtdr,ticketPrice,loginId,loginToken,httpHeaders);
        }else{
            rebookResult.setStatus(false);
            rebookResult.setMessage("Can't pay the difference,please try again");
            rebookResult.setOrder(null);
            return rebookResult;
        }
    }

    private RebookResult updateOrder(Order order, RebookInfo info, GetTripAllDetailResult gtdr, String ticketPrice, String loginId, String loginToken, HttpHeaders httpHeaders){
        RebookResult rebookResult = new RebookResult();
        //4.修改原有订单 设置order的各个信息
        Trip trip = gtdr.getTrip();
        String oldTripId = order.getTrainNumber();
        order.setTrainNumber(info.getTripId());
        order.setBoughtDate(new Date());
        order.setStatus(OrderStatus.CHANGE.getCode());
        order.setPrice(ticketPrice);//Set ticket price
        order.setSeatClass(info.getSeatType());
        order.setTravelDate(info.getDate());
        order.setTravelTime(trip.getStartingTime());

        if(info.getSeatType() == SeatClass.FIRSTCLASS.getCode()){//Dispatch the seat
            Ticket ticket =
                    dipatchSeat(info.getDate(),
                            order.getTrainNumber(),order.getFrom(),order.getTo(),
                            SeatClass.FIRSTCLASS.getCode(), httpHeaders);
            order.setSeatClass(SeatClass.FIRSTCLASS.getCode());
            order.setSeatNumber("" + ticket.getSeatNo());
        }else{
            Ticket ticket =
                    dipatchSeat(info.getDate(),
                            order.getTrainNumber(),order.getFrom(),order.getTo(),
                            SeatClass.SECONDCLASS.getCode(), httpHeaders);
            order.setSeatClass(SeatClass.SECONDCLASS.getCode());
            order.setSeatNumber("" + ticket.getSeatNo());
        }

//        if(info.getSeatType() == SeatClass.FIRSTCLASS.getCode()){//Dispatch the seat
//            int firstClassRemainNum = gtdr.getTripResponse().getConfortClass();
//            order.setSeatNumber("FirstClass-" + firstClassRemainNum);
//        }else{
//            int secondClassRemainNum = gtdr.getTripResponse().getEconomyClass();
//            order.setSeatNumber("SecondClass-" + secondClassRemainNum);
//        }


        //更新订单信息
        //原订单和新订单如果分别位于高铁动车和其他订单，应该删掉原订单，在另一边新建，用新的id
        if((tripGD(oldTripId) && tripGD(info.getTripId())) || (!tripGD(oldTripId) && !tripGD(info.getTripId()))){
            ChangeOrderInfo changeOrderInfo = new ChangeOrderInfo();
            changeOrderInfo.setLoginToken(loginToken);
            changeOrderInfo.setOrder(order);
            ChangeOrderResult changeOrderResult = updateOrder(changeOrderInfo,info.getTripId(), httpHeaders);
            if(changeOrderResult.isStatus()){
                rebookResult.setStatus(true);
                rebookResult.setMessage("Success!");
                rebookResult.setOrder(order);
                return rebookResult;
            }else{
                rebookResult.setStatus(false);
                rebookResult.setMessage("Can't update Order!");
                rebookResult.setOrder(null);
                return rebookResult;
            }
        }else{
            //删掉原有订单
            deleteOrder(order.getId().toString(), oldTripId, httpHeaders);
            //在另一边创建新订单
            createOrder(order,loginToken,order.getTrainNumber(), httpHeaders);
            rebookResult.setStatus(true);
            rebookResult.setMessage("Success!");
            rebookResult.setOrder(order); //order id是不对的，因为新创建的时候，会创建新的order id
            return rebookResult;
        }
    }

    public Ticket dipatchSeat(Date date,String tripId,String startStationId,String endStataionId,int seatType, HttpHeaders httpHeaders){
        SeatRequest seatRequest = new SeatRequest();
        seatRequest.setTravelDate(date);
        seatRequest.setTrainNumber(tripId);
        seatRequest.setStartStation(startStationId);
        seatRequest.setDestStation(endStataionId);
        seatRequest.setSeatType(seatType);

        HttpEntity requestEntityTicket = new HttpEntity(seatRequest,httpHeaders);
        ResponseEntity<Ticket> reTicket = restTemplate.exchange(
                "http://ts-seat-service:18898/seat/getSeat",
                HttpMethod.POST,
                requestEntityTicket,
                Ticket.class);
        Ticket ticket  = reTicket.getBody();

//        Ticket ticket = restTemplate.postForObject(
//                "http://ts-seat-service:18898/seat/getSeat"
//                ,seatRequest,Ticket.class);
        return ticket;
    }


    private boolean tripGD(String tripId){
        if(tripId.startsWith("G") || tripId.startsWith("D")){
            return true;
        }else{
            return false;
        }
    }

    private VerifyResult verifySsoLogin(String loginToken, HttpHeaders headers){
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

    private boolean checkTime(Date travelDate, Date travelTime) {
        boolean result = true;
        Calendar calDateA = Calendar.getInstance();
        Date today = new Date();
        calDateA.setTime(today);
        Calendar calDateB = Calendar.getInstance();
        calDateB.setTime(travelDate);
        Calendar calDateC = Calendar.getInstance();
        calDateC.setTime(travelTime);
        if(calDateA.get(Calendar.YEAR) > calDateB.get(Calendar.YEAR)){
            result = false;
        }else if(calDateA.get(Calendar.YEAR) == calDateB.get(Calendar.YEAR)){
            if(calDateA.get(Calendar.MONTH) > calDateB.get(Calendar.MONTH)){
                result = false;
            }else if(calDateA.get(Calendar.MONTH) == calDateB.get(Calendar.MONTH)){
                if(calDateA.get(Calendar.DAY_OF_MONTH) > calDateB.get(Calendar.DAY_OF_MONTH)){
                    result = false;
                }else if(calDateA.get(Calendar.DAY_OF_MONTH) == calDateB.get(Calendar.DAY_OF_MONTH)){
                    if(calDateA.get(Calendar.HOUR_OF_DAY) > calDateC.get(Calendar.HOUR_OF_DAY)+2){
                        result = false;
                    }else if(calDateA.get(Calendar.HOUR_OF_DAY) == calDateC.get(Calendar.HOUR_OF_DAY)+2){
                        if(calDateA.get(Calendar.MINUTE) > calDateC.get(Calendar.MINUTE)){
                            result = false;
                        }
                    }
                }
            }
        }
        return result;
    }

    private GetTripAllDetailResult getTripAllDetailInformation(GetTripAllDetailInfo gtdi, HttpHeaders httpHeaders){
        System.out.println("[Preserve Other Service][Get Trip All Detail Information] Getting....");

        HttpEntity requestGetTripAllDetailResult = new HttpEntity(gtdi, httpHeaders);
        ResponseEntity<GetTripAllDetailResult> reGetTripAllDetailResult = restTemplate.exchange(
                "http://ts-travel-service:12346/travel/getTripAllDetailInfo/",
                HttpMethod.POST,
                requestGetTripAllDetailResult,
                GetTripAllDetailResult.class);
        GetTripAllDetailResult gtdr = reGetTripAllDetailResult.getBody();
//        GetTripAllDetailResult gtdr = restTemplate.postForObject(
//                "http://ts-travel-service:12346/travel/getTripAllDetailInfo/"
//                ,gtdi,GetTripAllDetailResult.class);
        return gtdr;
    }


    private GetTripAllDetailResult getTripAllDetailInformation(GetTripAllDetailInfo gtdi, String tripId, HttpHeaders httpHeaders){
        GetTripAllDetailResult gtdr;
        if(tripId.startsWith("G") || tripId.startsWith("D")){

            HttpEntity requestGetTripAllDetailResult = new HttpEntity(gtdi, httpHeaders);
            ResponseEntity<GetTripAllDetailResult> reGetTripAllDetailResult = restTemplate.exchange(
                    "http://ts-travel-service:12346/travel/getTripAllDetailInfo/",
                    HttpMethod.POST,
                    requestGetTripAllDetailResult,
                    GetTripAllDetailResult.class);
            gtdr = reGetTripAllDetailResult.getBody();
//            gtdr = restTemplate.postForObject(
//                    "http://ts-travel-service:12346/travel/getTripAllDetailInfo"
//                    ,gtdi,GetTripAllDetailResult.class);
        }else{
            HttpEntity requestGetTripAllDetailResult = new HttpEntity(gtdi, httpHeaders);
            ResponseEntity<GetTripAllDetailResult> reGetTripAllDetailResult = restTemplate.exchange(
                    "http://ts-travel2-service:16346/travel2/getTripAllDetailInfo",
                    HttpMethod.POST,
                    requestGetTripAllDetailResult,
                    GetTripAllDetailResult.class);
            gtdr = reGetTripAllDetailResult.getBody();
//            gtdr = restTemplate.postForObject(
//                    "http://ts-travel2-service:16346/travel2/getTripAllDetailInfo"
//                    ,gtdi,GetTripAllDetailResult.class);
        }
        return gtdr;
    }

    private CreateOrderResult createOrder(Order order, String loginToken, String tripId, HttpHeaders httpHeaders){
        CreateOrderInfo createOrderInfo = new CreateOrderInfo();
        createOrderInfo.setOrder(order);
        createOrderInfo.setLoginToken(loginToken);
        CreateOrderResult createOrderResult;
        if(tripId.startsWith("G") || tripId.startsWith("D")){

            HttpEntity requestCreateOrder = new HttpEntity(createOrderInfo, httpHeaders);
            ResponseEntity<CreateOrderResult> reCreateOrder = restTemplate.exchange(
                    "http://ts-order-service:12031/order/create",
                    HttpMethod.POST,
                    requestCreateOrder,
                    CreateOrderResult.class);
            createOrderResult = reCreateOrder .getBody();
//            createOrderResult = restTemplate.postForObject(
//                    "http://ts-order-service:12031/order/create"
//                    ,createOrderInfo,CreateOrderResult.class);
        }else{

            HttpEntity requestCreateOrder = new HttpEntity(createOrderInfo, httpHeaders);
            ResponseEntity<CreateOrderResult> reCreateOrder = restTemplate.exchange(
                    "http://ts-order-other-service:12032/orderOther/create",
                    HttpMethod.POST,
                    requestCreateOrder,
                    CreateOrderResult.class);
            createOrderResult = reCreateOrder .getBody();
//            createOrderResult = restTemplate.postForObject(
//                    "http://ts-order-other-service:12032/orderOther/create"
//                    ,createOrderInfo,CreateOrderResult.class);
        }
        return createOrderResult;
    }

    private ChangeOrderResult updateOrder(ChangeOrderInfo info, String tripId, HttpHeaders httpHeaders){
        ChangeOrderResult result;
        if(tripGD(tripId)){
            HttpEntity requestUpdateOrder = new HttpEntity(info, httpHeaders);
            ResponseEntity<ChangeOrderResult> reUpdateOrder = restTemplate.exchange(
                    "http://ts-order-service:12031/order/update",
                    HttpMethod.POST,
                    requestUpdateOrder,
                    ChangeOrderResult.class);
            result = reUpdateOrder.getBody();
//            result = restTemplate.postForObject("http://ts-order-service:12031/order/update",
//                    info,ChangeOrderResult.class);
        }else{
            HttpEntity requestUpdateOrder = new HttpEntity(info, httpHeaders);
            ResponseEntity<ChangeOrderResult> reUpdateOrder = restTemplate.exchange(
                    "http://ts-order-other-service:12032/orderOther/update",
                    HttpMethod.POST,
                    requestUpdateOrder,
                    ChangeOrderResult.class);
            result = reUpdateOrder.getBody();
//            result = restTemplate.postForObject("http://ts-order-other-service:12032/orderOther/update",
//                    info,ChangeOrderResult.class);
        }
        return result;
    }

    private DeleteOrderResult deleteOrder(String orderId, String tripId, HttpHeaders httpHeaders){
        DeleteOrderInfo deleteOrderInfo = new DeleteOrderInfo();
        deleteOrderInfo.setOrderId(orderId);
        DeleteOrderResult deleteOrderResult;
        if(tripGD(tripId)){
            HttpEntity requestDeleteOrder = new HttpEntity(deleteOrderInfo, httpHeaders);
            ResponseEntity<DeleteOrderResult> reDeleteOrder = restTemplate.exchange(
                    "http://ts-order-service:12031/order/delete",
                    HttpMethod.POST,
                    requestDeleteOrder,
                    DeleteOrderResult.class);
            deleteOrderResult = reDeleteOrder .getBody();
//            deleteOrderResult = restTemplate.postForObject("http://ts-order-service:12031/order/delete",
//                    deleteOrderInfo,DeleteOrderResult.class);
        }else{
            HttpEntity requestDeleteOrder = new HttpEntity(deleteOrderInfo, httpHeaders);
            ResponseEntity<DeleteOrderResult> reDeleteOrder = restTemplate.exchange(
                    "http://ts-order-other-service:12032/orderOther/delete",
                    HttpMethod.POST,
                    requestDeleteOrder,
                    DeleteOrderResult.class);
            deleteOrderResult = reDeleteOrder .getBody();
//            deleteOrderResult = restTemplate.postForObject("http://ts-order-other-service:12032/orderOther/delete",
//                    deleteOrderInfo,DeleteOrderResult.class);
        }
        return deleteOrderResult;
    }

    private QueryOrderResult getOrderByRebookInfo(RebookInfo info, HttpHeaders httpHeaders){
        QueryOrderResult queryOrderResult;
        //改签只能改签一次，查询订单状态来判断是否已经改签过
        if(info.getOldTripId().startsWith("G") || info.getOldTripId().startsWith("D")){
            HttpEntity requestEntityGetOrderByRebookInfo = new HttpEntity(info,httpHeaders);
            ResponseEntity<QueryOrderResult> reGetOrderByRebookInfo = restTemplate.exchange(
                    "http://ts-order-service:12031/order/getById",
                    HttpMethod.POST,
                    requestEntityGetOrderByRebookInfo,
                    QueryOrderResult.class);
            queryOrderResult = reGetOrderByRebookInfo.getBody();
//            queryOrderResult = restTemplate.postForObject(
//                    "http://ts-order-service:12031/order/getById", new QueryOrder(info.getOrderId()),QueryOrderResult.class);
        }else{

            HttpEntity requestEntityGetOrderByRebookInfo = new HttpEntity(info,httpHeaders);
            ResponseEntity<QueryOrderResult> reGetOrderByRebookInfo = restTemplate.exchange(
                    "http://ts-order-other-service:12032/orderOther/getById",
                    HttpMethod.POST,
                    requestEntityGetOrderByRebookInfo,
                    QueryOrderResult.class);
            queryOrderResult = reGetOrderByRebookInfo.getBody();

//            queryOrderResult = restTemplate.postForObject(
//                    "http://ts-order-other-service:12032/orderOther/getById", new QueryOrder(info.getOrderId()),QueryOrderResult.class);
        }
        return queryOrderResult;
    }

    private String queryForStationName(String stationId, HttpHeaders httpHeaders){
        QueryById query = new QueryById();
        query.setStationId(stationId);

        HttpEntity requestEntityQueryForStationName = new HttpEntity(query,httpHeaders);
        ResponseEntity<QueryStation> reQueryForStationName = restTemplate.exchange(
                "http://ts-station-service:12345/station/queryById",
                HttpMethod.POST,
                requestEntityQueryForStationName,
                QueryStation.class);
        QueryStation station = reQueryForStationName.getBody();
//        QueryStation station = restTemplate.postForObject(
//                "http://ts-station-service:12345/station/queryById"
//                ,query,QueryStation.class);
        return station.getName();
    }

    private boolean payDifferentMoney(String orderId, String tripId, String userId, String money, HttpHeaders httpHeaders){
        PaymentDifferenceInfo info = new PaymentDifferenceInfo();
        info.setOrderId(orderId);
        info.setTripId(tripId);
        info.setUserId(userId);
        info.setPrice(money);

        HttpEntity requestEntityPayDifferentMoney = new HttpEntity(info,httpHeaders);
        ResponseEntity<Boolean> rePayDifferentMoney = restTemplate.exchange(
                "http://ts-inside-payment-service:18673/inside_payment/payDifference",
                HttpMethod.POST,
                requestEntityPayDifferentMoney,
                Boolean.class);
        boolean result = rePayDifferentMoney.getBody();
//        boolean result = restTemplate.postForObject(
//                "http://ts-inside-payment-service:18673/inside_payment/payDifference"
//                ,info,Boolean.class);
        return result;
    }

    private boolean drawBackMoney(String userId,String money, HttpHeaders httpHeaders){
        DrawBackInfo info = new DrawBackInfo();
        info.setUserId(userId);
        info.setMoney(money);

        HttpEntity requestEntityDrawBackMoney = new HttpEntity(info,httpHeaders);
        ResponseEntity<Boolean> reDrawBackMoney = restTemplate.exchange(
                "http://ts-inside-payment-service:18673/inside_payment/drawBack",
                HttpMethod.POST,
                requestEntityDrawBackMoney,
                Boolean.class);
        boolean result = reDrawBackMoney.getBody();
//        boolean result = restTemplate.postForObject(
//                "http://ts-inside-payment-service:18673/inside_payment/drawBack"
//                ,info,Boolean.class);
        return result;
    }

}
