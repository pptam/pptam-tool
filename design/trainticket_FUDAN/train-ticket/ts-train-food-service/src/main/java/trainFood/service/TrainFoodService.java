package trainFood.service;

import edu.fudan.common.util.Response;
import org.springframework.http.HttpHeaders;
import trainFood.entity.*;

public interface TrainFoodService {
    TrainFood createTrainFood(TrainFood tf, HttpHeaders headers);

    Response listTrainFood(HttpHeaders headers);

    Response listTrainFoodByTripId(String tripId, HttpHeaders headers);
}
