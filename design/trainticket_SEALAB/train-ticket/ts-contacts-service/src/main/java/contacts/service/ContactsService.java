package contacts.service;

import contacts.domain.*;
import org.springframework.http.HttpHeaders;

import java.util.ArrayList;
import java.util.UUID;

public interface ContactsService {

    Contacts createContacts(Contacts contacts, HttpHeaders headers);

    Contacts findContactsById(UUID id, HttpHeaders headers);

    ArrayList<Contacts> findContactsByAccountId(UUID accountId, HttpHeaders headers);

    AddContactsResult create(AddContactsInfo aci,String accountId, HttpHeaders headers);

    DeleteContactsResult delete(UUID contactsId, HttpHeaders headers);

    ModifyContactsResult modify(ModifyContactsInfo info, HttpHeaders headers);

    GetAllContactsResult getAllContacts(HttpHeaders headers);

}
