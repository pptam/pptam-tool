package preserveOther.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.integration.dsl.http.Http;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import preserveOther.domain.*;
import java.util.Date;
import java.util.UUID;

@Service
public class PreserveOtherServiceImpl implements PreserveOtherService{

    @Autowired
    private RestTemplate restTemplate;

    @Override
    public OrderTicketsResult preserve(OrderTicketsInfo oti, String accountId, String loginToken, HttpHeaders httpHeaders){
        VerifyResult tokenResult = verifySsoLogin(loginToken, httpHeaders);
        OrderTicketsResult otr = new OrderTicketsResult();
        if(tokenResult.isStatus() == true){
            System.out.println("[Preserve Other Service][Verify Login] Success");
            //1.黄牛检测
            System.out.println("[Preserve Service] [Step 1] Check Security");
            CheckInfo checkInfo = new CheckInfo();
            checkInfo.setAccountId(accountId);
            CheckResult result = checkSecurity(checkInfo, httpHeaders);
            if(result.isStatus() == false){
                System.out.println("[Preserve Service] [Step 1] Check Security Fail. Return soon.");
                otr.setStatus(false);
                otr.setMessage(result.getMessage());
                otr.setOrder(null);
                return otr;
            }
            System.out.println("[Preserve Service] [Step 1] Check Security Complete. ");
            //2.查询联系人信息 -- 修改，通过基础信息微服务作为中介
            System.out.println("[Preserve Other Service] [Step 2] Find contacts");
            GetContactsInfo gci = new GetContactsInfo();
            System.out.println("[Preserve Other Service] [Step 2] Contacts Id:" + oti.getContactsId());
            gci.setContactsId(oti.getContactsId());
            gci.setLoginToken(loginToken);
            GetContactsResult gcr = getContactsById(gci, httpHeaders);
            if(gcr.isStatus() == false){
                System.out.println("[Preserve Other Service][Get Contacts] Fail." + gcr.getMessage());
                otr.setStatus(false);
                otr.setMessage(gcr.getMessage());
                otr.setOrder(null);
                return otr;
            }
            System.out.println("[Preserve Other Service][Step 2] Complete");
            //3.查询座位余票信息和车次的详情
            System.out.println("[Preserve Other Service] [Step 3] Check tickets num");
            GetTripAllDetailInfo gtdi = new GetTripAllDetailInfo();

            gtdi.setFrom(oti.getFrom());
            gtdi.setTo(oti.getTo());

            gtdi.setTravelDate(oti.getDate());
            gtdi.setTripId(oti.getTripId());
            System.out.println("[Preserve Other Service] [Step 3] TripId:" + oti.getTripId());
            GetTripAllDetailResult gtdr = getTripAllDetailInformation(gtdi, httpHeaders);
            if(gtdr.isStatus() == false){
                System.out.println("[Preserve Other Service][Search For Trip Detail Information] " + gcr.getMessage());
                otr.setStatus(false);
                otr.setMessage(gcr.getMessage());
                otr.setOrder(null);
                return otr;
            }else{
                TripResponse tripResponse = gtdr.getTripResponse();
                if(oti.getSeatType() == SeatClass.FIRSTCLASS.getCode()){
                    if(tripResponse.getConfortClass() == 0){
                        System.out.println("[Preserve Other Service][Check seat is enough] " + gcr.getMessage());
                        otr.setStatus(false);
                        otr.setMessage("Seat Not Enough");
                        otr.setOrder(null);
                        return otr;
                    }
                }else{
                    if(tripResponse.getEconomyClass() == SeatClass.SECONDCLASS.getCode()){
                        if(tripResponse.getConfortClass() == 0){
                            System.out.println("[Preserve Other Service][Check seat is enough] " + gcr.getMessage());
                            otr.setStatus(false);
                            otr.setMessage("Seat Not Enough");
                            otr.setOrder(null);
                            return otr;
                        }
                    }
                }
            }
            Trip trip = gtdr.getTrip();
            System.out.println("[Preserve Other Service] [Step 3] Tickets Enough");
            //4.下达订单请求 设置order的各个信息
            System.out.println("[Preserve Other Service] [Step 4] Do Order");
            Contacts contacts = gcr.getContacts();
            Order order = new Order();
            order.setId(UUID.randomUUID());
            order.setTrainNumber(oti.getTripId());
            order.setAccountId(UUID.fromString(accountId));

            String fromStationId = queryForStationId(oti.getFrom(), httpHeaders);
            String toStationId = queryForStationId(oti.getTo(), httpHeaders);

            order.setFrom(fromStationId);
            order.setTo(toStationId);
            order.setBoughtDate(new Date());
            order.setStatus(OrderStatus.NOTPAID.getCode());
            order.setContactsDocumentNumber(contacts.getDocumentNumber());
            order.setContactsName(contacts.getName());
            order.setDocumentType(contacts.getDocumentType());

            QueryPriceInfo queryPriceInfo = new QueryPriceInfo();
            queryPriceInfo.setStartingPlaceId(fromStationId);
            queryPriceInfo.setEndPlaceId(toStationId);
            if(oti.getSeatType() == SeatClass.FIRSTCLASS.getCode()){
                queryPriceInfo.setSeatClass("confortClass");
                System.out.println("[Preserve Other Service][Seat Class] Confort Class.");
            }else if(oti.getSeatType() == SeatClass.SECONDCLASS.getCode()) {
                queryPriceInfo.setSeatClass("economyClass");
                System.out.println("[Preserve Other Service][Seat Class] Economy Class.");
            }
            queryPriceInfo.setTrainTypeId(gtdr.getTrip().getTrainTypeId());//----------------------------

            QueryForTravel query = new QueryForTravel();
            query.setTrip(trip);
            query.setStartingPlace(oti.getFrom());
            query.setEndPlace(oti.getTo());
            query.setDepartureTime(new Date());


            HttpEntity requestEntityResultForTravel = new HttpEntity(query,httpHeaders);
            ResponseEntity<ResultForTravel> reResultForTravel = restTemplate.exchange(
                    "http://ts-ticketinfo-service:15681/ticketinfo/queryForTravel",
                    HttpMethod.POST,
                    requestEntityResultForTravel,
                    ResultForTravel.class);
            ResultForTravel resultForTravel = reResultForTravel.getBody();
//            ResultForTravel resultForTravel = restTemplate.postForObject(
//                    "http://ts-ticketinfo-service:15681/ticketinfo/queryForTravel", query ,ResultForTravel.class);


//            String ticketPrice = getPrice(queryPriceInfo);
//            order.setPrice(ticketPrice);//Set ticket price


            order.setSeatClass(oti.getSeatType());
            System.out.println("[Preserve Other Service][Order] Order Travel Date:" + oti.getDate().toString());
            order.setTravelDate(oti.getDate());
            order.setTravelTime(gtdr.getTripResponse().getStartingTime());

            if(oti.getSeatType() == SeatClass.FIRSTCLASS.getCode()){//Dispatch the seat
                Ticket ticket =
                        dipatchSeat(oti.getDate(),
                                order.getTrainNumber(),fromStationId,toStationId,
                                SeatClass.FIRSTCLASS.getCode(), httpHeaders);
                order.setSeatClass(SeatClass.FIRSTCLASS.getCode());
                order.setSeatNumber("" + ticket.getSeatNo());
//                int firstClassRemainNum = gtdr.getTripResponse().getConfortClass();
//                order.setSeatNumber("FirstClass-" + firstClassRemainNum);
                order.setPrice(resultForTravel.getPrices().get("confortClass"));
            }else{
                Ticket ticket =
                        dipatchSeat(oti.getDate(),
                                order.getTrainNumber(),fromStationId,toStationId,
                                SeatClass.SECONDCLASS.getCode(), httpHeaders);
                order.setSeatClass(SeatClass.SECONDCLASS.getCode());
                order.setSeatNumber("" + ticket.getSeatNo());
//                int secondClassRemainNum = gtdr.getTripResponse().getEconomyClass();
//                order.setSeatNumber("SecondClass-" + secondClassRemainNum);
                order.setPrice(resultForTravel.getPrices().get("economyClass"));
            }
            System.out.println("[Preserve Other Service][Order Price] Price is: " + order.getPrice());
            CreateOrderInfo coi = new CreateOrderInfo();//Send info to create the order.
            coi.setLoginToken(loginToken);
            coi.setOrder(order);
            CreateOrderResult cor = createOrder(coi, httpHeaders);
            if(cor.isStatus() == false){
                System.out.println("[Preserve Other Service][Create Order Fail] Create Order Fail." +
                        "Reason:" + cor.getMessage());
                otr.setStatus(false);
                otr.setMessage(cor.getMessage());
                otr.setOrder(null);
                return otr;
            }
            System.out.println("[Preserve Other Service] [Step 4] Do Order Complete");
            otr.setStatus(true);
            otr.setMessage("Success");
            otr.setOrder(cor.getOrder());
            //5.检查保险的选择
            if(oti.getAssurance() == 0){
                System.out.println("[Preserve Service][Step 5] Do not need to buy assurance");
            }else{
                AddAssuranceResult addAssuranceResult = addAssuranceForOrder(
                        oti.getAssurance(),cor.getOrder().getId().toString(), httpHeaders);
                if(addAssuranceResult.isStatus() == true){
                    System.out.println("[Preserve Service][Step 5] Buy Assurance Success");
                }else{
                    System.out.println("[Preserve Service][Step 5] Buy Assurance Fail.");
                    otr.setMessage("Success.But Buy Assurance Fail.");
                }
            }

            //6.增加订餐
            if(oti.getFoodType() != 0){
                AddFoodOrderInfo afoi = new AddFoodOrderInfo();
                afoi.setOrderId(cor.getOrder().getId().toString());
                afoi.setFoodType(oti.getFoodType());
                afoi.setFoodName(oti.getFoodName());
                afoi.setPrice(oti.getFoodPrice());
                if(oti.getFoodType() == 2){
                    afoi.setStationName(oti.getStationName());
                    afoi.setStoreName(oti.getStoreName());
                }
                AddFoodOrderResult afor = createFoodOrder(afoi, httpHeaders);
                if(afor.isStatus()){
                    System.out.println("[Preserve Service][Step 6] Buy Food Success");
                } else {
                    System.out.println("[Preserve Service][Step 6] Buy Food Fail.");
                    otr.setMessage("Success.But Buy Food Fail.");
                }
            } else {
                System.out.println("[Preserve Service][Step 6] Do not need to buy food");
            }

            //7.增加托运
            if(null != oti.getConsigneeName() && !"".equals(oti.getConsigneeName())){
                ConsignRequest consignRequest = new ConsignRequest();
                consignRequest.setAccountId(cor.getOrder().getAccountId());
                consignRequest.setHandleDate(oti.getHandleDate());
                consignRequest.setTargetDate(cor.getOrder().getTravelDate().toString());
                consignRequest.setFrom(cor.getOrder().getFrom());
                consignRequest.setTo(cor.getOrder().getTo());
                consignRequest.setConsignee(oti.getConsigneeName());
                consignRequest.setPhone(oti.getConsigneePhone());
                consignRequest.setWeight(oti.getConsigneeWeight());
                consignRequest.setWithin(oti.isWithin());
                InsertConsignRecordResult icresult = createConsign(consignRequest, httpHeaders);
                if(icresult.isStatus()){
                    System.out.println("[Preserve Service][Step 7] Consign Success");
                } else {
                    System.out.println("[Preserve Service][Step 7] Consign Fail.");
                    otr.setMessage("Consign Fail.");
                }
            } else {
                System.out.println("[Preserve Service][Step 7] Do not need to consign");
            }

            //8.发送notification
            System.out.println("[Preserve Service]");
            GetAccountByIdInfo getAccountByIdInfo = new GetAccountByIdInfo();
            getAccountByIdInfo.setAccountId(order.getAccountId().toString());
            GetAccountByIdResult getAccountByIdResult = getAccount(getAccountByIdInfo, httpHeaders);
            if(result.isStatus() == false){
                return null;
            }

            NotifyInfo notifyInfo = new NotifyInfo();
            notifyInfo.setDate(new Date().toString());

            notifyInfo.setEmail(getAccountByIdResult.getAccount().getEmail());
            notifyInfo.setStartingPlace(order.getFrom());
            notifyInfo.setEndPlace(order.getTo());
            notifyInfo.setUsername(getAccountByIdResult.getAccount().getName());
            notifyInfo.setSeatNumber(order.getSeatNumber());
            notifyInfo.setOrderNumber(order.getId().toString());
            notifyInfo.setPrice(order.getPrice());
            notifyInfo.setSeatClass(SeatClass.getNameByCode(order.getSeatClass()));
            notifyInfo.setStartingTime(order.getTravelTime().toString());

            sendEmail(notifyInfo, httpHeaders);
        }else{
            System.out.println("[Preserve Other Service][Verify Login] Fail");
            otr.setStatus(false);
            otr.setMessage("Not Login");
            otr.setOrder(null);
        }
        return otr;
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

    public boolean sendEmail(NotifyInfo notifyInfo, HttpHeaders httpHeaders){
        System.out.println("[Preserve Service][Send Email]");

        HttpEntity requestEntitySendEmail = new HttpEntity(notifyInfo,httpHeaders);
        ResponseEntity<Boolean> reSendEmail = restTemplate.exchange(
                "http://ts-notification-service:17853/notification/order_cancel_success",
                HttpMethod.POST,
                requestEntitySendEmail,
                Boolean.class);
        boolean result = reSendEmail.getBody();
//        boolean result = restTemplate.postForObject(
//                "http://ts-notification-service:17853/notification/order_cancel_success",
//                notifyInfo,
//                Boolean.class
//        );
        return result;
    }

    public GetAccountByIdResult getAccount(GetAccountByIdInfo info, HttpHeaders httpHeaders){
        System.out.println("[Cancel Order Service][Get By Id]");

        HttpEntity requestEntitySendEmail = new HttpEntity(info,httpHeaders);
        ResponseEntity<GetAccountByIdResult> reSendEmail = restTemplate.exchange(
                "http://ts-sso-service:12349/account/findById",
                HttpMethod.POST,
                requestEntitySendEmail,
                GetAccountByIdResult.class);
        GetAccountByIdResult result = reSendEmail.getBody();
//        GetAccountByIdResult result = restTemplate.postForObject(
//                "http://ts-sso-service:12349/account/findById",
//                info,
//                GetAccountByIdResult.class
//        );
        return result;
    }

    private AddAssuranceResult addAssuranceForOrder(int assuranceType,String orderId, HttpHeaders httpHeaders){
        System.out.println("[Preserve Service][Add Assurance For Order]");
        AddAssuranceInfo info = new AddAssuranceInfo();
        info.setOrderId(orderId);
        info.setTypeIndex(assuranceType);

        HttpEntity requestAddAssuranceResult = new HttpEntity(info,httpHeaders);
        ResponseEntity<AddAssuranceResult> reAddAssuranceResult = restTemplate.exchange(
                "http://ts-assurance-service:18888/assurance/create",
                HttpMethod.POST,
                requestAddAssuranceResult,
                AddAssuranceResult.class);
        AddAssuranceResult result = reAddAssuranceResult.getBody();
//        AddAssuranceResult result = restTemplate.postForObject(
//                "http://ts-assurance-service:18888/assurance/create",
//                info,
//                AddAssuranceResult.class
//        );
        return result;
    }


    private String queryForStationId(String stationName, HttpHeaders httpHeaders){
        System.out.println("[Preserve Other Service][Get Station Name]");
        QueryForId queryForId = new QueryForId();
        queryForId.setName(stationName);

        HttpEntity requestQueryForStationId = new HttpEntity(queryForId, httpHeaders);
        ResponseEntity<String> reQueryForStationId = restTemplate.exchange(
                "http://ts-station-service:12345/station/queryForId",
                HttpMethod.POST,
                requestQueryForStationId,
                String.class);
        String stationId = reQueryForStationId.getBody();
//        String stationId = restTemplate.postForObject(
//                "http://ts-station-service:12345/station/queryForId",queryForId,String.class);
        return stationId;
    }

    private CheckResult checkSecurity(CheckInfo info, HttpHeaders httpHeaders){
        System.out.println("[Preserve Other Service][Check Security] Checking....");

        HttpEntity requestCheckResult = new HttpEntity(info, httpHeaders);
        ResponseEntity<CheckResult> reCheckResult = restTemplate.exchange(
                "http://ts-security-service:11188/security/check",
                HttpMethod.POST,
                requestCheckResult,
                CheckResult.class);
        CheckResult result = reCheckResult.getBody();
//        CheckResult result = restTemplate.postForObject("http://ts-security-service:11188/security/check",
//                info,CheckResult.class);
        return result;
    }

    private VerifyResult verifySsoLogin(String loginToken, HttpHeaders httpHeaders){
        System.out.println("[Preserve Other Service][Verify Login] Verifying....");

        HttpEntity requestCheckResult = new HttpEntity(null, httpHeaders);
        ResponseEntity<VerifyResult> reCheckResult = restTemplate.exchange(
                "http://ts-sso-service:12349/verifyLoginToken/" + loginToken,
                HttpMethod.GET,
                requestCheckResult,
                VerifyResult.class);
        VerifyResult tokenResult = reCheckResult.getBody();
//        VerifyResult tokenResult = restTemplate.getForObject(
//                "http://ts-sso-service:12349/verifyLoginToken/" + loginToken,
//                VerifyResult.class);
        return tokenResult;
    }

    private GetTripAllDetailResult getTripAllDetailInformation(GetTripAllDetailInfo gtdi, HttpHeaders httpHeaders){
        System.out.println("[Preserve Other Service][Get Trip All Detail Information] Getting....");

        HttpEntity requestGetTripAllDetailResult = new HttpEntity(gtdi, httpHeaders);
        ResponseEntity<GetTripAllDetailResult> reGetTripAllDetailResult = restTemplate.exchange(
                "http://ts-travel2-service:16346/travel2/getTripAllDetailInfo/",
                HttpMethod.POST,
                requestGetTripAllDetailResult,
                GetTripAllDetailResult.class);
        GetTripAllDetailResult gtdr = reGetTripAllDetailResult.getBody();
//        GetTripAllDetailResult gtdr = restTemplate.postForObject(
//                "http://ts-travel2-service:16346/travel2/getTripAllDetailInfo/"
//                ,gtdi,GetTripAllDetailResult.class);
        return gtdr;
    }

    private GetContactsResult getContactsById(GetContactsInfo gci, HttpHeaders httpHeaders){
        System.out.println("[Preserve Other Service][Get Contacts By Id] Getting....");

        HttpEntity requestGetContactsResult = new HttpEntity(gci, httpHeaders);
        ResponseEntity<GetContactsResult> reGetContactsResult= restTemplate.exchange(
                "http://ts-contacts-service:12347/contacts/getContactsById/",
                HttpMethod.POST,
                requestGetContactsResult,
                GetContactsResult.class);
        GetContactsResult gcr = reGetContactsResult.getBody();
//        GetContactsResult gcr = restTemplate.postForObject(
//                "http://ts-contacts-service:12347/contacts/getContactsById/"
//                ,gci,GetContactsResult.class);
        return gcr;
    }

    private CreateOrderResult createOrder(CreateOrderInfo coi, HttpHeaders httpHeaders){
        System.out.println("[Preserve Other Service][Get Contacts By Id] Creating....");

        HttpEntity requestEntityCreateOrderResult = new HttpEntity(coi,httpHeaders);
        ResponseEntity<CreateOrderResult> reCreateOrderResult = restTemplate.exchange(
                "http://ts-order-other-service:12032/orderOther/create",
                HttpMethod.POST,
                requestEntityCreateOrderResult,
                CreateOrderResult.class);
        CreateOrderResult cor = reCreateOrderResult .getBody();

//        CreateOrderResult cor = restTemplate.postForObject(
//                "http://ts-order-other-service:12032/orderOther/create"
//                ,coi,CreateOrderResult.class);
        return cor;
    }

    private AddFoodOrderResult createFoodOrder(AddFoodOrderInfo afi, HttpHeaders httpHeaders) {
        System.out.println("[Preserve Service][Add food Order] Creating....");

        HttpEntity requestEntityAddFoodOrderResult = new HttpEntity(afi,httpHeaders);
        ResponseEntity<AddFoodOrderResult> reAddFoodOrderResult = restTemplate.exchange(
                "http://ts-food-service:18856/food/createFoodOrder",
                HttpMethod.POST,
                requestEntityAddFoodOrderResult,
                AddFoodOrderResult.class);
        AddFoodOrderResult afr = reAddFoodOrderResult.getBody();
//        AddFoodOrderResult afr = restTemplate.postForObject(
//                "http://ts-food-service:18856/food/createFoodOrder"
//                ,afi,AddFoodOrderResult.class);
        return afr;
    }

    private InsertConsignRecordResult createConsign(ConsignRequest cr, HttpHeaders httpHeaders){
        System.out.println("[Preserve Service][Add Condign] Creating....");

        HttpEntity requestEntityResultForTravel = new HttpEntity(cr,httpHeaders);
        ResponseEntity<InsertConsignRecordResult> reResultForTravel = restTemplate.exchange(
                "http://ts-consign-service:16111/consign/insertConsign",
                HttpMethod.POST,
                requestEntityResultForTravel,
                InsertConsignRecordResult.class);
        InsertConsignRecordResult icr = reResultForTravel.getBody();
//        InsertConsignRecordResult icr = restTemplate.postForObject(
//                "http://ts-consign-service:16111/consign/insertConsign"
//                ,cr,InsertConsignRecordResult.class);

        return icr;
    }
}
