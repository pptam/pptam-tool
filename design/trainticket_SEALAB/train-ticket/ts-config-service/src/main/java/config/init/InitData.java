package config.init;

import config.domain.Information;
import config.service.ConfigService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;


@Component
public class InitData implements CommandLineRunner{

    @Autowired
    ConfigService service;

    @Override
    public void run(String... args) throws Exception {
        Information info = new Information();

        info.setName("DirectTicketAllocationProportion");
        info.setValue("0.5");
        info.setDescription("Allocation Proportion Of The Direct Ticket - From Start To End");
        service.create(info,null);

//        info.setName("GaoTieOne_economyClass_priceRate");
//        info.setValue("7");
//        info.setDescription("");
//        service.create(info);
//
//        info.setName("GaoTieOne_confortClass_priceRate");
//        info.setValue("10");
//        info.setDescription("");
//        service.create(info);
//
//        info.setName("GaoTieTwo_economyClass_priceRate");
//        info.setValue("7");
//        info.setDescription("");
//        service.create(info);
//
//        info.setName("GaoTieTwo_confortClass_priceRate");
//        info.setValue("10");
//        info.setDescription("");
//        service.create(info);
//
//        info.setName("DongCheOne_economyClass_priceRate");
//        info.setValue("6");
//        info.setDescription("");
//        service.create(info);
//
//        info.setName("DongCheOne_confortClass_priceRate");
//        info.setValue("9");
//        info.setDescription("");
//        service.create(info);
//
//        info.setName("ZhiDa_economyClass_priceRate");
//        info.setValue("4");
//        info.setDescription("");
//        service.create(info);
//
//        info.setName("ZhiDa_confortClass_priceRate");
//        info.setValue("6");
//        info.setDescription("");
//        service.create(info);
//
//        info.setName("TeKuai_economyClass_priceRate");
//        info.setValue("3");
//        info.setDescription("");
//        service.create(info);
//
//        info.setName("TeKuai_confortClass_priceRate");
//        info.setValue("5");
//        info.setDescription("");
//        service.create(info);
//
//        info.setName("KuaiSu_economyClass_priceRate");
//        info.setValue("2");
//        info.setDescription("");
//        service.create(info);
//
//        info.setName("KuaiSu_confortClass_priceRate");
//        info.setValue("3");
//        info.setDescription("");
//        service.create(info);
    }
}
