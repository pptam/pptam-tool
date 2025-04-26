package consignprice.service;

import consignprice.entity.ConsignPrice;
import consignprice.repository.ConsignPriceConfigRepository;
import edu.fudan.common.util.Response;

import java.util.UUID;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.stereotype.Service;

/**
 * @author fdse
 */
@Service
public class ConsignPriceServiceImpl implements ConsignPriceService {

    @Autowired
    private ConsignPriceConfigRepository repository;

    String success = "Success";

    private static final Logger LOGGER = LoggerFactory.getLogger(ConsignPriceServiceImpl.class);

    @Override
    public Response getPriceByWeightAndRegion(double weight, boolean isWithinRegion, HttpHeaders headers) {
        ConsignPrice priceConfig = repository.findByIndex(0);
        double price = 0;
        double initialPrice = priceConfig.getInitialPrice();
        if (weight <= priceConfig.getInitialWeight()) {
            price = initialPrice;
        } else {
            double extraWeight = weight - priceConfig.getInitialWeight();
            if (isWithinRegion) {
                price = initialPrice + extraWeight * priceConfig.getWithinPrice();
            }else {
                price = initialPrice + extraWeight * priceConfig.getBeyondPrice();
            }
        }
        return new Response<>(1, success, price);
    }

    @Override
    public Response queryPriceInformation(HttpHeaders headers) {
        StringBuilder sb = new StringBuilder();
        ConsignPrice price = repository.findByIndex(0);
        sb.append("The price of weight within ");
        sb.append(price.getInitialWeight());
        sb.append(" is ");
        sb.append(price.getInitialPrice());
        sb.append(". The price of extra weight within the region is ");
        sb.append(price.getWithinPrice());
        sb.append(" and beyond the region is ");
        sb.append(price.getBeyondPrice());
        sb.append("\n");
        return new Response<>(1, success, sb.toString());
    }

    @Override
    public Response createAndModifyPrice(ConsignPrice config, HttpHeaders headers) {
        ConsignPriceServiceImpl.LOGGER.info("[createAndModifyPrice][Starting Operation]");
    
        // 查找现有记录
        ConsignPrice originalConfig = repository.findByIndex(0);
    
        if (originalConfig == null) {
            // 创建新记录
            ConsignPriceServiceImpl.LOGGER.info("[createAndModifyPrice][Creating New Price Config]");
            originalConfig = new ConsignPrice();
            originalConfig.setId(UUID.randomUUID().toString()); // 生成新 ID
        } else {
            // 更新现有记录
            ConsignPriceServiceImpl.LOGGER.info("[createAndModifyPrice][Updating Existing Price Config]");
        }
    
        // 设置/更新字段
        originalConfig.setIndex(0);
        originalConfig.setInitialPrice(config.getInitialPrice());
        originalConfig.setInitialWeight(config.getInitialWeight());
        originalConfig.setWithinPrice(config.getWithinPrice());
        originalConfig.setBeyondPrice(config.getBeyondPrice());
    
        // 保存记录（JPA 会根据主键自动区分是插入还是更新）
        ConsignPrice newConfig = repository.save(originalConfig);
    
        return new Response<>(1, "Success", newConfig);
    }

    @Override
    public Response getPriceConfig(HttpHeaders headers) {
        return new Response<>(1, success, repository.findByIndex(0));
    }
}
