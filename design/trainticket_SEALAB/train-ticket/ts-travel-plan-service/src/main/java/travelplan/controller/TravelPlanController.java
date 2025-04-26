package travelplan.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.*;
import travelplan.domain.QueryInfo;
import travelplan.domain.TransferTravelSearchInfo;
import travelplan.domain.TransferTravelSearchResult;
import travelplan.domain.TravelAdvanceResult;
import travelplan.service.TravelPlanService;

@RestController
public class TravelPlanController {

    @Autowired
    TravelPlanService travelPlanService;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home() {
        return "Welcome to [ TravelPlan Service ] !";
    }

    @RequestMapping(value="/travelPlan/getTransferResult", method= RequestMethod.POST)
    public TransferTravelSearchResult getTransferResult(@RequestBody TransferTravelSearchInfo info,@RequestHeader HttpHeaders headers) {
        System.out.println("[Search Transit]");
        return travelPlanService.getTransferSearch(info, headers);
    }

    @RequestMapping(value="/travelPlan/getCheapest", method= RequestMethod.POST)
    public TravelAdvanceResult getByCheapest(@RequestBody QueryInfo queryInfo,@RequestHeader HttpHeaders headers) {
        System.out.println("[Search Cheapest]");
        return travelPlanService.getCheapest(queryInfo, headers);
    }

    @RequestMapping(value="/travelPlan/getQuickest", method= RequestMethod.POST)
    public TravelAdvanceResult getByQuickest(@RequestBody QueryInfo queryInfo,@RequestHeader HttpHeaders headers) {
        System.out.println("[Search Quickest]");
        return travelPlanService.getQuickest(queryInfo, headers);
    }

    @RequestMapping(value="/travelPlan/getMinStation", method= RequestMethod.POST)
    public TravelAdvanceResult getByMinStation(@RequestBody QueryInfo queryInfo,@RequestHeader HttpHeaders headers) {
        System.out.println("[Search Min Station]");
        return travelPlanService.getMinStation(queryInfo, headers);
    }


}
