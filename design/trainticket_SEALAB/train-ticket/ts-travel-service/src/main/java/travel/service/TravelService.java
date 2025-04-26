package travel.service;

import org.springframework.http.HttpHeaders;
import org.springframework.integration.dsl.http.Http;
import travel.domain.*;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by Chenjie Xu on 2017/5/9.
 */
public interface TravelService {

    String create(Information info, HttpHeaders headers);

    Trip retrieve(Information2 info, HttpHeaders headers);

    String update(Information info, HttpHeaders headers);

    String delete(Information2 info, HttpHeaders headers);

    ArrayList<TripResponse> query(QueryInfo info, HttpHeaders headers);

    GetTripAllDetailResult getTripAllDetailInfo(GetTripAllDetailInfo gtdi, HttpHeaders headers);

    GetRouteResult getRouteByTripId(String tripId, HttpHeaders headers);

    GetTrainTypeResult getTrainTypeByTripId(String tripId, HttpHeaders headers);

    List<Trip> queryAll(HttpHeaders headers);

    GetTripsByRouteIdResult getTripByRoute(GetTripsByRouteIdInfo info, HttpHeaders headers);

    AdminFindAllResult adminQueryAll(HttpHeaders headers);
}
