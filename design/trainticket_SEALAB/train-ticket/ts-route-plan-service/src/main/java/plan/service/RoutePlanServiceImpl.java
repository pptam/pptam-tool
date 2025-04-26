package plan.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import plan.domain.*;
import java.util.ArrayList;

@Service
public class RoutePlanServiceImpl implements RoutePlanService{

    @Autowired
    private RestTemplate restTemplate;

    @Override
    public RoutePlanResults searchCheapestResult(GetRoutePlanInfo info,HttpHeaders headers) {

        //1.暴力取出travel-service和travle2-service的所有结果
        QueryInfo queryInfo = new QueryInfo();
        queryInfo.setStartingPlace(info.getFormStationName());
        queryInfo.setEndPlace(info.getToStationName());
        queryInfo.setDepartureTime(info.getTravelDate());

        ArrayList<TripResponse> highSpeed = getTripFromHighSpeedTravelServive(queryInfo,headers);
        ArrayList<TripResponse> normalTrain = getTripFromNormalTrainTravelService(queryInfo,headers);

        //2.按照二等座位结果排序
        ArrayList<TripResponse> finalResult = new ArrayList<>();
        finalResult.addAll(highSpeed);
        finalResult.addAll(normalTrain);

        float minPrice;
        int minIndex = -1;
        int size = Math.min(5,finalResult.size());
        ArrayList<TripResponse> returnResult = new ArrayList<>();
        for(int i = 0;i < size;i++){

            minPrice = Float.MAX_VALUE;
            for(int j = 0;j < finalResult.size();j++){
                TripResponse thisRes = finalResult.get(j);
                if(Float.parseFloat(thisRes.getPriceForEconomyClass()) < minPrice){
                    minPrice = Float.parseFloat(finalResult.get(j).getPriceForEconomyClass());
                    minIndex = j;
                }
            }
            returnResult.add(finalResult.get(minIndex));
            finalResult.remove(minIndex);
        }

        RoutePlanResults result = new RoutePlanResults();
        result.setStatus(true);
        result.setMessage("Success.");
        ArrayList<RoutePlanResultUnit> units = new ArrayList<>();
        for(int i = 0;i < returnResult.size();i++){
            TripResponse tempResponse = returnResult.get(i);

            RoutePlanResultUnit tempUnit = new RoutePlanResultUnit();
            tempUnit.setTripId(tempResponse.getTripId().toString());
            tempUnit.setTrainTypeId(tempResponse.getTrainTypeId());
            tempUnit.setFromStationName(tempResponse.getStartingStation());
            tempUnit.setToStationName(tempResponse.getTerminalStation());

            tempUnit.setStopStations(getStationList(tempResponse.getTripId().toString(),headers));

            tempUnit.setPriceForSecondClassSeat(tempResponse.getPriceForEconomyClass());
            tempUnit.setPriceForFirstClassSeat(tempResponse.getPriceForConfortClass());
            tempUnit.setStartingTime(tempResponse.getStartingTime());
            tempUnit.setEndTime(tempResponse.getEndTime());
            units.add(tempUnit);
        }
        result.setResults(units);

        return result;
    }

    @Override
    public RoutePlanResults searchQuickestResult(GetRoutePlanInfo info,HttpHeaders headers) {

        //1.暴力取出travel-service和travel2-service的所有结果
        QueryInfo queryInfo = new QueryInfo();
        queryInfo.setStartingPlace(info.getFormStationName());
        queryInfo.setEndPlace(info.getToStationName());
        queryInfo.setDepartureTime(info.getTravelDate());

        ArrayList<TripResponse> highSpeed = getTripFromHighSpeedTravelServive(queryInfo,headers);
        ArrayList<TripResponse> normalTrain = getTripFromNormalTrainTravelService(queryInfo,headers);

        //2.按照时间排序
        ArrayList<TripResponse> finalResult = new ArrayList<>();
//        finalResult.addAll(highSpeed);
//        finalResult.addAll(normalTrain);
//        return finalResult;
        for(TripResponse tr : highSpeed){
            finalResult.add(tr);
        }
        for(TripResponse tr : normalTrain){
            finalResult.add(tr);
        }

        long minTime;
        int minIndex = -1;
        int size = Math.min(finalResult.size(),5);
        ArrayList<TripResponse> returnResult = new ArrayList<>();
        for(int i = 0;i < size;i++){

            minTime = Long.MAX_VALUE;
            for(int j = 0;j < finalResult.size();j++){
                TripResponse thisRes = finalResult.get(j);
                if(thisRes.getEndTime().getTime() - thisRes.getStartingTime().getTime() < minTime){
                    minTime = thisRes.getEndTime().getTime() - thisRes.getStartingTime().getTime();
                    minIndex = j;
                }
            }
            returnResult.add(finalResult.get(minIndex));
            finalResult.remove(minIndex);

        }

        RoutePlanResults result = new RoutePlanResults();
        result.setStatus(true);
        result.setMessage("Success.");
        ArrayList<RoutePlanResultUnit> units = new ArrayList<>();
        for(int i = 0;i < returnResult.size();i++){
            TripResponse tempResponse = returnResult.get(i);

            RoutePlanResultUnit tempUnit = new RoutePlanResultUnit();
            tempUnit.setTripId(tempResponse.getTripId().toString());
            tempUnit.setTrainTypeId(tempResponse.getTrainTypeId());
            tempUnit.setFromStationName(tempResponse.getStartingStation());
            tempUnit.setToStationName(tempResponse.getTerminalStation());

            tempUnit.setStopStations(getStationList(tempResponse.getTripId().toString(),headers));

            tempUnit.setPriceForSecondClassSeat(tempResponse.getPriceForEconomyClass());
            tempUnit.setPriceForFirstClassSeat(tempResponse.getPriceForConfortClass());
            tempUnit.setStartingTime(tempResponse.getStartingTime());
            tempUnit.setEndTime(tempResponse.getEndTime());
            units.add(tempUnit);
        }
        result.setResults(units);

        return result;
    }

    @Override
    public RoutePlanResults searchMinStopStations(GetRoutePlanInfo info,HttpHeaders headers) {
        String fromStationId = queryForStationId(info.getFormStationName(),headers);
        String toStationId = queryForStationId(info.getToStationName(),headers);
        System.out.println("From Id:" + fromStationId + " To:" + toStationId);
        //1.获取这个经过这两个车站的路线
        GetRouteByStartAndTerminalInfo searchRouteInfo =
                new GetRouteByStartAndTerminalInfo(fromStationId,toStationId);
        HttpEntity requestEntity = new HttpEntity(searchRouteInfo,headers);
        ResponseEntity<GetRoutesListlResult> re = restTemplate.exchange(
                "http://ts-route-service:11178/route/queryByStartAndTerminal",
                HttpMethod.POST,
                requestEntity,
                GetRoutesListlResult.class);
        GetRoutesListlResult routeResult = re.getBody();

//        GetRoutesListlResult routeResult = restTemplate.postForObject(
//                "http://ts-route-service:11178/route/queryByStartAndTerminal",
//                searchRouteInfo, GetRoutesListlResult.class);
        ArrayList<Route> routeList = routeResult.getRoutes();
        System.out.println("[Route Plan Service] Candidate Route Number:" + routeList.size());
        //2.计算这两个车站之间有多少停靠站
        ArrayList<Integer> gapList = new ArrayList<>();
        for(int i = 0; i < routeList.size(); i++){
            int indexStart = routeList.get(i).getStations().indexOf(fromStationId);
            int indexEnd = routeList.get(i).getStations().indexOf(toStationId);
            gapList.add(indexEnd - indexStart);
        }
        //3.挑选出最少停靠站的几条路线
        ArrayList<String> resultRoutes = new ArrayList<>();
        for(int i = 0; i < Math.min(info.getNum(),routeList.size()); i++){
            int minIndex = 0;
            int tempMinGap = Integer.MAX_VALUE;
            for(int j = 0; j < gapList.size(); j++){
                if(gapList.get(j) < tempMinGap){
                    tempMinGap = gapList.get(j);
                    minIndex = j;
                }
            }
            resultRoutes.add(routeList.get(minIndex).getId());
            routeList.remove(minIndex);
        }
        //4.根据路线，去travel或者travel2获取这些车次信息
        GetTripsByRouteIdInfo getTripInfo = new GetTripsByRouteIdInfo();
        getTripInfo.setRouteIds(resultRoutes);
        requestEntity = new HttpEntity(getTripInfo,headers);
        ResponseEntity<GetTripsByRouteIdResult> re2 = restTemplate.exchange(
                "http://ts-travel-service:12346/travel/getTripsByRouteId",
                HttpMethod.POST,
                requestEntity,
                GetTripsByRouteIdResult.class);
        GetTripsByRouteIdResult resultTravel = re2.getBody();

//        GetTripsByRouteIdResult resultTravel = restTemplate.postForObject(
//                "http://ts-travel-service:12346/travel/getTripsByRouteId",
//                getTripInfo,GetTripsByRouteIdResult.class
//        );

        re2 = restTemplate.exchange(
                "http://ts-travel2-service:16346/travel2/getTripsByRouteId",
                HttpMethod.POST,
                requestEntity,
                GetTripsByRouteIdResult.class);
        GetTripsByRouteIdResult resultTravel2 = re2.getBody();

//        GetTripsByRouteIdResult resultTravel2 = restTemplate.postForObject(
//                "http://ts-travel2-service:16346/travel2/getTripsByRouteId",
//                getTripInfo,GetTripsByRouteIdResult.class);
            //合并查询结果
        ArrayList<ArrayList<Trip>> finalTripResult = new ArrayList<>();
        ArrayList<ArrayList<Trip>> travelTrips = resultTravel.getTripsSet();
        ArrayList<ArrayList<Trip>> travel2Trips = resultTravel2.getTripsSet();
        for(int i = 0;i < travel2Trips.size();i++){
            ArrayList<Trip> tempList = travel2Trips.get(i);
            tempList.addAll(travelTrips.get(i));
            finalTripResult.add(tempList);
        }
        System.out.println("[Route Plan Service] Trips Num:" + finalTripResult.size());
        //5.再根据这些车次信息获取其价格和停靠站信息
        ArrayList<Trip> trips = new ArrayList<>();
        for(ArrayList<Trip> tempTrips : finalTripResult){
            trips.addAll(tempTrips);
        }
        ArrayList<RoutePlanResultUnit> tripResponses = new ArrayList<>();

        ResponseEntity<GetTripAllDetailResult> re3;
        for(Trip trip : trips){
            TripResponse tripResponse;
            if(trip.getTripId().toString().charAt(0) == 'D' || trip.getTripId().toString().charAt(0) == 'G'){
                GetTripAllDetailInfo allDetailInfo = new GetTripAllDetailInfo();
                allDetailInfo.setTripId(trip.getTripId().toString());
                allDetailInfo.setTravelDate(info.getTravelDate());
                allDetailInfo.setFrom(info.getFormStationName());
                allDetailInfo.setTo(info.getToStationName());
                requestEntity = new HttpEntity(allDetailInfo,headers);
                re3 = restTemplate.exchange(
                        "http://ts-travel-service:12346//travel/getTripAllDetailInfo",
                        HttpMethod.POST,
                        requestEntity,
                        GetTripAllDetailResult.class);
                GetTripAllDetailResult tripDetailResult = re3.getBody();
//                GetTripAllDetailResult tripDetailResult = restTemplate.postForObject(
//                        "http://ts-travel-service:12346//travel/getTripAllDetailInfo",
//                        allDetailInfo,GetTripAllDetailResult.class);
                tripResponse = tripDetailResult.getTripResponse();
            }else{
                GetTripAllDetailInfo allDetailInfo = new GetTripAllDetailInfo();
                allDetailInfo.setTripId(trip.getTripId().toString());
                allDetailInfo.setTravelDate(info.getTravelDate());
                allDetailInfo.setFrom(info.getFormStationName());
                allDetailInfo.setTo(info.getToStationName());
                requestEntity = new HttpEntity(allDetailInfo,headers);
                re3 = restTemplate.exchange(
                        "http://ts-travel2-service:16346//travel2/getTripAllDetailInfo",
                        HttpMethod.POST,
                        requestEntity,
                        GetTripAllDetailResult.class);
                GetTripAllDetailResult tripDetailResult = re3.getBody();
//                GetTripAllDetailResult tripDetailResult = restTemplate.postForObject(
//                        "http://ts-travel2-service:16346//travel2/getTripAllDetailInfo",
//                        allDetailInfo,GetTripAllDetailResult.class);
                tripResponse = tripDetailResult.getTripResponse();
            }
            RoutePlanResultUnit unit = new RoutePlanResultUnit();
            unit.setTripId(trip.getTripId().toString());
            unit.setTrainTypeId(tripResponse.getTrainTypeId());
            unit.setFromStationName(tripResponse.getStartingStation());
            unit.setToStationName(tripResponse.getTerminalStation());
            unit.setStartingTime(tripResponse.getStartingTime());
            unit.setEndTime(tripResponse.getEndTime());
            unit.setPriceForFirstClassSeat(tripResponse.getPriceForConfortClass());
            unit.setPriceForSecondClassSeat(tripResponse.getPriceForEconomyClass());
            //根据routeid去拿路线图
            String routeId = trip.getRouteId();
            Route tripRoute = getRouteByRouteId(routeId,headers);
            unit.setStopStations(tripRoute.getStations());

            tripResponses.add(unit);
        }

        System.out.println("[Route Plan Service] Trips Response Unit Num:" + tripResponses.size());
        RoutePlanResults finalResults = new RoutePlanResults();

        finalResults.setStatus(true);
        finalResults.setMessage("Success.");
        finalResults.setResults(tripResponses);
        
        return finalResults;
    }

    private String queryForStationId(String stationName, HttpHeaders headers){
        System.out.println("[Preserve Service][Get Station Name]");
        QueryForStationId queryForId = new QueryForStationId();
        queryForId.setName(stationName);

        HttpEntity requestEntity = new HttpEntity(queryForId,headers);
        ResponseEntity<String> re = restTemplate.exchange(
                "http://ts-station-service:12345/station/queryForId",
                HttpMethod.POST,
                requestEntity,
                String.class);
        String stationId = re.getBody();
//        String stationId = restTemplate.postForObject("http://ts-station-service:12345/station/queryForId",queryForId,String.class);
        return stationId;
    }

    private Route getRouteByRouteId(String routeId, HttpHeaders headers){
        System.out.println("[Route Plan Service][Get Route By Id] Route ID：" + routeId);
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

    private ArrayList<TripResponse> getTripFromHighSpeedTravelServive(QueryInfo info, HttpHeaders headers){
        HttpEntity requestEntity = new HttpEntity(info,headers);
        ResponseEntity<QueryTripResponsePackage> re = restTemplate.exchange(
                "http://ts-travel-service:12346/travel/queryWithPackage",
                HttpMethod.POST,
                requestEntity,
                QueryTripResponsePackage.class);
        QueryTripResponsePackage list = re.getBody();
//        QueryTripResponsePackage list = restTemplate.postForObject(
//                "http://ts-travel-service:12346/travel/queryWithPackage",
//                info,  QueryTripResponsePackage.class);

        System.out.println("[Route Plan Get Trip][Size]" + list.getResponses().size());

        return list.getResponses();
    }

    private ArrayList<TripResponse> getTripFromNormalTrainTravelService(QueryInfo info, HttpHeaders headers){
        HttpEntity requestEntity = new HttpEntity(info,headers);
        ResponseEntity<QueryTripResponsePackage> re = restTemplate.exchange(
                "http://ts-travel2-service:16346/travel2/queryWithPackage",
                HttpMethod.POST,
                requestEntity,
                QueryTripResponsePackage.class);
        QueryTripResponsePackage list = re.getBody();
//        QueryTripResponsePackage list = restTemplate.postForObject(
//                "http://ts-travel2-service:16346/travel2/queryWithPackage",
//                info,  QueryTripResponsePackage.class);

        System.out.println("[Route Plan Get TripOther][Size]" + list.getResponses().size());

        return list.getResponses();
    }

    private ArrayList<String> getStationList(String tripId, HttpHeaders headers){
        //首先获取

        String path;
        if(tripId.charAt(0) == 'G' || tripId.charAt(0) == 'D'){
            path = "http://ts-travel-service:12346/travel/getRouteByTripId/" + tripId;
        }else{
            path = "http://ts-travel2-service:16346/travel2/getRouteByTripId/" + tripId;
        }

        HttpEntity requestEntity = new HttpEntity(headers);
        ResponseEntity<GetRouteResult> re = restTemplate.exchange(
                path,
                HttpMethod.GET,
                requestEntity,
                GetRouteResult.class);
        GetRouteResult route = re.getBody();
//        GetRouteResult route = restTemplate.getForObject(
//                path,
//                GetRouteResult.class
//        );

        return route.getRoute().getStations();
    }
}
