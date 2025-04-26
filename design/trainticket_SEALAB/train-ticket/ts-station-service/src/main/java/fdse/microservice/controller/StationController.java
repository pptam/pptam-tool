package fdse.microservice.controller;

import fdse.microservice.domain.*;
import fdse.microservice.service.StationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;


@RestController
public class StationController {

    //private static final Logger log = LoggerFactory.getLogger(Application.class);

    @Autowired
    private StationService stationService;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home(@RequestHeader HttpHeaders headers) {
        return "Welcome to [ Station Service ] !";
    }

    @RequestMapping(value="/station/create",method= RequestMethod.POST)
    public boolean create(@RequestBody Information info,@RequestHeader HttpHeaders headers){
        return stationService.create(info,headers);
    }

    @RequestMapping(value="/station/exist",method= RequestMethod.POST)
    public boolean exist(@RequestBody QueryStation info,@RequestHeader HttpHeaders headers){
        return stationService.exist(info,headers);
    }

    @RequestMapping(value="/station/update",method= RequestMethod.POST)
    public boolean update(@RequestBody Information info,@RequestHeader HttpHeaders headers){
        return stationService.update(info,headers);
    }

    @RequestMapping(value="/station/delete",method= RequestMethod.POST)
    public boolean delete(@RequestBody Information info,@RequestHeader HttpHeaders headers){
        return stationService.delete(info,headers);
    }

    @RequestMapping(value="/station/query",method= RequestMethod.GET)
    public List<Station> query(@RequestHeader HttpHeaders headers){
        return stationService.query(headers);
    }

    @RequestMapping(value="/station/queryForId",method= RequestMethod.POST)
    public String queryForId(@RequestBody QueryForId info, @RequestHeader HttpHeaders headers){
        return stationService.queryForId(info,headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(value="/station/queryForIdBatch", method = RequestMethod.POST)
    public ArrayList<String> queryForIdBatch(@RequestBody QueryForIdBatch queryForIdBatch, @RequestHeader HttpHeaders headers){
        return stationService.queryForIdBatch(queryForIdBatch, headers);
    }


    @CrossOrigin(origins = "*")
    @RequestMapping(value = "/station/queryById",method = RequestMethod.POST)
    public QueryStation queryById(@RequestBody QueryById queryById,@RequestHeader HttpHeaders headers){
        System.out.println("[Station Service] Query By Id:" + queryById.getStationId());
        return stationService.queryById(queryById.getStationId(),headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(value="/station/queryByIdBatch", method = RequestMethod.POST)
    public QueryByIdBatchResult queryByIdBatch(@RequestBody QueryByIdBatch queryByIdBatch, @RequestHeader HttpHeaders headers){
        QueryByIdBatchResult result = new QueryByIdBatchResult(stationService.queryByIdBatch(queryByIdBatch, headers));
        return result;
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(value = "/station/queryByIdForName",method = RequestMethod.POST)
    public String queryByIdForName(@RequestBody QueryById queryById,@RequestHeader HttpHeaders headers){
        System.out.println("[Station Service] Query By Id For Name:" + queryById.getStationId());
        return stationService.queryById(queryById.getStationId(),headers).getName();
    }
}
