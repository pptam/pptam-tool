package consignprice.controller;

import consignprice.domain.GetPriceDomain;
import consignprice.domain.PriceConfig;
import consignprice.service.ConsignPriceService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.*;

@RestController
public class ConsignPriceController {

    @Autowired
    ConsignPriceService service;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home(@RequestHeader HttpHeaders headers){
        return "Welcome to [ ConsignPrice Service ] !";
    }

    @RequestMapping(value = "/consignPrice/getPrice", method= RequestMethod.POST)
    public double getPriceByWeightAndRegion(@RequestBody GetPriceDomain info, @RequestHeader HttpHeaders headers){
        return service.getPriceByWeightAndRegion(info, headers);
    }

    @RequestMapping(value = "/consignPrice/getPriceInfo", method= RequestMethod.GET)
    public String getPriceInfo(@RequestHeader HttpHeaders headers){
        return service.queryPriceInformation(headers);
    }

    @RequestMapping(value = "/consignPrice/getPriceConfig", method= RequestMethod.GET)
    public PriceConfig getPriceConfig(@RequestHeader HttpHeaders headers){
        return service.getPriceConfig(headers);
    }

    @RequestMapping(value = "/consignPrice/modifyPriceConfig", method= RequestMethod.POST)
    public boolean modifyPriceConfig(@RequestBody PriceConfig priceConfig, @RequestHeader HttpHeaders headers){
        return service.createAndModifyPrice(priceConfig, headers);
    }
}
