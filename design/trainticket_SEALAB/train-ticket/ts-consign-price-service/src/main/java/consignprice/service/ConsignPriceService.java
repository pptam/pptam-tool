package consignprice.service;

import consignprice.domain.GetPriceDomain;
import consignprice.domain.PriceConfig;
import org.springframework.http.HttpHeaders;

public interface ConsignPriceService {
    double getPriceByWeightAndRegion(GetPriceDomain domain, HttpHeaders headers);
    String queryPriceInformation(HttpHeaders headers);
    boolean createAndModifyPrice(PriceConfig config, HttpHeaders headers);
    PriceConfig getPriceConfig(HttpHeaders headers);
}
