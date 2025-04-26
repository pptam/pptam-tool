package security.init;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import security.domain.CreateSecurityConfigInfo;
import security.service.SecurityService;

@Component
public class initData implements CommandLineRunner {

    @Autowired
    private SecurityService securityService;

    @Override
    public void run(String... args) throws Exception {
        CreateSecurityConfigInfo info1 = new CreateSecurityConfigInfo();
        info1.setName("max_order_1_hour");
        info1.setValue("1000");
        info1.setDescription("Max in 1 hour");
        securityService.addNewSecurityConfig(info1,null);
        CreateSecurityConfigInfo info2 = new CreateSecurityConfigInfo();
        info2.setName("max_order_not_use");
        info2.setValue("1000");
        info2.setDescription("Max not used");
        securityService.addNewSecurityConfig(info2,null);
    }
}
