package train.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.*;
import train.domain.Information;
import train.domain.Information2;
import train.domain.TrainType;
import train.service.TrainService;

import java.util.List;



@RestController
public class TrainController {

    //private static final Logger log = LoggerFactory.getLogger(Application.class);

    @Autowired
    private TrainService trainService;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home(@RequestHeader HttpHeaders headers) {
        return "Welcome to [ Train Service ] !";
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(value="/train/create",method= RequestMethod.POST)
    public boolean create(@RequestBody Information info,@RequestHeader HttpHeaders headers){
        return trainService.create(info,headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(value="/train/retrieve",method= RequestMethod.POST)
    public TrainType retrieve(@RequestBody Information2 info,@RequestHeader HttpHeaders headers){
        return trainService.retrieve(info,headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(value="/train/update",method= RequestMethod.POST)
    public boolean update(@RequestBody Information info,@RequestHeader HttpHeaders headers){
        return trainService.update(info,headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(value="/train/delete",method= RequestMethod.POST)
    public boolean delete(@RequestBody Information2 info,@RequestHeader HttpHeaders headers){
        return trainService.delete(info,headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(value="/train/query",method= RequestMethod.GET)
    public List<TrainType> query(@RequestHeader HttpHeaders headers){
        return trainService.query(headers);
    }
}
