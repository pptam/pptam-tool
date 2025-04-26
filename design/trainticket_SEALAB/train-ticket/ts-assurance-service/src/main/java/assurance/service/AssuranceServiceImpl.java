package assurance.service;

import assurance.domain.*;
import assurance.repository.AssuranceRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;

@Service
public class AssuranceServiceImpl implements AssuranceService {

    @Autowired
    private AssuranceRepository assuranceRepository;

//    @Override
//    public Assurance createAssurance(Assurance assurance) {
//        Assurance assuranceTemp = assuranceRepository.findById(assurance.getId());
//        if(assuranceTemp != null){
//            System.out.println("[Assurance Service][Init Assurance] Already Exists Id:" + assurance.getId());
//        } else {
//            assuranceRepository.save(assurance);
//        }
//        return assurance;
//    }

    @Override
    public Assurance findAssuranceById(UUID id, HttpHeaders headers) {
        return assuranceRepository.findById(id);
    }

    @Override
    public Assurance findAssuranceByOrderId(UUID orderId, HttpHeaders headers) {
        return assuranceRepository.findByOrderId(orderId);
    }

    @Override
    public AddAssuranceResult create(AddAssuranceInfo aai, HttpHeaders headers) {
        Assurance a = assuranceRepository.findByOrderId(UUID.fromString(aai.getOrderId()));
        AddAssuranceResult aar = new AddAssuranceResult();
        AssuranceType at = AssuranceType.getTypeByIndex(aai.getTypeIndex());
        if(a != null){
            System.out.println("[Assurance-Add&Delete-Service][AddAssurance] Fail.Assurance already exists");
            aar.setStatus(false);
            aar.setMessage("Assurance Already Exists");
            aar.setAssurance(null);
        } else if(at == null){
            System.out.println("[Assurance-Add&Delete-Service][AddAssurance] Fail.Assurance type doesn't exist");
            aar.setStatus(false);
            aar.setMessage("Assurance type doesn't exist");
            aar.setAssurance(null);
        } else{
            Assurance assurance = new Assurance(UUID.randomUUID(), UUID.fromString(aai.getOrderId()), at);
            assuranceRepository.save(assurance);
            System.out.println("[Assurance-Add&Delete-Service][AddAssurance] Success.");
            aar.setStatus(true);
            aar.setMessage("Success");
            aar.setAssurance(assurance);
        }
        return aar;
    }

    @Override
    public DeleteAssuranceResult deleteById(UUID assuranceId, HttpHeaders headers) {
        assuranceRepository.deleteById(assuranceId);
        Assurance a = assuranceRepository.findById(assuranceId);
        DeleteAssuranceResult dar = new DeleteAssuranceResult();
        if(a == null){
            System.out.println("[Assurance-Add&Delete-Service][DeleteAssurance] Success.");
            dar.setStatus(true);
            dar.setMessage("Success");
        } else {
            System.out.println("[Assurance-Add&Delete-Service][DeleteAssurance] Fail.Assurance not clear.");
            dar.setStatus(false);
            dar.setMessage("Reason Not clear");
        }
        return dar;
    }

    @Override
    public DeleteAssuranceResult deleteByOrderId(UUID orderId, HttpHeaders headers) {
        assuranceRepository.removeAssuranceByOrderId(orderId);
        Assurance a = assuranceRepository.findByOrderId(orderId);
        DeleteAssuranceResult dar = new DeleteAssuranceResult();
        if(a == null){
            System.out.println("[Assurance-Add&Delete-Service][DeleteAssurance] Success.");
            dar.setStatus(true);
            dar.setMessage("Success");
        } else {
            System.out.println("[Assurance-Add&Delete-Service][DeleteAssurance] Fail.Assurance not clear.");
            dar.setStatus(false);
            dar.setMessage("Reason Not clear");
        }
        return dar;
    }

    @Override
    public ModifyAssuranceResult modify(ModifyAssuranceInfo info, HttpHeaders headers) {
        Assurance oldAssurance = findAssuranceById(UUID.fromString(info.getAssuranceId()), headers);
        ModifyAssuranceResult mcr = new ModifyAssuranceResult();
        if(oldAssurance == null){
            System.out.println("[Assurance-Modify-Service][ModifyAssurance] Fail.Assurance not found.");
            mcr.setStatus(false);
            mcr.setMessage("Contacts not found");
            mcr.setAssurance(null);
        }else{
            AssuranceType at = AssuranceType.getTypeByIndex(info.getTypeIndex());
            if(at != null){
                oldAssurance.setType(at);
                assuranceRepository.save(oldAssurance);
                System.out.println("[Assurance-Modify-Service][ModifyAssurance] Success.");
                mcr.setStatus(true);
                mcr.setMessage("Success");
                mcr.setAssurance(oldAssurance);
            } else {
                System.out.println("[Assurance-Modify-Service][ModifyAssurance] Fail.Assurance Type not exist.");
                mcr.setStatus(false);
                mcr.setMessage("Assurance Type not exist");
                mcr.setAssurance(null);
            }
        }
        return mcr;
    }

    @Override
    public GetAllAssuranceResult getAllAssurances(HttpHeaders headers) {
        ArrayList<Assurance> as = assuranceRepository.findAll();
        GetAllAssuranceResult gar = new GetAllAssuranceResult();
        gar.setStatus(true);
        gar.setMessage("Success");
        ArrayList<PlainAssurance> result = new ArrayList<PlainAssurance>();
        for(Assurance a : as){
            PlainAssurance pa = new PlainAssurance();
            pa.setId(a.getId());
            pa.setOrderId(a.getOrderId());
            pa.setTypeIndex(a.getType().getIndex());
            pa.setTypeName(a.getType().getName());
            pa.setTypePrice(a.getType().getPrice());
            result.add(pa);
        }
        gar.setAssurances(result);
        return gar;
    }

    @Override
    public  List<AssuranceTypeBean> getAllAssuranceTypes(HttpHeaders headers) {
        List<AssuranceTypeBean> atlist = new ArrayList<AssuranceTypeBean>();
        for(AssuranceType at : AssuranceType.values()){
            AssuranceTypeBean atb = new AssuranceTypeBean();
            atb.setIndex(at.getIndex());
            atb.setName(at.getName());
            atb.setPrice(at.getPrice());
            atlist.add(atb);
        }
        return atlist;
    }
}
