package travel.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import travel.domain.*;
import travel.repository.TripRepository;
import java.util.*;

@Service
public class TravelServiceImpl implements TravelService{

    @Autowired
    private TripRepository repository;

    @Autowired
    private RestTemplate restTemplate;

    @Override
    public GetRouteResult getRouteByTripId(String tripId, HttpHeaders headers){
        GetRouteResult result = new GetRouteResult();

        if(null != tripId && tripId.length() >= 2){
            TripId tripId1 = new TripId(tripId);
            Trip trip = repository.findByTripId(tripId1);
            if(trip == null){
                result.setStatus(false);
                result.setMessage("Trip Not Found");
                System.out.println("[Get Route By Trip ID] Trip Not Found:" + tripId);
                result.setRoute(null);
            }else{
                Route route = getRouteByRouteId(trip.getRouteId(), headers);
                if(route == null){
                    result.setStatus(false);
                    result.setMessage("Route Not Found");
                    System.out.println("[Get Route By Trip ID] Route Not Found:" + trip.getRouteId());
                    result.setRoute(null);
                }else{
                    result.setStatus(true);
                    result.setMessage("Success");
                    System.out.println("[Get Route By Trip ID] Success");
                    result.setRoute(route);
                }
            }
        } else {
            result.setStatus(false);
            System.out.println("[Get Route By Trip ID] TripId is invaild");
            result.setMessage("TripId is invaild");
            result.setRoute(null);
        }

        return result;
    }

    @Override
    public GetTrainTypeResult getTrainTypeByTripId(String tripId, HttpHeaders headers){
        TripId tripId1 = new TripId(tripId);
        GetTrainTypeResult result = new GetTrainTypeResult();
        Trip trip = repository.findByTripId(tripId1);
        if(trip == null){
            result.setStatus(false);
            result.setMessage("Trip Not Found");
            result.setTrainType(null);
        }else{
            TrainType train = getTrainType(trip.getTrainTypeId(), headers);
            if(train == null){
                result.setStatus(false);
                result.setMessage("Route Not Found");
                result.setTrainType(null);
            }else{
                result.setStatus(true);
                result.setMessage("Success");
                result.setTrainType(train);
            }
        }
        return result;
    }

    @Override
    public GetTripsByRouteIdResult getTripByRoute(GetTripsByRouteIdInfo info,HttpHeaders headers) {
        ArrayList<String> routeIds = info.getRouteIds();
        ArrayList<ArrayList<Trip>> tripList = new ArrayList<>();
        for(String routeId : routeIds){
            ArrayList<Trip> tempTripList = repository.findByRouteId(routeId);
            if(tempTripList == null){
                tempTripList = new ArrayList<>();
            }
            tripList.add(tempTripList);
        }
        GetTripsByRouteIdResult result = new GetTripsByRouteIdResult();
        result.setMessage("Success.");
        result.setTripsSet(tripList);
        return result;
    }

    @Override
    public String create(Information info,HttpHeaders headers){
        TripId ti = new TripId(info.getTripId());
        if(repository.findByTripId(ti) == null){
            Trip trip = new Trip(ti,info.getTrainTypeId(),info.getStartingStationId(),
                    info.getStationsId(),info.getTerminalStationId(),info.getStartingTime(),info.getEndTime());
            trip.setRouteId(info.getRouteId());
            repository.save(trip);
            return "Create trip:" + ti.toString() + ".";
        }else{
            return "Trip "+ info.getTripId().toString() +" already exists";
        }
    }

    @Override
    public Trip retrieve(Information2 info,HttpHeaders headers){
        TripId ti = new TripId(info.getTripId());
        if(repository.findByTripId(ti) != null){
            return repository.findByTripId(ti);
        }else{
            return null;
        }
    }

    @Override
    public String update(Information info,HttpHeaders headers){
        TripId ti = new TripId(info.getTripId());
        if(repository.findByTripId(ti) != null){
            Trip trip = new Trip(ti,info.getTrainTypeId(),info.getStartingStationId(),
                    info.getStationsId(),info.getTerminalStationId(),info.getStartingTime(),info.getEndTime());
            trip.setRouteId(info.getRouteId());
            repository.save(trip);
            return "Update trip:" + ti.toString();
        }else{
            return "Trip "+ info.getTripId().toString() +" doesn't exists";
        }
    }

    @Override
    public String delete(Information2 info,HttpHeaders headers){
        TripId ti = new TripId(info.getTripId());
        if(repository.findByTripId(ti) != null){
            repository.deleteByTripId(ti);
            return "Delete trip:" +info.getTripId().toString()+ ".";
        }else{
            return "Trip "+info.getTripId().toString()+" doesn't exist.";
        }
    }

    @Override
    public ArrayList<TripResponse> query(QueryInfo info, HttpHeaders headers){

        //获取要查询的车次的起始站和到达站。这里收到的起始站和到达站都是站的名称，所以需要发两个请求转换成站的id
        String startingPlaceName = info.getStartingPlace();
        String endPlaceName = info.getEndPlace();
        String startingPlaceId = queryForStationId(startingPlaceName, headers);
        String endPlaceId = queryForStationId(endPlaceName, headers);

        //这个是最终的结果
        ArrayList<TripResponse> list = new ArrayList<>();

        //查询所有的车次信息
        ArrayList<Trip> allTripList = repository.findAll();
        for(Trip tempTrip : allTripList){
            //拿到这个车次的具体路线表
            Route tempRoute = getRouteByRouteId(tempTrip.getRouteId(), headers);
            //检查这个车次的路线表。检查要求的起始站和到达站在不在车次路线的停靠站列表中
            //并检查起始站的位置在到达站之前。满足以上条件的车次被加入返回列表
            if(tempRoute.getStations().contains(startingPlaceId) &&
                    tempRoute.getStations().contains(endPlaceId) &&
                    tempRoute.getStations().indexOf(startingPlaceId) < tempRoute.getStations().indexOf(endPlaceId)){
                TripResponse response = getTickets(tempTrip,tempRoute,startingPlaceId,endPlaceId,startingPlaceName,endPlaceName,info.getDepartureTime(), headers);
                if(response == null){
                    return null;
                }
                list.add(response);
            }
        }
        return list;
    }

    @Override
    public GetTripAllDetailResult getTripAllDetailInfo(GetTripAllDetailInfo gtdi, HttpHeaders headers){
        GetTripAllDetailResult gtdr = new GetTripAllDetailResult();
        System.out.println("[TravelService] [GetTripAllDetailInfo] TripId:" + gtdi.getTripId());
        Trip trip = repository.findByTripId(new TripId(gtdi.getTripId()));
        if(trip == null){
            gtdr.setStatus(false);
            gtdr.setMessage("Trip Not Exist");
            gtdr.setTripResponse(null);
            gtdr.setTrip(null);
        }else{

            String startingPlaceName = gtdi.getFrom();
            String endPlaceName = gtdi.getTo();
            String startingPlaceId = queryForStationId(startingPlaceName,headers);
            String endPlaceId = queryForStationId(endPlaceName,headers);
            Route tempRoute = getRouteByRouteId(trip.getRouteId(),headers);

            TripResponse tripResponse = getTickets(trip,tempRoute,startingPlaceId,endPlaceId,gtdi.getFrom(),gtdi.getTo(),gtdi.getTravelDate(),headers);
            if(tripResponse == null){
                gtdr.setStatus(false);
                gtdr.setMessage("Cannot found TripResponse");
                gtdr.setTripResponse(null);
                gtdr.setTrip(null);
            }else{
                gtdr.setStatus(true);
                gtdr.setMessage("Success");
                gtdr.setTripResponse(tripResponse);
                gtdr.setTrip(repository.findByTripId(new TripId(gtdi.getTripId())));
            }
        }
        return gtdr;
    }

    private TripResponse getTickets(Trip trip, Route route, String startingPlaceId, String endPlaceId, String startingPlaceName, String endPlaceName, Date departureTime, HttpHeaders headers){

        //判断所查日期是否在当天及之后
        if(!afterToday(departureTime)){
            return null;
        }

        QueryForTravel query = new QueryForTravel();
        query.setTrip(trip);
        query.setStartingPlace(startingPlaceName);
        query.setEndPlace(endPlaceName);
        query.setDepartureTime(departureTime);

        HttpEntity requestEntity = new HttpEntity(query,headers);
        ResponseEntity<ResultForTravel> re = restTemplate.exchange(
                "http://ts-ticketinfo-service:15681/ticketinfo/queryForTravel",
                HttpMethod.POST,
                requestEntity,
                ResultForTravel.class);
        ResultForTravel resultForTravel = re.getBody();


        if(resultForTravel.isStatus() == false && resultForTravel.getMessage().contains("OOM")){
            System.out.println("报出了OOOOOOOOOOMMMMMMMMMMMMMMMMMMMM");
            return null;
        }

//        ResultForTravel resultForTravel = restTemplate.postForObject(
//                "http://ts-ticketinfo-service:15681/ticketinfo/queryForTravel", query ,ResultForTravel.class);

        //车票订单_高铁动车（已购票数）
        QuerySoldTicket information = new QuerySoldTicket(departureTime,trip.getTripId().toString());
        requestEntity = new HttpEntity(information,headers);
        ResponseEntity<ResultSoldTicket> re2 = restTemplate.exchange(
                "http://ts-order-service:12031/order/calculate",
                HttpMethod.POST,
                requestEntity,
                ResultSoldTicket.class);
        ResultSoldTicket result = re2.getBody();

//        ResultSoldTicket result = restTemplate.postForObject(
//                "http://ts-order-service:12031/order/calculate", information ,ResultSoldTicket.class);
        if(result == null){
            System.out.println("soldticket Info doesn't exist");
            return null;
        }
        //设置返回的车票信息
        TripResponse response = new TripResponse();
        if(queryForStationId(startingPlaceName,headers).equals(trip.getStartingStationId()) &&
                queryForStationId(endPlaceName,headers).equals(trip.getTerminalStationId())){
            response.setConfortClass(50);
            response.setEconomyClass(50);
        }else{
            response.setConfortClass(50);
            response.setEconomyClass(50);
        }

        int first = getRestTicketNumber(departureTime,trip.getTripId().toString(),
                startingPlaceName,endPlaceName,SeatClass.FIRSTCLASS.getCode(),headers);

        int second = getRestTicketNumber(departureTime,trip.getTripId().toString(),
                startingPlaceName,endPlaceName,SeatClass.SECONDCLASS.getCode(),headers);
        response.setConfortClass(first);
        response.setEconomyClass(second);

        response.setStartingStation(startingPlaceName);
        response.setTerminalStation(endPlaceName);

        //计算车从起始站开出的距离
        int indexStart = route.getStations().indexOf(startingPlaceId);
        int indexEnd = route.getStations().indexOf(endPlaceId);
        int distanceStart = route.getDistances().get(indexStart) - route.getDistances().get(0);
        int distanceEnd = route.getDistances().get(indexEnd) - route.getDistances().get(0);
        TrainType trainType = getTrainType(trip.getTrainTypeId(), headers);
        //根据列车平均运行速度计算列车运行时间
        int minutesStart = 60 * distanceStart / trainType.getAverageSpeed();
        int minutesEnd = 60 * distanceEnd / trainType.getAverageSpeed();

        Calendar calendarStart = Calendar.getInstance();
        calendarStart.setTime(trip.getStartingTime());
        calendarStart.add(Calendar.MINUTE,minutesStart);
        response.setStartingTime(calendarStart.getTime());
        System.out.println("[Train Service]计算时间：" + minutesStart  + " 时间:" + calendarStart.getTime().toString());

        Calendar calendarEnd = Calendar.getInstance();
        calendarEnd.setTime(trip.getStartingTime());
        calendarEnd.add(Calendar.MINUTE,minutesEnd);
        response.setEndTime(calendarEnd.getTime());
        System.out.println("[Train Service]计算时间：" + minutesEnd  + " 时间:" + calendarEnd.getTime().toString());

        response.setTripId(new TripId(result.getTrainNumber()));
        response.setTrainTypeId(trip.getTrainTypeId());
        response.setPriceForConfortClass(resultForTravel.getPrices().get("confortClass"));
        response.setPriceForEconomyClass(resultForTravel.getPrices().get("economyClass"));

        return response;
}

    @Override
    public List<Trip> queryAll(HttpHeaders headers){
        return repository.findAll();
    }

    private static boolean afterToday(Date date) {
        Calendar calDateA = Calendar.getInstance();
        Date today = new Date();
        calDateA.setTime(today);

        Calendar calDateB = Calendar.getInstance();
        calDateB.setTime(date);

        if(calDateA.get(Calendar.YEAR) > calDateB.get(Calendar.YEAR)){
            return false;
        }else if(calDateA.get(Calendar.YEAR) == calDateB.get(Calendar.YEAR)){
            if(calDateA.get(Calendar.MONTH) > calDateB.get(Calendar.MONTH)){
                return false;
            }else if(calDateA.get(Calendar.MONTH) == calDateB.get(Calendar.MONTH)){
                if(calDateA.get(Calendar.DAY_OF_MONTH) > calDateB.get(Calendar.DAY_OF_MONTH)){
                    return false;
                }else{
                    return true;
                }
            }else{
                return true;
            }
        }else{
            return true;
        }
    }

    private TrainType getTrainType(String trainTypeId, HttpHeaders headers){
        GetTrainTypeInformation info = new GetTrainTypeInformation();
        info.setId(trainTypeId);
        HttpEntity requestEntity = new HttpEntity(info,headers);
        ResponseEntity<TrainType> re = restTemplate.exchange(
                "http://ts-train-service:14567/train/retrieve",
                HttpMethod.POST,
                requestEntity,
                TrainType.class);
        TrainType trainType = re.getBody();
//        TrainType trainType = restTemplate.postForObject(
//                "http://ts-train-service:14567/train/retrieve", info, TrainType.class);
        return trainType;
    }

    private String queryForStationId(String stationName, HttpHeaders headers){
        QueryForStationId query = new QueryForStationId();
        query.setName(stationName);
        HttpEntity requestEntity = new HttpEntity(query,headers);
        ResponseEntity<String> re = restTemplate.exchange(
                "http://ts-ticketinfo-service:15681/ticketinfo/queryForStationId",
                HttpMethod.POST,
                requestEntity,
                String.class);
        String id = re.getBody();
//        String id = restTemplate.postForObject(
//                "http://ts-ticketinfo-service:15681/ticketinfo/queryForStationId", query ,String.class);
        return id;
    }

    private Route getRouteByRouteId(String routeId, HttpHeaders headers){
        System.out.println("[Travel Service][Get Route By Id] Route ID：" + routeId);
        HttpEntity requestEntity = new HttpEntity(headers);
        ResponseEntity<GetRouteResult> re = restTemplate.exchange(
                "http://ts-route-service:11178/route/queryById/" + routeId,
                HttpMethod.GET,
                requestEntity,
                GetRouteResult.class);
        GetRouteResult result = re.getBody();
//        GetRouteResult result = restTemplate.getForObject(
//                "http://ts-route-service:11178/route/queryById/" + routeId,
//                GetRouteResult.class);
        if(result.isStatus() == false){
            System.out.println("[Travel Service][Get Route By Id] Fail." + result.getMessage());
            return null;
        }else{
            System.out.println("[Travel Service][Get Route By Id] Success.");
            return result.getRoute();
        }
    }

    private int getRestTicketNumber(Date travelDate, String trainNumber, String startStationName, String endStationName, int seatType, HttpHeaders headers) {
        SeatRequest seatRequest = new SeatRequest();

        String fromId = queryForStationId(startStationName,headers);
        String toId = queryForStationId(endStationName,headers);

        seatRequest.setDestStation(toId);
        seatRequest.setStartStation(fromId);
        seatRequest.setTrainNumber(trainNumber);
        seatRequest.setTravelDate(travelDate);
        seatRequest.setSeatType(seatType);

        HttpEntity requestEntity = new HttpEntity(seatRequest,headers);
        ResponseEntity<Integer> re = restTemplate.exchange(
                "http://ts-seat-service:18898/seat/getLeftTicketOfInterval",
                HttpMethod.POST,
                requestEntity,
                Integer.class);
        int restNumber = re.getBody();
//        int restNumber = restTemplate.postForObject(
//                "http://ts-seat-service:18898/seat/getLeftTicketOfInterval",
//                seatRequest,Integer.class
//        );

        return restNumber;
    }

    @Override
    public AdminFindAllResult adminQueryAll(HttpHeaders headers) {
        List<Trip> trips = repository.findAll();
        ArrayList<AdminTrip> adminTrips = new ArrayList<AdminTrip>();
        for(Trip trip : trips){
            AdminTrip adminTrip = new AdminTrip();
            adminTrip.setTrip(trip);
            adminTrip.setRoute(getRouteByRouteId(trip.getRouteId(),headers));
            adminTrip.setTrainType(getTrainType(trip.getTrainTypeId(),headers));
            adminTrips.add(adminTrip);
        }
        AdminFindAllResult result = new AdminFindAllResult();
        result.setStatus(true);
        result.setMessage("Travel Service Admin Query All Travel Success");
        result.setTrips(adminTrips);
        return result;
    }
}
