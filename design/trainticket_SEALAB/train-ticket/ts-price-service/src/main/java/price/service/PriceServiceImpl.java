package price.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.stereotype.Service;
import price.domain.CreateAndModifyPriceConfig;
import price.domain.PriceConfig;
import price.domain.ReturnManyPriceConfigResult;
import price.domain.ReturnSinglePriceConfigResult;
import price.repository.PriceConfigRepository;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Service
public class PriceServiceImpl implements PriceService{

    @Autowired
    private PriceConfigRepository priceConfigRepository;

    @Override
    public ReturnSinglePriceConfigResult createNewPriceConfig(CreateAndModifyPriceConfig createAndModifyPriceConfig, HttpHeaders headers) {
        System.out.println("[Price Service][Create New Price Config]");
        ReturnSinglePriceConfigResult result = new ReturnSinglePriceConfigResult();
        if(createAndModifyPriceConfig.getId() == null || createAndModifyPriceConfig.getId().length() < 10){
            PriceConfig priceConfig = new PriceConfig();
            priceConfig.setId(UUID.randomUUID());
            priceConfig.setBasicPriceRate(createAndModifyPriceConfig.getBasicPriceRate());
            priceConfig.setFirstClassPriceRate(createAndModifyPriceConfig.getFirstClassPriceRate());
            priceConfig.setRouteId(createAndModifyPriceConfig.getRouteId());
            priceConfig.setTrainType(createAndModifyPriceConfig.getTrainType());
            priceConfigRepository.save(priceConfig);
            result.setPriceConfig(priceConfig);
            result.setMessage("Success.");
            result.setStatus(true);
        }else{
            PriceConfig priceConfig = priceConfigRepository.findById(UUID.fromString(createAndModifyPriceConfig.getId()));
            if(priceConfig == null){
                priceConfig = new PriceConfig();
                priceConfig.setId(UUID.fromString(createAndModifyPriceConfig.getId()));
            }
            priceConfig.setBasicPriceRate(createAndModifyPriceConfig.getBasicPriceRate());
            priceConfig.setFirstClassPriceRate(createAndModifyPriceConfig.getFirstClassPriceRate());
            priceConfig.setRouteId(createAndModifyPriceConfig.getRouteId());
            priceConfig.setTrainType(createAndModifyPriceConfig.getTrainType());
            priceConfigRepository.save(priceConfig);
            result.setPriceConfig(priceConfig);
            result.setMessage("Success.");
            result.setStatus(true);
        }
        return result;
    }

    @Override
    public ReturnSinglePriceConfigResult findById(String id, HttpHeaders headers) {
        System.out.println("[Price Service][Find By Id] ID:" + id);
        PriceConfig priceConfig = priceConfigRepository.findById(UUID.fromString(id));
        ReturnSinglePriceConfigResult result = new ReturnSinglePriceConfigResult();
        if(priceConfig == null){
            result.setStatus(false);
            result.setMessage("Price Config Not Found");
            result.setPriceConfig(null);
        }else{
            result.setStatus(true);
            result.setMessage("Success");
            result.setPriceConfig(priceConfig);
        }
        return result;
    }

    @Override
    public ReturnSinglePriceConfigResult findByRouteIdAndTrainType(String routeId, String trainType, HttpHeaders headers) {
        System.out.println("[Price Service][Find By Route And Train Type] Rote:" + routeId + "Train Type:" + trainType);
        PriceConfig priceConfig = priceConfigRepository.findByRouteIdAndTrainType(routeId,trainType);
        ReturnSinglePriceConfigResult result = new ReturnSinglePriceConfigResult();
        if(priceConfig == null){
            result.setStatus(false);
            result.setMessage("Price Config Not Found");
            result.setPriceConfig(null);
            System.out.println("[Price Service][Find By Route Id And Train Type] Fail");

        }else{
            result.setStatus(true);
            result.setMessage("Success");
            result.setPriceConfig(priceConfig);
            System.out.println("[Price Service][Find By Route Id And Train Type] Success");
        }

        return result;
    }



    @Override
    public ReturnManyPriceConfigResult findAllPriceConfig(HttpHeaders headers) {
        ArrayList<PriceConfig> list = priceConfigRepository.findAll();
        ReturnManyPriceConfigResult result = new ReturnManyPriceConfigResult();
        if(list == null){
            list = new ArrayList<>();
        }
        result.setMessage("Success");
        result.setPriceConfig(list);
        result.setStatus(true);
        return result;
    }

    @Override
    public boolean deletePriceConfig(CreateAndModifyPriceConfig c, HttpHeaders headers) {
        PriceConfig priceConfig = priceConfigRepository.findById(UUID.fromString(c.getId()));
        if(priceConfig == null){
            return false;
        } else {
            PriceConfig pc = new PriceConfig();
            pc.setId(UUID.fromString(c.getId()));
            pc.setRouteId(c.getRouteId());
            pc.setTrainType(c.getTrainType());
            pc.setBasicPriceRate(c.getBasicPriceRate());
            pc.setFirstClassPriceRate(c.getFirstClassPriceRate());
            priceConfigRepository.delete(pc);
            return true;
        }
    }

    @Override
    public boolean updatePriceConfig(CreateAndModifyPriceConfig c, HttpHeaders headers) {
        PriceConfig priceConfig = priceConfigRepository.findById(UUID.fromString(c.getId()));
        if(priceConfig == null){
            return false;
        } else {
            priceConfig.setId(UUID.fromString(c.getId()));
            priceConfig.setBasicPriceRate(c.getBasicPriceRate());
            priceConfig.setFirstClassPriceRate(c.getFirstClassPriceRate());
            priceConfig.setRouteId(c.getRouteId());
            priceConfig.setTrainType(c.getTrainType());
            priceConfigRepository.save(priceConfig);
            return true;
        }
    }

}
