package assurance.service;

import assurance.domain.*;
import org.springframework.http.HttpHeaders;

import java.util.List;
import java.util.UUID;

public interface AssuranceService {

//    Assurance createAssurance(Assurance assurance);

    Assurance findAssuranceById(UUID id, HttpHeaders headers);

    Assurance findAssuranceByOrderId(UUID orderId, HttpHeaders headers);

    AddAssuranceResult create(AddAssuranceInfo aai, HttpHeaders headers);

    DeleteAssuranceResult deleteById(UUID assuranceId, HttpHeaders headers);

    DeleteAssuranceResult deleteByOrderId(UUID orderId, HttpHeaders headers);

    ModifyAssuranceResult modify(ModifyAssuranceInfo info, HttpHeaders headers);

    GetAllAssuranceResult getAllAssurances(HttpHeaders headers);

    List<AssuranceTypeBean> getAllAssuranceTypes(HttpHeaders headers);
}
