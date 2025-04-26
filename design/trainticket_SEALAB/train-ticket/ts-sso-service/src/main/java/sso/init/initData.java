package sso.init;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import sso.domain.Account;
import sso.domain.DocumentType;
import sso.domain.Gender;
import sso.service.AccountSsoService;
import java.util.UUID;

@Component
public class initData implements CommandLineRunner {

    @Autowired
    private AccountSsoService ssoService;

    @Override
    public void run(String... args) throws Exception {
        Account acc = new Account();
        acc.setDocumentType(DocumentType.ID_CARD.getCode());
        acc.setDocumentNum("DefaultDocumentNumber");
        acc.setEmail("fdse_microservices@163.com");
        acc.setPassword("DefaultPassword");
        acc.setName("Default User");
        acc.setGender(Gender.MALE.getCode());
        acc.setId(UUID.fromString("4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f"));
        ssoService.createAccount(acc, null);

        acc = new Account();
        acc.setDocumentType(DocumentType.ID_CARD.getCode());
        acc.setDocumentNum("DefaultDocumentNumber");
        acc.setEmail("root@163.com");
        acc.setPassword("adminroot");
        acc.setName("adminroot");
        acc.setGender(Gender.MALE.getCode());
        acc.setId(UUID.fromString("1d1a11c1-11cb-1cf1-b1bb-b11111d1da1f"));
        ssoService.createAccount(acc, null);
    }

}
