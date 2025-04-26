package travel2.init;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import travel2.domain.Information;
import travel2.service.Travel2Service;
import java.util.Date;


@Component
public class InitData implements CommandLineRunner {

    @Autowired
    Travel2Service service;

    public void run(String... args)throws Exception{
        Information info = new Information();

        info.setTripId("Z1234");
        info.setTrainTypeId("ZhiDa");
        info.setRouteId("0b23bd3e-876a-4af3-b920-c50a90c90b04");
        info.setStartingStationId("shanghai");
        info.setStationsId("nanjing");
        info.setTerminalStationId("beijing");
        info.setStartingTime(new Date("Mon May 04 09:51:52 GMT+0800 2013"));
        info.setEndTime(new Date("Mon May 04 15:51:52 GMT+0800 2013"));
        service.create(info,null);

        info.setTripId("Z1235");
        info.setTrainTypeId("ZhiDa");
        info.setRouteId("9fc9c261-3263-4bfa-82f8-bb44e06b2f52");
        info.setStartingStationId("shanghai");
        info.setStationsId("nanjing");
        info.setTerminalStationId("beijing");
        info.setStartingTime(new Date("Mon May 04 11:31:52 GMT+0800 2013"));
        info.setEndTime(new Date("Mon May 04 17:51:52 GMT+0800 2013"));
        service.create(info,null);

        info.setTripId("Z1236");
        info.setTrainTypeId("ZhiDa");
        info.setRouteId("d693a2c5-ef87-4a3c-bef8-600b43f62c68");
        info.setStartingStationId("shanghai");
        info.setStationsId("nanjing");
        info.setTerminalStationId("beijing");
        info.setStartingTime(new Date("Mon May 04 7:05:52 GMT+0800 2013"));
        info.setEndTime(new Date("Mon May 04 12:51:52 GMT+0800 2013"));
        service.create(info,null);

        info.setTripId("T1235");
        info.setTrainTypeId("TeKuai");
        info.setRouteId("20eb7122-3a11-423f-b10a-be0dc5bce7db");
        info.setStartingStationId("shanghai");
        info.setStationsId("nanjing");
        info.setTerminalStationId("beijing");
        info.setStartingTime(new Date("Mon May 04 08:31:52 GMT+0800 2013"));
        info.setEndTime(new Date("Mon May 04 17:21:52 GMT+0800 2013"));
        service.create(info,null);

        info.setTripId("K1345");
        info.setTrainTypeId("KuaiSu");
        info.setRouteId("1367db1f-461e-4ab7-87ad-2bcc05fd9cb7");
        info.setStartingStationId("shanghai");
        info.setStationsId("nanjing");
        info.setTerminalStationId("beijing");
        info.setStartingTime(new Date("Mon May 04 07:51:52 GMT+0800 2013"));
        info.setEndTime(new Date("Mon May 04 19:59:52 GMT+0800 2013"));
        service.create(info,null);
    }
}
