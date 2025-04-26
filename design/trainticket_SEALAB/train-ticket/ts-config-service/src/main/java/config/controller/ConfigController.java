package config.controller;

/**
 * Created by Chenjie Xu on 2017/5/11.
 */

import config.domain.Config;
import config.domain.Information;
import config.domain.Information2;
import config.service.ConfigService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class ConfigController {
    @Autowired
    private ConfigService configService;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home(@RequestHeader HttpHeaders headers){
        return "Welcome to [ Config Service ] !";
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(value="/config/create", method = RequestMethod.POST)
    public String delete(@RequestBody Information info, @RequestHeader HttpHeaders headers){
        return configService.create(info, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(value="/config/update", method = RequestMethod.POST)
    public String update(@RequestBody Information info, @RequestHeader HttpHeaders headers){
        return configService.update(info, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(value="/config/retrieve", method = RequestMethod.POST)
    public Config retrieve(@RequestBody Information2 info, @RequestHeader HttpHeaders headers){
        return configService.retrieve(info, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(value="/config/query", method = RequestMethod.POST)
    public String query(@RequestBody Information2 info, @RequestHeader HttpHeaders headers){
        return configService.query(info, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(value="/config/delete", method = RequestMethod.POST)
    public String delete(@RequestBody Information2 info, @RequestHeader HttpHeaders headers){
        return configService.delete(info, headers);
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(value="/config/queryAll", method = RequestMethod.GET)
    public List<Config> queryAll(@RequestHeader HttpHeaders headers){
        return configService.queryAll(headers);
    }
}
