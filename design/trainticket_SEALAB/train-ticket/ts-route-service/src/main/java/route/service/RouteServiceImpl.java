package route.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.stereotype.Service;
import route.domain.*;
import route.repository.RouteRepository;
import java.util.ArrayList;
import java.util.UUID;

@Service
public class RouteServiceImpl implements RouteService {

    @Autowired
    private RouteRepository routeRepository;

    @Override
    public CreateAndModifyRouteResult createAndModify(CreateAndModifyRouteInfo info, HttpHeaders headers){
        System.out.println("[Route Service] Create And Modify Start:" + info.getStartStation() + " End:" + info.getEndStation());
        CreateAndModifyRouteResult result;
        String[] stations = info.getStationList().split(",");
        String[] distances = info.getDistanceList().split(",");
        ArrayList<String> stationList = new ArrayList<>();
        ArrayList<Integer> distanceList = new ArrayList<>();
        if(stations.length != distances.length){
            result  = new CreateAndModifyRouteResult(
                    false,
                    "Station Number Not Equal To Distance Number",
                    null
            );
            return result;
        }
        for(int i = 0;i < stations.length;i++){
            stationList.add(stations[i]);
            distanceList.add(Integer.parseInt(distances[i]));
        }
        if(info.getId() == null || info.getId().length() < 10){
            Route route = new Route();
            route.setId(UUID.randomUUID().toString());
            route.setStartStationId(info.getStartStation());
            route.setTerminalStationId(info.getEndStation());
            route.setStations(stationList);
            route.setDistances(distanceList);
            routeRepository.save(route);
            result  = new CreateAndModifyRouteResult(
                    true,
                    "Success.",
                    route
            );
        }else{
            Route route = routeRepository.findById(info.getId());
            if(route == null){
                route = new Route();
                route.setId(info.getId());
            }

            route.setStartStationId(info.getStartStation());
            route.setTerminalStationId(info.getEndStation());
            route.setStations(stationList);
            route.setDistances(distanceList);
            routeRepository.save(route);
            result  = new CreateAndModifyRouteResult(
                    true,
                    "Success.",
                    route
            );
        }
        return result;
    }

    @Override
    public DeleteRouteResult deleteRoute(DeleteRouteInfo info,HttpHeaders headers){
        routeRepository.removeRouteById(info.getRouteId());
        DeleteRouteResult result = new DeleteRouteResult(true,"Success");
        return result;
    }

    @Override
    public GetRouteByIdResult getRouteById(String routeId,HttpHeaders headers){
        Route route = routeRepository.findById(routeId);
        GetRouteByIdResult result;
        if(route == null){
            result = new GetRouteByIdResult(false,"Route Not Exist",null);
        }else{
            result = new GetRouteByIdResult(true,"Success",route);
        }
        return result;
    }

    @Override
    public GetRoutesListlResult getRouteByStartAndTerminal(GetRouteByStartAndTerminalInfo info,HttpHeaders headers){
//        ArrayList<Route> routes = routeRepository.findByStartStationIdAndTerminalStationId(info.getStartId(),info.getTerminalId());
        ArrayList<Route> routes = routeRepository.findAll();
        System.out.println("[Route Service] Find All:" + routes.size());
        ArrayList<Route> resultList = new ArrayList<>();
        for(Route route : routes){
            if(route.getStations().contains(info.getStartId()) &&
                    route.getStations().contains(info.getTerminalId()) &&
                    route.getStations().indexOf(info.getStartId()) < route.getStations().indexOf(info.getTerminalId())) {
                resultList.add(route);
            }
       }
       GetRoutesListlResult result = new GetRoutesListlResult(
                true, "Success", resultList
       );
        return result;
    }

    @Override
    public GetRoutesListlResult getAllRoutes(HttpHeaders headers) {
        ArrayList<Route> routes = routeRepository.findAll();

        if(routes == null){
            routes = new ArrayList<>();
        }
        GetRoutesListlResult result = new GetRoutesListlResult(
                true, "Success", routes
        );
        return result;
    }

}
