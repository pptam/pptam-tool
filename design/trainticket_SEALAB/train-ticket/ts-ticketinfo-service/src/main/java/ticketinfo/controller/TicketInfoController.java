package ticketinfo.controller;

/**
 * Created by Chenjie Xu on 2017/6/6.
 */

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.*;
import ticketinfo.domain.QueryForStationId;
import ticketinfo.domain.QueryForTravel;
import ticketinfo.domain.ResultForTravel;
import ticketinfo.service.TicketInfoService;

@RestController
public class TicketInfoController {

    @Autowired
    TicketInfoService service;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home() {
        return "Welcome to [ TicketInfo Service ] !";
    }

    @RequestMapping(value="/ticketinfo/queryForTravel", method = RequestMethod.POST)
    public ResultForTravel queryForTravel(@RequestBody QueryForTravel info,@RequestHeader HttpHeaders headers){
        return service.queryForTravel(info,headers);
    }

    @RequestMapping(value="/ticketinfo/queryForStationId", method = RequestMethod.POST)
    public String queryForStationId(@RequestBody QueryForStationId info,@RequestHeader HttpHeaders headers){
        return service.queryForStationId(info,headers);
    }
}
