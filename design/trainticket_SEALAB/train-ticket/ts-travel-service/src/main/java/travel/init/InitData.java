package travel.init;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import travel.domain.Information;
import travel.service.TravelService;

import java.util.Date;


@Component
public class InitData implements CommandLineRunner{

    @Autowired
    TravelService service;

    public void run(String... args)throws Exception{
        Information info = new Information();

        info.setTripId("G1234");
        info.setTrainTypeId("GaoTieOne");
        info.setRouteId("92708982-77af-4318-be25-57ccb0ff69ad");
        info.setStartingStationId("shanghai");
        info.setStationsId("suzhou");
        info.setTerminalStationId("taiyuan");
        info.setStartingTime(new Date("Mon May 04 09:00:00 GMT+0800 2013"));
        info.setEndTime(new Date("Mon May 04 15:51:52 GMT+0800 2013"));
        service.create(info,null);

        info.setTripId("G1235");
        info.setTrainTypeId("GaoTieOne");
        info.setRouteId("aefcef3f-3f42-46e8-afd7-6cb2a928bd3d");
        info.setStartingStationId("shanghai");
        info.setStationsId("suzhou");
        info.setTerminalStationId("taiyuan");
        info.setStartingTime(new Date("Mon May 04 12:00:00 GMT+0800 2013"));
        info.setEndTime(new Date("Mon May 04 17:51:52 GMT+0800 2013"));
        service.create(info,null);

        info.setTripId("G1236");
        info.setTrainTypeId("GaoTieOne");
        info.setRouteId("a3f256c1-0e43-4f7d-9c21-121bf258101f");
        info.setStartingStationId("shanghai");
        info.setStationsId("suzhou");
        info.setTerminalStationId("taiyuan");
        info.setStartingTime(new Date("Mon May 04 14:00:00 GMT+0800 2013"));
        info.setEndTime(new Date("Mon May 04 20:51:52 GMT+0800 2013"));
        service.create(info,null);

        info.setTripId("G1237");
        info.setTrainTypeId("GaoTieTwo");
        info.setRouteId("084837bb-53c8-4438-87c8-0321a4d09917");
        info.setStartingStationId("shanghai");
        info.setStationsId("suzhou");
        info.setTerminalStationId("taiyuan");
        info.setStartingTime(new Date("Mon May 04 08:00:00 GMT+0800 2013"));
        info.setEndTime(new Date("Mon May 04 17:21:52 GMT+0800 2013"));
        service.create(info,null);

        info.setTripId("D1345");
        info.setTrainTypeId("DongCheOne");
        info.setRouteId("f3d4d4ef-693b-4456-8eed-59c0d717dd08");
        info.setStartingStationId("shanghai");
        info.setStationsId("suzhou");
        info.setTerminalStationId("taiyuan");
        info.setStartingTime(new Date("Mon May 04 07:00:00 GMT+0800 2013"));
        info.setEndTime(new Date("Mon May 04 19:59:52 GMT+0800 2013"));
        service.create(info,null);
    }
}
