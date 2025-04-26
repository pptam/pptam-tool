package travelplan.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import travelplan.domain.*;
import java.util.ArrayList;
import java.util.Date;

@Service
public class TravelPlanServiceImpl implements TravelPlanService{

    @Autowired
    private RestTemplate restTemplate;


    @Override
    public TransferTravelSearchResult getTransferSearch(TransferTravelSearchInfo info, HttpHeaders headers) {

        QueryInfo queryInfoFirstSection = new QueryInfo();
        queryInfoFirstSection.setDepartureTime(info.getTravelDate());
        queryInfoFirstSection.setStartingPlace(info.getFromStationName());
        queryInfoFirstSection.setEndPlace(info.getViaStationName());

        ArrayList<TripResponse> firstSectionFromHighSpeed;
        ArrayList<TripResponse> firstSectionFromNormal;
        firstSectionFromHighSpeed = tripsFromHighSpeed(queryInfoFirstSection,headers);
        firstSectionFromNormal = tripsFromNormal(queryInfoFirstSection,headers);

        QueryInfo queryInfoSecondSectoin = new QueryInfo();
        queryInfoSecondSectoin.setDepartureTime(info.getTravelDate());
        queryInfoSecondSectoin.setStartingPlace(info.getViaStationName());
        queryInfoSecondSectoin.setEndPlace(info.getToStationName());

        ArrayList<TripResponse> secondSectionFromHighSpeed;
        ArrayList<TripResponse> secondSectionFromNormal;
        secondSectionFromHighSpeed = tripsFromHighSpeed(queryInfoSecondSectoin,headers);
        secondSectionFromNormal = tripsFromNormal(queryInfoSecondSectoin,headers);

        ArrayList<TripResponse> firstSection = new ArrayList<>();
        firstSection.addAll(firstSectionFromHighSpeed);
        firstSection.addAll(firstSectionFromNormal);

        ArrayList<TripResponse> secondSection = new ArrayList<>();
        secondSection.addAll(secondSectionFromHighSpeed);
        secondSection.addAll(secondSectionFromNormal);

        TransferTravelSearchResult result = new TransferTravelSearchResult();
        result.setStatus(true);
        result.setMessage("Success.");
        result.setFirstSectionResult(firstSection);
        result.setSecondSectionResult(secondSection);

        return result;
    }

    @Override
    public TravelAdvanceResult getCheapest(QueryInfo info, HttpHeaders headers) {
        GetRoutePlanInfo routePlanInfo = new GetRoutePlanInfo();
        routePlanInfo.setNum(5);
        routePlanInfo.setFormStationName(info.getStartingPlace());
        routePlanInfo.setToStationName(info.getEndPlace());
        routePlanInfo.setTravelDate(info.getDepartureTime());
        RoutePlanResults routePlanResults = getRoutePlanResultCheapest(routePlanInfo,headers);

        TravelAdvanceResult travelAdvanceResult = new TravelAdvanceResult();

        if(routePlanResults.isStatus() == true){
            ArrayList<RoutePlanResultUnit> routePlanResultUnits = routePlanResults.getResults();
            travelAdvanceResult.setStatus(true);
            travelAdvanceResult.setMessage("Success");
            ArrayList<TravelAdvanceResultUnit> lists = new ArrayList<>();
            for(int i = 0; i < routePlanResultUnits.size(); i++){
                RoutePlanResultUnit tempUnit = routePlanResultUnits.get(i);
                TravelAdvanceResultUnit newUnit = new TravelAdvanceResultUnit();
                newUnit.setTripId(tempUnit.getTripId());
                newUnit.setTrainTypeId(tempUnit.getTrainTypeId());
                newUnit.setFromStationName(tempUnit.getFromStationName());
                newUnit.setToStationName(tempUnit.getToStationName());
                ArrayList<String> stops = transferStationIdToStationName(tempUnit.getStopStations(),headers);
                newUnit.setStopStations(stops);
                newUnit.setPriceForFirstClassSeat(tempUnit.getPriceForFirstClassSeat());
                newUnit.setPriceForSecondClassSeat(tempUnit.getPriceForSecondClassSeat());
                newUnit.setStartingTime(tempUnit.getStartingTime());
                newUnit.setEndTime(tempUnit.getEndTime());
                int first = getRestTicketNumber(info.getDepartureTime(),tempUnit.getTripId(),
                        tempUnit.getFromStationName(),tempUnit.getToStationName(),SeatClass.FIRSTCLASS.getCode(),headers);

                int second = getRestTicketNumber(info.getDepartureTime(),tempUnit.getTripId(),
                        tempUnit.getFromStationName(),tempUnit.getToStationName(),SeatClass.SECONDCLASS.getCode(),headers);
                newUnit.setNumberOfRestTicketFirstClass(first);
                newUnit.setNumberOfRestTicketSecondClass(second);
                lists.add(newUnit);
            }
            travelAdvanceResult.setTravelAdvanceResultUnits(lists);
        }else{
            travelAdvanceResult.setStatus(false);
            travelAdvanceResult.setMessage("Cannot Find");
            travelAdvanceResult.setTravelAdvanceResultUnits(new ArrayList<>());
        }

        return travelAdvanceResult;
}

    @Override
    public TravelAdvanceResult getQuickest(QueryInfo info, HttpHeaders headers) {
        GetRoutePlanInfo routePlanInfo = new GetRoutePlanInfo();
        routePlanInfo.setNum(5);
        routePlanInfo.setFormStationName(info.getStartingPlace());
        routePlanInfo.setToStationName(info.getEndPlace());
        routePlanInfo.setTravelDate(info.getDepartureTime());
        RoutePlanResults routePlanResults = getRoutePlanResultQuickest(routePlanInfo,headers);

        TravelAdvanceResult travelAdvanceResult = new TravelAdvanceResult();

        if(routePlanResults.isStatus() == true){
            ArrayList<RoutePlanResultUnit> routePlanResultUnits = routePlanResults.getResults();
            travelAdvanceResult.setStatus(true);
            travelAdvanceResult.setMessage("Success");
            ArrayList<TravelAdvanceResultUnit> lists = new ArrayList<>();
            for(int i = 0; i < routePlanResultUnits.size(); i++){
                RoutePlanResultUnit tempUnit = routePlanResultUnits.get(i);
                TravelAdvanceResultUnit newUnit = new TravelAdvanceResultUnit();
                newUnit.setTripId(tempUnit.getTripId());
                newUnit.setTrainTypeId(tempUnit.getTrainTypeId());
                newUnit.setFromStationName(tempUnit.getFromStationName());
                newUnit.setToStationName(tempUnit.getToStationName());

                ArrayList<String> stops = transferStationIdToStationName(tempUnit.getStopStations(),headers);
                newUnit.setStopStations(stops);

                newUnit.setPriceForFirstClassSeat(tempUnit.getPriceForFirstClassSeat());
                newUnit.setPriceForSecondClassSeat(tempUnit.getPriceForSecondClassSeat());
                newUnit.setStartingTime(tempUnit.getStartingTime());
                newUnit.setEndTime(tempUnit.getEndTime());
                int first = getRestTicketNumber(info.getDepartureTime(),tempUnit.getTripId(),
                        tempUnit.getFromStationName(),tempUnit.getToStationName(),SeatClass.FIRSTCLASS.getCode(),headers);

                int second = getRestTicketNumber(info.getDepartureTime(),tempUnit.getTripId(),
                        tempUnit.getFromStationName(),tempUnit.getToStationName(),SeatClass.SECONDCLASS.getCode(),headers);
                newUnit.setNumberOfRestTicketFirstClass(first);
                newUnit.setNumberOfRestTicketSecondClass(second);
                lists.add(newUnit);
            }
            travelAdvanceResult.setTravelAdvanceResultUnits(lists);
        }else{
            travelAdvanceResult.setStatus(false);
            travelAdvanceResult.setMessage("Cannot Find");
            travelAdvanceResult.setTravelAdvanceResultUnits(new ArrayList<>());
        }

        return travelAdvanceResult;

    }

    @Override
    public TravelAdvanceResult getMinStation(QueryInfo info, HttpHeaders headers) {
        GetRoutePlanInfo routePlanInfo = new GetRoutePlanInfo();
        routePlanInfo.setNum(5);
        routePlanInfo.setFormStationName(info.getStartingPlace());
        routePlanInfo.setToStationName(info.getEndPlace());
        routePlanInfo.setTravelDate(info.getDepartureTime());
        RoutePlanResults routePlanResults = getRoutePlanResultMinStation(routePlanInfo,headers);
        TravelAdvanceResult travelAdvanceResult = new TravelAdvanceResult();

        if(routePlanResults.isStatus() == true){
            ArrayList<RoutePlanResultUnit> routePlanResultUnits = routePlanResults.getResults();
            travelAdvanceResult.setStatus(true);
            travelAdvanceResult.setMessage("Success");
            ArrayList<TravelAdvanceResultUnit> lists = new ArrayList<>();
            for(int i = 0; i < routePlanResultUnits.size(); i++){
                RoutePlanResultUnit tempUnit = routePlanResultUnits.get(i);
                TravelAdvanceResultUnit newUnit = new TravelAdvanceResultUnit();
                newUnit.setTripId(tempUnit.getTripId());
                newUnit.setTrainTypeId(tempUnit.getTrainTypeId());
                newUnit.setFromStationName(tempUnit.getFromStationName());
                newUnit.setToStationName(tempUnit.getToStationName());

                ArrayList<String> stops = transferStationIdToStationName(tempUnit.getStopStations(),headers);
                newUnit.setStopStations(stops);

                newUnit.setPriceForFirstClassSeat(tempUnit.getPriceForFirstClassSeat());
                newUnit.setPriceForSecondClassSeat(tempUnit.getPriceForSecondClassSeat());
                newUnit.setStartingTime(tempUnit.getStartingTime());
                newUnit.setEndTime(tempUnit.getEndTime());
                int first = getRestTicketNumber(info.getDepartureTime(),tempUnit.getTripId(),
                        tempUnit.getFromStationName(),tempUnit.getToStationName(),SeatClass.FIRSTCLASS.getCode(),headers);

                int second = getRestTicketNumber(info.getDepartureTime(),tempUnit.getTripId(),
                        tempUnit.getFromStationName(),tempUnit.getToStationName(),SeatClass.SECONDCLASS.getCode(),headers);
                newUnit.setNumberOfRestTicketFirstClass(first);
                newUnit.setNumberOfRestTicketSecondClass(second);
                lists.add(newUnit);
            }
            travelAdvanceResult.setTravelAdvanceResultUnits(lists);
        }else{
            travelAdvanceResult.setStatus(false);
            travelAdvanceResult.setMessage("Cannot Find");
            travelAdvanceResult.setTravelAdvanceResultUnits(new ArrayList<>());
        }

        return travelAdvanceResult;
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
//                );

        return restNumber;
    }

    private RoutePlanResults getRoutePlanResultCheapest(GetRoutePlanInfo info, HttpHeaders headers){
        HttpEntity requestEntity = new HttpEntity(info,headers);
        ResponseEntity<RoutePlanResults> re = restTemplate.exchange(
                "http://ts-route-plan-service:14578/routePlan/cheapestRoute",
                HttpMethod.POST,
                requestEntity,
                RoutePlanResults.class);
        RoutePlanResults routePlanResults = re.getBody();
//        RoutePlanResults routePlanResults =
//                restTemplate.postForObject(
//                        "http://ts-route-plan-service:14578/routePlan/cheapestRoute",
//                        info,RoutePlanResults.class
//                );
        return routePlanResults;
    }

    private RoutePlanResults getRoutePlanResultQuickest(GetRoutePlanInfo info, HttpHeaders headers){
        HttpEntity requestEntity = new HttpEntity(info,headers);
        ResponseEntity<RoutePlanResults> re = restTemplate.exchange(
                "http://ts-route-plan-service:14578/routePlan/quickestRoute",
                HttpMethod.POST,
                requestEntity,
                RoutePlanResults.class);
        RoutePlanResults routePlanResults = re.getBody();
//        RoutePlanResults routePlanResults =
//                restTemplate.postForObject(
//                        "http://ts-route-plan-service:14578/routePlan/quickestRoute",
//                        info,RoutePlanResults.class
//                );
        return routePlanResults;
    }

    private RoutePlanResults getRoutePlanResultMinStation(GetRoutePlanInfo info, HttpHeaders headers){
        HttpEntity requestEntity = new HttpEntity(info,headers);
        ResponseEntity<RoutePlanResults> re = restTemplate.exchange(
                "http://ts-route-plan-service:14578/routePlan/minStopStations",
                HttpMethod.POST,
                requestEntity,
                RoutePlanResults.class);
        RoutePlanResults routePlanResults = re.getBody();
//        RoutePlanResults routePlanResults =
//                restTemplate.postForObject(
//                        "http://ts-route-plan-service:14578/routePlan/minStopStations",
//                        info,RoutePlanResults.class
//                );
        return routePlanResults;
    }

    private ArrayList<TripResponse> tripsFromHighSpeed(QueryInfo info, HttpHeaders headers){
        ArrayList<TripResponse> result = new ArrayList<>();
        Class c = result.getClass();
        HttpEntity requestEntity = new HttpEntity(info,headers);
        ResponseEntity<ArrayList<TripResponse>> re = restTemplate.exchange(
                "http://ts-travel-service:12346/travel/query",
                HttpMethod.POST,
                requestEntity,
                c);
        result = re.getBody();
//        result = restTemplate.postForObject("http://ts-travel-service:12346/travel/query",info,result.getClass());
        return result;
    }

    private ArrayList<TripResponse> tripsFromNormal(QueryInfo info, HttpHeaders headers){
        ArrayList<TripResponse> result = new ArrayList<>();
        Class c = result.getClass();
        HttpEntity requestEntity = new HttpEntity(info,headers);
        ResponseEntity<ArrayList<TripResponse>> re = restTemplate.exchange(
                "http://ts-travel2-service:16346/travel2/query",
                HttpMethod.POST,
                requestEntity,
                c);
        result = re.getBody();
//        result = restTemplate.postForObject("http://ts-travel2-service:16346/travel2/query",info,result.getClass());
        return result;
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

    private ArrayList<String> transferStationIdToStationName(ArrayList<String> stations, HttpHeaders headers){
        ArrayList<String> stationNames = new ArrayList<>();
        for(int i = 0;i < stations.size();i++){
            String name = queryForStaionNameByStationId(stations.get(i),headers);
            stationNames.add(name);
        }
        return stationNames;
    }

    private String queryForStaionNameByStationId(String stationId, HttpHeaders headers) {

        QueryByStationIdForName queryByStationIdForName = new QueryByStationIdForName(stationId);
        HttpEntity requestEntity = new HttpEntity(queryByStationIdForName,headers);
        ResponseEntity<String> re = restTemplate.exchange(
                "http://ts-station-service:12345/station/queryByIdForName",
                HttpMethod.POST,
                requestEntity,
                String.class);
        return re.getBody();
//        return restTemplate.postForObject(
//                "http://ts-station-service:12345/station/queryByIdForName",
//                queryByStationIdForName,String.class
//        );
    }

}
