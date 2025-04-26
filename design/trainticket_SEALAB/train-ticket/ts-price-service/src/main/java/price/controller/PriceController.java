package price.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.*;
import price.domain.CreateAndModifyPriceConfig;
import price.domain.QueryPriceConfigByTrainAndRoute;
import price.domain.ReturnManyPriceConfigResult;
import price.domain.ReturnSinglePriceConfigResult;
import price.service.PriceService;

@RestController
public class PriceController {

    @Autowired
    PriceService service;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home() {
        return "Welcome to [ Price Service ] !";
    }

    @RequestMapping(value="/price/query", method= RequestMethod.POST)
    public ReturnSinglePriceConfigResult query(@RequestBody QueryPriceConfigByTrainAndRoute info,
                                               @RequestHeader HttpHeaders headers){
        return service.findByRouteIdAndTrainType(info.getRouteId(),info.getTrainType(), headers);
    }

    @RequestMapping(value="/price/queryAll", method= RequestMethod.GET)
    public ReturnManyPriceConfigResult queryAll(@RequestHeader HttpHeaders headers){
        return service.findAllPriceConfig(headers);
    }

    @RequestMapping(value="/price/create", method= RequestMethod.POST)
    public ReturnSinglePriceConfigResult create(@RequestBody CreateAndModifyPriceConfig info,
                                                @RequestHeader HttpHeaders headers){
        return service.createNewPriceConfig(info, headers);
    }

    @RequestMapping(value="/price/delete", method= RequestMethod.POST)
    public boolean delete(@RequestBody CreateAndModifyPriceConfig info, @RequestHeader HttpHeaders headers){
        return service.deletePriceConfig(info, headers);
    }

    @RequestMapping(value="/price/update", method= RequestMethod.POST)
    public boolean update(@RequestBody CreateAndModifyPriceConfig info, @RequestHeader HttpHeaders headers){
        return service.updatePriceConfig(info, headers);
    }


}
