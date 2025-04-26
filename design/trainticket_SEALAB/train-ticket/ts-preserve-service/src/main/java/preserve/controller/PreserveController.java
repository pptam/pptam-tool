package preserve.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.*;
import preserve.domain.*;
import preserve.service.PreserveService;

@RestController
public class PreserveController {

    @Autowired
    private PreserveService preserveService;

    @RequestMapping(path = "/welcome", method = RequestMethod.GET)
    public String home() {
        return "Welcome to [ Preserve Service ] !";
    }

    @CrossOrigin(origins = "*")
    @RequestMapping(value="/preserve", method = RequestMethod.POST)
    public OrderTicketsResult preserve(@RequestBody OrderTicketsInfo oti,@CookieValue String loginId,
                                       @CookieValue String loginToken, @RequestHeader HttpHeaders headers){
        System.out.println("[Preserve Service][Preserve] Account " + loginId + " order from " +
            oti.getFrom() + " -----> " + oti.getTo() + " at " + oti.getDate());
        return preserveService.preserve(oti,loginId,loginToken, headers);
    }

}
