package fdse.microservice.controller;

import fdse.microservice.domain.QueryForStationId;
import fdse.microservice.domain.QueryForTravel;
import fdse.microservice.domain.QueryStation;
import fdse.microservice.domain.ResultForTravel;
import fdse.microservice.service.BasicService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.*;

/**
 * Created by Chenjie Xu on 2017/6/6.
 */
@RestController
public class BasicController {

    @Autowired
    BasicService service;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home(@RequestHeader HttpHeaders headers){
        return "Welcome to [ Basic Service ] !";
    }

    @RequestMapping(value="/basic/queryForTravel", method= RequestMethod.POST)
    public ResultForTravel queryForTravel(@RequestBody QueryForTravel info, @RequestHeader HttpHeaders headers){
        return service.queryForTravel(info, headers);
    }

    @RequestMapping(value="/basic/queryForStationId", method= RequestMethod.POST)
    public String queryForStationId(@RequestBody QueryStation info, @RequestHeader HttpHeaders headers){
        return service.queryForStationId(info, headers);
    }
}
