package consign.controller;

import consign.domain.ConsignRecord;
import consign.domain.ConsignRequest;
import consign.domain.InsertConsignRecordResult;
import consign.service.ConsignService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
public class ConsignController {
    @Autowired
    ConsignService service;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home(@RequestHeader HttpHeaders headers){
        return "Welcome to [ Consign Service ] !";
    }

    @RequestMapping(value = "/consign/insertConsign", method= RequestMethod.POST)
    public InsertConsignRecordResult insertConsign(@RequestBody ConsignRequest request, @RequestHeader HttpHeaders headers){
        return service.insertConsignRecord(request, headers);
    }

    @RequestMapping(value = "/consign/updateConsign", method= RequestMethod.POST)
    public boolean updateConsign(@RequestBody ConsignRequest request, @RequestHeader HttpHeaders headers){
        return service.updateConsignRecord(request, headers);
    }

    @RequestMapping(value = "/consign/findByAccountId/{id}", method= RequestMethod.GET)
    public List<ConsignRecord> findByAccountId(@PathVariable String id, @RequestHeader HttpHeaders headers){
        UUID newid = UUID.fromString(id);
        return service.queryByAccountId(newid, headers);
    }

    @RequestMapping(value = "/consign/findByConsignee", method= RequestMethod.POST)
    public List<ConsignRecord> findByConsignee(@RequestParam(value = "consignee", required = true) String consignee, @RequestHeader HttpHeaders headers){
        return service.queryByConsignee(consignee, headers);
    }
}
