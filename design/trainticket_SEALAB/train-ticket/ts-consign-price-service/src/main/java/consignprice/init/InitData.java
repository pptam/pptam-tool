package consignprice.init;

import consignprice.domain.PriceConfig;
import consignprice.service.ConsignPriceService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.util.UUID;

@Component
public class InitData implements CommandLineRunner {
    @Autowired
    ConsignPriceService service;

    @Override
    public void run(String... strings) throws Exception {
        System.out.println("[Consign price service] [Init data operation]");
        PriceConfig config = new PriceConfig();
        config.setId(UUID.randomUUID());
        config.setIndex(0);
        config.setInitialPrice(8);
        config.setInitialWeight(1);
        config.setWithinPrice(2);
        config.setBeyondPrice(4);

        service.createAndModifyPrice(config, null);
    }
}
