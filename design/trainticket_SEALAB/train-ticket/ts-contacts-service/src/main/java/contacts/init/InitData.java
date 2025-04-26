package contacts.init;

import contacts.domain.Contacts;
import contacts.domain.DocumentType;
import contacts.service.ContactsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import java.util.UUID;

@Component
public class InitData implements CommandLineRunner{

    @Autowired
    ContactsService service;

    @Override
    public void run(String... args)throws Exception{
        Contacts contacts_One = new Contacts();
        contacts_One.setAccountId(UUID.fromString("4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f"));
        contacts_One.setDocumentType(DocumentType.ID_CARD.getCode());
        contacts_One.setName("Contacts_One");
        contacts_One.setDocumentNumber("DocumentNumber_One");
        contacts_One.setPhoneNumber("ContactsPhoneNum_One");
        contacts_One.setId(UUID.fromString("4d2a46c7-71cb-4cf1-a5bb-b68406d9da6f"));
        service.createContacts(contacts_One ,null);

        Contacts contacts_Two = new Contacts();
        contacts_Two.setAccountId(UUID.fromString("4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f"));
        contacts_Two.setDocumentType(DocumentType.ID_CARD.getCode());
        contacts_Two.setName("Contacts_Two");
        contacts_Two.setDocumentNumber("DocumentNumber_Two");
        contacts_Two.setPhoneNumber("ContactsPhoneNum_Two");
        contacts_Two.setId(UUID.fromString("4d2546c7-71cb-4cf1-a5bb-b68406d9da6f"));
        service.createContacts(contacts_Two,null);
    }
}
