package price.service;

        import org.springframework.http.HttpHeaders;
        import price.domain.CreateAndModifyPriceConfig;
        import price.domain.ReturnManyPriceConfigResult;
        import price.domain.ReturnSinglePriceConfigResult;

public interface PriceService {

    ReturnSinglePriceConfigResult createNewPriceConfig(CreateAndModifyPriceConfig createAndModifyPriceConfig, HttpHeaders headers);

    ReturnSinglePriceConfigResult findById(String id, HttpHeaders headers);

    ReturnSinglePriceConfigResult findByRouteIdAndTrainType(String routeId,String trainType, HttpHeaders headers);

    ReturnManyPriceConfigResult findAllPriceConfig(HttpHeaders headers);

    boolean deletePriceConfig(CreateAndModifyPriceConfig c, HttpHeaders headers);

    boolean updatePriceConfig(CreateAndModifyPriceConfig c, HttpHeaders headers);

}
