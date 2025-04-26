package price.init;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import price.domain.CreateAndModifyPriceConfig;
import price.service.PriceService;


/**
 * Created by Chenjie Xu on 2017/6/12.
 */

@Component
public class InitData implements CommandLineRunner {

    @Autowired
    PriceService service;

    public void run(String... args)throws Exception{
        CreateAndModifyPriceConfig priceConfig = new CreateAndModifyPriceConfig();
        priceConfig.setId("6d20b8cb-039c-474c-ae25-b6177ea41152");
        priceConfig.setRouteId("92708982-77af-4318-be25-57ccb0ff69ad");
        priceConfig.setTrainType("GaoTieOne");
        priceConfig.setBasicPriceRate(0.38);
        priceConfig.setFirstClassPriceRate(1.0);
        service.createNewPriceConfig(priceConfig, null);

        priceConfig.setId("c5679b7e-4a54-4f52-9939-1ae86ba16fa7");
        priceConfig.setRouteId("aefcef3f-3f42-46e8-afd7-6cb2a928bd3d");
        priceConfig.setTrainType("GaoTieOne");
        priceConfig.setBasicPriceRate(0.5);
        priceConfig.setFirstClassPriceRate(1.0);
        service.createNewPriceConfig(priceConfig, null);

        priceConfig.setId("719287d6-d3e7-4b54-9a92-71d039748b22");
        priceConfig.setRouteId("a3f256c1-0e43-4f7d-9c21-121bf258101f");
        priceConfig.setTrainType("GaoTieOne");
        priceConfig.setBasicPriceRate(0.7);
        priceConfig.setFirstClassPriceRate(1.0);
        service.createNewPriceConfig(priceConfig, null);

        priceConfig.setId("7de18cf8-bb17-4bb2-aeb4-85d8176d3a93");
        priceConfig.setRouteId("084837bb-53c8-4438-87c8-0321a4d09917");
        priceConfig.setTrainType("GaoTieTwo");
        priceConfig.setBasicPriceRate(0.6);
        priceConfig.setFirstClassPriceRate(1.0);
        service.createNewPriceConfig(priceConfig, null);

        priceConfig.setId("d5c4523a-827c-468c-95be-e9024a40572e");
        priceConfig.setRouteId("f3d4d4ef-693b-4456-8eed-59c0d717dd08");
        priceConfig.setTrainType("DongCheOne");
        priceConfig.setBasicPriceRate(0.45);
        priceConfig.setFirstClassPriceRate(1.0);
        service.createNewPriceConfig(priceConfig, null);

        priceConfig.setId("b90a6ad7-ffad-4624-9655-48e9e185fa6c");
        priceConfig.setRouteId("0b23bd3e-876a-4af3-b920-c50a90c90b04");
        priceConfig.setTrainType("ZhiDa");
        priceConfig.setBasicPriceRate(0.35);
        priceConfig.setFirstClassPriceRate(1.0);
        service.createNewPriceConfig(priceConfig, null);

        priceConfig.setId("8fb01829-393f-4af4-9e96-f72866f94d14");
        priceConfig.setRouteId("9fc9c261-3263-4bfa-82f8-bb44e06b2f52");
        priceConfig.setTrainType("ZhiDa");
        priceConfig.setBasicPriceRate(0.35);
        priceConfig.setFirstClassPriceRate(1.0);
        service.createNewPriceConfig(priceConfig, null);

        priceConfig.setId("8b059dc5-01a2-4f8f-8f94-6c886b38bb34");
        priceConfig.setRouteId("d693a2c5-ef87-4a3c-bef8-600b43f62c68");
        priceConfig.setTrainType("ZhiDa");
        priceConfig.setBasicPriceRate(0.32);
        service.createNewPriceConfig(priceConfig, null);

        priceConfig.setId("dd0e572e-7443-420c-8280-7d8215636069");
        priceConfig.setRouteId("20eb7122-3a11-423f-b10a-be0dc5bce7db");
        priceConfig.setTrainType("TeKuai");
        priceConfig.setBasicPriceRate(0.30);
        priceConfig.setFirstClassPriceRate(1.0);
        service.createNewPriceConfig(priceConfig, null);

        priceConfig.setId("0eb474c9-f8be-4119-8681-eb538a404a6a");
        priceConfig.setRouteId("1367db1f-461e-4ab7-87ad-2bcc05fd9cb7");
        priceConfig.setTrainType("KuaiSu");
        priceConfig.setBasicPriceRate(0.2);
        priceConfig.setFirstClassPriceRate(1.0);
        service.createNewPriceConfig(priceConfig, null);
    }
}
