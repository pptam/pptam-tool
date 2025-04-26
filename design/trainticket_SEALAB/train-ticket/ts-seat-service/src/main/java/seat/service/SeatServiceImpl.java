package seat.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.integration.dsl.http.Http;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import seat.domain.*;

import java.util.List;
import java.util.Random;
import java.util.Set;

@Service
public class SeatServiceImpl implements SeatService {
    @Autowired
    RestTemplate restTemplate;

    @Override
    public Ticket distributeSeat(SeatRequest seatRequest,HttpHeaders headers){
        GetRouteResult routeResult;
        GetTrainTypeResult trainTypeResult;
        LeftTicketInfo leftTicketInfo;

        ResponseEntity<GetRouteResult> re;
        ResponseEntity<GetTrainTypeResult> re2;
        ResponseEntity<LeftTicketInfo> re3;

        //区分G\D开头和其它车次
        String trainNumber = seatRequest.getTrainNumber();
        if(trainNumber.startsWith("G") || trainNumber.startsWith("D") ){
            System.out.println("[SeatService distributeSeat] TrainNumber start with G|D");

            //调用微服务，查询获得车次的所有站点信息
            HttpEntity requestEntity = new HttpEntity(headers);
            re = restTemplate.exchange(
                    "http://ts-travel-service:12346/travel/getRouteByTripId/"+ seatRequest.getTrainNumber(),
                    HttpMethod.GET,
                    requestEntity,
                    GetRouteResult.class);
            routeResult = re.getBody();
//            routeResult = restTemplate.getForObject(
//                    "http://ts-travel-service:12346/travel/getRouteByTripId/"+ seatRequest.getTrainNumber() ,GetRouteResult.class);
            System.out.println("[SeatService distributeSeat] The result of getRouteResult is " + routeResult.getMessage());

            //调用微服务，查询获得余票信息：该车次指定座型已售Ticket的set集合
            requestEntity = new HttpEntity(seatRequest,headers);
            re3 = restTemplate.exchange(
                    "http://ts-order-service:12031/order/getTicketListByDateAndTripId",
                    HttpMethod.POST,
                    requestEntity,
                    LeftTicketInfo.class);
            leftTicketInfo = re3.getBody();
//            leftTicketInfo = restTemplate.postForObject(
//                    "http://ts-order-service:12031/order/getTicketListByDateAndTripId", seatRequest ,LeftTicketInfo.class);

            //调用微服务，查询该车次指定座型总数量
            requestEntity = new HttpEntity(headers);
            re2 = restTemplate.exchange(
                    "http://ts-travel-service:12346/travel/getTrainTypeByTripId/" + seatRequest.getTrainNumber(),
                    HttpMethod.GET,
                    requestEntity,
                    GetTrainTypeResult.class);
            trainTypeResult = re2.getBody();

//            trainTypeResult = restTemplate.getForObject(
//                    "http://ts-travel-service:12346/travel/getTrainTypeByTripId/" + seatRequest.getTrainNumber() ,GetTrainTypeResult.class);
            System.out.println("[SeatService distributeSeat] The result of getTrainTypeResult is " + trainTypeResult.getMessage());
        }
        else{
            System.out.println("[SeatService] TrainNumber start with other capital");
            //调用微服务，查询获得车次的所有站点信息
            HttpEntity requestEntity = new HttpEntity(headers);
            re = restTemplate.exchange(
                    "http://ts-travel2-service:16346/travel2/getRouteByTripId/" + seatRequest.getTrainNumber(),
                    HttpMethod.GET,
                    requestEntity,
                    GetRouteResult.class);
            routeResult = re.getBody();
//            routeResult = restTemplate.getForObject(
//                    "http://ts-travel2-service:16346/travel2/getRouteByTripId/" + seatRequest.getTrainNumber() ,GetRouteResult.class);
            System.out.println("[SeatService distributeSeat] The result of getRouteResult is " + routeResult.getMessage());

            //调用微服务，查询获得余票信息：该车次指定座型已售Ticket的set集合
            requestEntity = new HttpEntity(seatRequest,headers);
            re3 = restTemplate.exchange(
                    "http://ts-order-other-service:12032/orderOther/getTicketListByDateAndTripId",
                    HttpMethod.POST,
                    requestEntity,
                    LeftTicketInfo.class);
            leftTicketInfo = re3.getBody();
//            leftTicketInfo = restTemplate.postForObject(
//                    "http://ts-order-other-service:12032/orderOther/getTicketListByDateAndTripId", seatRequest ,LeftTicketInfo.class);

            //调用微服务，查询该车次指定座型总数量
            requestEntity = new HttpEntity(headers);
            re2 = restTemplate.exchange(
                    "http://ts-travel2-service:16346/travel2/getTrainTypeByTripId/" + seatRequest.getTrainNumber(),
                    HttpMethod.GET,
                    requestEntity,
                    GetTrainTypeResult.class);
            trainTypeResult = re2.getBody();
//            trainTypeResult = restTemplate.getForObject(
//                    "http://ts-travel2-service:16346/travel2/getTrainTypeByTripId/" + seatRequest.getTrainNumber(), GetTrainTypeResult.class);
            System.out.println("[SeatService distributeSeat] The result of getTrainTypeResult is " + trainTypeResult.getMessage());
        }


        //分配座位
        List<String> stationList = routeResult.getRoute().getStations();
        int seatTotalNum;
        if(seatRequest.getSeatType() == SeatClass.FIRSTCLASS.getCode()) {
            seatTotalNum = trainTypeResult.getTrainType().getConfortClass();
            System.out.println("[SeatService distributeSeat] The request seat type is confortClass and the total num is " + seatTotalNum);
        }
        else {
            seatTotalNum = trainTypeResult.getTrainType().getEconomyClass();
            System.out.println("[SeatService distributeSeat] The request seat type is economyClass and the total num is " + seatTotalNum);
        }
        String startStation = seatRequest.getStartStation();
        Ticket ticket = new Ticket();
        ticket.setStartStation(startStation);
        ticket.setDestStation(seatRequest.getDestStation());
        Set<Ticket> soldTickets = leftTicketInfo.getSoldTickets();

        //优先分配已经售出的票
        for(Ticket soldTicket : soldTickets){
            String soldTicketDestStation = soldTicket.getDestStation();
            //售出的票的终点站在请求的起点之前，则可以分配出去
            if(stationList.indexOf(soldTicketDestStation) < stationList.indexOf(startStation)){
                ticket.setSeatNo(soldTicket.getSeatNo());
                System.out.println("[SeatService distributeSeat] Use the previous distributed seat number!" + soldTicket.getSeatNo());
                return ticket;
            }
        }

        //分配新的票
        Random rand = new Random();
        int range = seatTotalNum;
        int seat = rand.nextInt(range) + 1;
        while (isContained(soldTickets, seat)){
            seat = rand.nextInt(range) + 1;
        }
        ticket.setSeatNo(seat);
        System.out.println("[SeatService distributeSeat] Use a new seat number!" + seat);
        return ticket;
    }

    //检查座位号是否已经被使用
    private boolean isContained( Set<Ticket> soldTickets, int seat){
        boolean result = false;
        for(Ticket soldTicket : soldTickets){
            if(soldTicket.getSeatNo() == seat){
                return true;
            }
        }
        return result;
    }

    @Override
    public int getLeftTicketOfInterval(SeatRequest seatRequest,HttpHeaders headers){
        int numOfLeftTicket = 0;
        GetRouteResult routeResult;
        GetTrainTypeResult trainTypeResult;
        LeftTicketInfo leftTicketInfo;

        ResponseEntity<GetRouteResult> re;
        ResponseEntity<GetTrainTypeResult> re2;
        ResponseEntity<LeftTicketInfo> re3;

        //区分G\D开头和其它车次
        String trainNumber = seatRequest.getTrainNumber();
        if(trainNumber.startsWith("G") || trainNumber.startsWith("D") ){
            System.out.println("[SeatService getLeftTicketOfInterval] TrainNumber start with G|D");

            //调用微服务，查询获得车次的所有站点信息
            HttpEntity requestEntity = new HttpEntity(headers);
            re = restTemplate.exchange(
                    "http://ts-travel-service:12346/travel/getRouteByTripId/"+ seatRequest.getTrainNumber(),
                    HttpMethod.GET,
                    requestEntity,
                    GetRouteResult.class);
            routeResult = re.getBody();
//            routeResult = restTemplate.getForObject(
//                    "http://ts-travel-service:12346/travel/getRouteByTripId/"+ seatRequest.getTrainNumber() ,GetRouteResult.class);
            System.out.println("[SeatService getLeftTicketOfInterval] The result of getRouteResult is " + routeResult.getMessage());

            //调用微服务，查询获得余票信息：该车次指定座型已售Ticket的set集合
            requestEntity = new HttpEntity(seatRequest,headers);
            re3 = restTemplate.exchange(
                    "http://ts-order-service:12031/order/getTicketListByDateAndTripId",
                    HttpMethod.POST,
                    requestEntity,
                    LeftTicketInfo.class);
            leftTicketInfo = re3.getBody();
//            leftTicketInfo = restTemplate.postForObject(
//                    "http://ts-order-service:12031/order/getTicketListByDateAndTripId", seatRequest ,LeftTicketInfo.class);

            //调用微服务，查询该车次指定座型总数量
            requestEntity = new HttpEntity(headers);
            re2 = restTemplate.exchange(
                    "http://ts-travel-service:12346/travel/getTrainTypeByTripId/" + seatRequest.getTrainNumber(),
                    HttpMethod.GET,
                    requestEntity,
                    GetTrainTypeResult.class);
            trainTypeResult = re2.getBody();
//            trainTypeResult = restTemplate.getForObject(
//                    "http://ts-travel-service:12346/travel/getTrainTypeByTripId/" + seatRequest.getTrainNumber() ,GetTrainTypeResult.class);
            System.out.println("[SeatService getLeftTicketOfInterval] The result of getTrainTypeResult is " + trainTypeResult.getMessage());
        }
        else{
            System.out.println("[SeatService getLeftTicketOfInterval] TrainNumber start with other capital");
            //调用微服务，查询获得车次的所有站点信息
            HttpEntity requestEntity = new HttpEntity(headers);
            re = restTemplate.exchange(
                    "http://ts-travel2-service:16346/travel2/getRouteByTripId/" + seatRequest.getTrainNumber(),
                    HttpMethod.GET,
                    requestEntity,
                    GetRouteResult.class);
            routeResult = re.getBody();
//            routeResult = restTemplate.getForObject(
//                    "http://ts-travel2-service:16346/travel2/getRouteByTripId/" + seatRequest.getTrainNumber() ,GetRouteResult.class);
            System.out.println("[SeatService getLeftTicketOfInterval] The result of getRouteResult is " + routeResult.getMessage());

            //调用微服务，查询获得余票信息：该车次指定座型已售Ticket的set集合
            requestEntity = new HttpEntity(seatRequest,headers);
            re3 = restTemplate.exchange(
                    "http://ts-order-other-service:12032/orderOther/getTicketListByDateAndTripId",
                    HttpMethod.POST,
                    requestEntity,
                    LeftTicketInfo.class);
            leftTicketInfo = re3.getBody();
//            leftTicketInfo = restTemplate.postForObject(
//                    "http://ts-order-other-service:12032/orderOther/getTicketListByDateAndTripId", seatRequest ,LeftTicketInfo.class);

            //调用微服务，查询该车次指定座型总数量
            requestEntity = new HttpEntity(headers);
            re2 = restTemplate.exchange(
                    "http://ts-travel2-service:16346/travel2/getTrainTypeByTripId/" + seatRequest.getTrainNumber(),
                    HttpMethod.GET,
                    requestEntity,
                    GetTrainTypeResult.class);
            trainTypeResult = re2.getBody();
//            trainTypeResult = restTemplate.getForObject(
//                    "http://ts-travel2-service:16346/travel2/getTrainTypeByTripId/" + seatRequest.getTrainNumber(), GetTrainTypeResult.class);
            System.out.println("[SeatService getLeftTicketOfInterval] The result of getTrainTypeResult is " + trainTypeResult.getMessage());
        }

        //统计特定区间座位余票
        List<String> stationList = routeResult.getRoute().getStations();
        int seatTotalNum;
        if(seatRequest.getSeatType() == SeatClass.FIRSTCLASS.getCode()) {
            seatTotalNum = trainTypeResult.getTrainType().getConfortClass();
            System.out.println("[SeatService getLeftTicketOfInterval] The request seat type is confortClass and the total num is " + seatTotalNum);
        }
        else {
            seatTotalNum = trainTypeResult.getTrainType().getEconomyClass();
            System.out.println("[SeatService getLeftTicketOfInterval] The request seat type is economyClass and the total num is " + seatTotalNum);
        }
        String startStation = seatRequest.getStartStation();
        Set<Ticket> soldTickets = leftTicketInfo.getSoldTickets();

        //统计已经售出去的票是否可供使用
        for(Ticket soldTicket : soldTickets){
            String soldTicketDestStation = soldTicket.getDestStation();
            //售出的票的终点站在请求的起点之前，则可以分配出去
            if(stationList.indexOf(soldTicketDestStation) < stationList.indexOf(startStation)){
                System.out.println("[SeatService getLeftTicketOfInterval] The previous distributed seat number is usable!" + soldTicket.getSeatNo());
                numOfLeftTicket++;
            }
        }
        //统计未售出的票

        double direstPart = getDirectProportion(headers);
        Route route = routeResult.getRoute();
        if(route.getStations().get(0).equals(seatRequest.getStartStation()) &&
                route.getStations().get(route.getStations().size()-1).equals(seatRequest.getDestStation())){
            //do nothing
        }else{
            direstPart = 1.0 - direstPart;
        }

        int unusedNum = (int)(seatTotalNum * direstPart) - soldTickets.size();
        numOfLeftTicket += unusedNum;

        return numOfLeftTicket;
    }

    private double getDirectProportion(HttpHeaders headers){

        QueryConfig queryConfig = new QueryConfig("DirectTicketAllocationProportion");
        HttpEntity requestEntity = new HttpEntity(queryConfig,headers);
        ResponseEntity<String> re = restTemplate.exchange(
                "http://ts-config-service:15679//config/query",
                HttpMethod.POST,
                requestEntity,
                String.class);
        String configValue = re.getBody();
//        String configValue = restTemplate.postForObject(
//                "http://ts-config-service:15679//config/query",
//                queryConfig,String.class);

        return Double.parseDouble(configValue);
    }
}