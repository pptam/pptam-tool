package admintravel.service;

import admintravel.domain.request.AddAndModifyTravelRequest;
import admintravel.domain.request.DeleteTravelRequest;
import admintravel.domain.response.AdminFindAllResult;
import admintravel.domain.response.ResponseBean;
import org.springframework.http.HttpHeaders;

public interface AdminTravelService {
    AdminFindAllResult getAllTravels(String id, HttpHeaders headers);
    ResponseBean addTravel(AddAndModifyTravelRequest request, HttpHeaders headers);
    ResponseBean updateTravel(AddAndModifyTravelRequest request, HttpHeaders headers);
    ResponseBean deleteTravel(DeleteTravelRequest request, HttpHeaders headers);
}
