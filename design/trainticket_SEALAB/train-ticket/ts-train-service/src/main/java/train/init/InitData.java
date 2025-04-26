package train.init;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import train.domain.Information;
import train.service.TrainService;


@Component
public class InitData implements CommandLineRunner{

    @Autowired
    TrainService service;

    @Override
    public void run(String... args) throws Exception {
        Information info = new Information();

        info.setId("GaoTieOne");
        info.setConfortClass(60);
        info.setEconomyClass(120);
        info.setAverageSpeed(250);
        service.create(info,null);

        info.setId("GaoTieTwo");
        info.setConfortClass(80);
        info.setEconomyClass(200);
        info.setAverageSpeed(200);
        service.create(info,null);

        info.setId("DongCheOne");
        info.setConfortClass(100);
        info.setEconomyClass(300);
        info.setAverageSpeed(180);
        service.create(info,null);

        info.setId("ZhiDa");
        info.setConfortClass(60);
        info.setEconomyClass(120);
        info.setAverageSpeed(120);
        service.create(info,null);

        info.setId("TeKuai");
        info.setConfortClass(80);
        info.setEconomyClass(200);
        info.setAverageSpeed(120);
        service.create(info,null);

        info.setId("KuaiSu");
        info.setConfortClass(100);
        info.setEconomyClass(300);
        info.setAverageSpeed(90);
        service.create(info,null);
    }
}
