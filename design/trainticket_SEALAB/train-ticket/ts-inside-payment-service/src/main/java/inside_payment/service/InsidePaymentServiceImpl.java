package inside_payment.service;

import inside_payment.async.AsyncTask;
import inside_payment.domain.*;
import inside_payment.repository.AddMoneyRepository;
import inside_payment.repository.PaymentRepository;
import inside_payment.util.CookieUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import javax.servlet.http.HttpServletRequest;
import java.math.BigDecimal;
import java.util.*;

@Service
public class InsidePaymentServiceImpl implements InsidePaymentService{

    @Autowired
    public AddMoneyRepository addMoneyRepository;

    @Autowired
    public PaymentRepository paymentRepository;

    @Autowired
    public RestTemplate restTemplate;

    @Override
    public boolean pay(PaymentInfo info, HttpServletRequest request, HttpHeaders headers){
//        QueryOrderResult result;
        String userId = CookieUtil.getCookieByName(request,"loginId").getValue();

        GetOrderByIdInfo getOrderByIdInfo = new GetOrderByIdInfo();
        getOrderByIdInfo.setOrderId(info.getOrderId());
        GetOrderResult result;

        if(info.getTripId().startsWith("G") || info.getTripId().startsWith("D")){

            HttpEntity requestGetOrderResults = new HttpEntity(getOrderByIdInfo,headers);
            ResponseEntity<GetOrderResult> reGetOrderResults = restTemplate.exchange(
                    "http://ts-order-service:12031/order/getById",
                    HttpMethod.POST,
                    requestGetOrderResults,
                    GetOrderResult.class);
            result = reGetOrderResults.getBody();

//            result = restTemplate.postForObject("http://ts-order-service:12031/order/getById",getOrderByIdInfo,GetOrderResult.class);
             //result = restTemplate.postForObject(
             //       "http://ts-order-service:12031/order/price", new QueryOrder(info.getOrderId()),QueryOrderResult.class);
        }else{


            HttpEntity requestGetOrderResults = new HttpEntity(getOrderByIdInfo,headers);
            ResponseEntity<GetOrderResult> reGetOrderResults = restTemplate.exchange(
                    "http://ts-order-other-service:12032/orderOther/getById",
                    HttpMethod.POST,
                    requestGetOrderResults,
                    GetOrderResult.class);
            result = reGetOrderResults.getBody();

//            result = restTemplate.postForObject("http://ts-order-other-service:12032/orderOther/getById",getOrderByIdInfo,GetOrderResult.class);
            //result = restTemplate.postForObject(
            //      "http://ts-order-other-service:12032/orderOther/price", new QueryOrder(info.getOrderId()),QueryOrderResult.class);
        }

        if(result.isStatus()){

            if(result.getOrder().getStatus() != OrderStatus.NOTPAID.getCode()){
                System.out.println("[Inside Payment Service][Pay] Error. Order status Not allowed to Pay.");
                return false;
            }

            Payment payment = new Payment();
            payment.setOrderId(info.getOrderId());
            payment.setPrice(result.getOrder().getPrice());
            payment.setUserId(userId);

            //判断一下账户余额够不够，不够要去站外支付
            List<Payment> payments = paymentRepository.findByUserId(userId);
            List<AddMoney> addMonies = addMoneyRepository.findByUserId(userId);
            Iterator<Payment> paymentsIterator = payments.iterator();
            Iterator<AddMoney> addMoniesIterator = addMonies.iterator();

            BigDecimal totalExpand = new BigDecimal("0");
            while(paymentsIterator.hasNext()){
                Payment p = paymentsIterator.next();
                totalExpand = totalExpand.add(new BigDecimal(p.getPrice()));
            }
            totalExpand = totalExpand.add(new BigDecimal(result.getOrder().getPrice()));

            BigDecimal money = new BigDecimal("0");
            while(addMoniesIterator.hasNext()){
                AddMoney addMoney = addMoniesIterator.next();
                money = money.add(new BigDecimal(addMoney.getMoney()));
            }

            if(totalExpand.compareTo(money) > 0){
                //站外支付
                OutsidePaymentInfo outsidePaymentInfo = new OutsidePaymentInfo();
                outsidePaymentInfo.setOrderId(info.getOrderId());
                outsidePaymentInfo.setUserId(userId);
                outsidePaymentInfo.setPrice(result.getOrder().getPrice());


                /****这里异步调用第三方支付***/

                HttpEntity requestEntityOutsidePaySuccess = new HttpEntity(outsidePaymentInfo,headers);
                ResponseEntity<Boolean> reOutsidePaySuccess = restTemplate.exchange(
                        "http://ts-payment-service:19001/payment/pay",
                        HttpMethod.POST,
                        requestEntityOutsidePaySuccess,
                        Boolean.class);
                boolean outsidePaySuccess = reOutsidePaySuccess.getBody();

//                boolean outsidePaySuccess = restTemplate.postForObject(
//                        "http://ts-payment-service:19001/payment/pay", outsidePaymentInfo,Boolean.class);
//                boolean outsidePaySuccess = false;
//                try{
//                    System.out.println("[Payment Service][Turn To Outside Patment] Async Task Begin");
//                    Future<Boolean> task = asyncTask.sendAsyncCallToPaymentService(outsidePaymentInfo);
//                    outsidePaySuccess = task.get(2000,TimeUnit.MILLISECONDS).booleanValue();
//
//                }catch (Exception e){
//                    System.out.println("[Inside Payment][Turn to Outside Payment] Time Out.");
//                    //e.printStackTrace();
//                    return false;
//                }

                if(outsidePaySuccess){
                    payment.setType(PaymentType.O);
                    paymentRepository.save(payment);
                    setOrderStatus(info.getTripId(),info.getOrderId(), headers);
                    return true;
                }else{
                    return false;
                }
            }else{
                setOrderStatus(info.getTripId(),info.getOrderId(), headers);
                payment.setType(PaymentType.P);
                paymentRepository.save(payment);
            }
                return true;

        }else{
            return false;
        }
    }

    @Override
    public boolean createAccount(CreateAccountInfo info, HttpHeaders headers){
        List<AddMoney> list = addMoneyRepository.findByUserId(info.getUserId());
        if(list.size() == 0){
            AddMoney addMoney = new AddMoney();
            addMoney.setMoney(info.getMoney());
            addMoney.setUserId(info.getUserId());
            addMoney.setType(AddMoneyType.A);
            addMoneyRepository.save(addMoney);
            return true;
        }else{
            return false;
        }
    }

    @Override
    public boolean addMoney(AddMoneyInfo info, HttpHeaders headers){
        if(addMoneyRepository.findByUserId(info.getUserId()) != null){
            AddMoney addMoney = new AddMoney();
            addMoney.setUserId(info.getUserId());
            addMoney.setMoney(info.getMoney());
            addMoney.setType(AddMoneyType.A);
            addMoneyRepository.save(addMoney);
            return true;
        }else{
            return false;
        }
    }

    @Override
    public List<Balance> queryAccount(HttpHeaders headers){
        List<Balance> result = new ArrayList<Balance>();
        List<AddMoney> list = addMoneyRepository.findAll();
        Iterator<AddMoney> ite = list.iterator();
        HashMap<String,String> map = new HashMap<String,String>();
        while(ite.hasNext()){
            AddMoney addMoney = ite.next();
            if(map.containsKey(addMoney.getUserId())){
                BigDecimal money = new BigDecimal(map.get(addMoney.getUserId()));
                map.put(addMoney.getUserId(),money.add(new BigDecimal(addMoney.getMoney())).toString());
            }else{
                map.put(addMoney.getUserId(),addMoney.getMoney());
            }
        }

        Iterator ite1 = map.entrySet().iterator();
        while(ite1.hasNext()){
            Map.Entry entry = (Map.Entry) ite1.next();
            String userId = (String)entry.getKey();
            String money = (String)entry.getValue();

            List<Payment> payments = paymentRepository.findByUserId(userId);
            Iterator<Payment> iterator = payments.iterator();
            String totalExpand = "0";
            while(iterator.hasNext()){
                Payment p = iterator.next();
                BigDecimal expand = new BigDecimal(totalExpand);
                totalExpand = expand.add(new BigDecimal(p.getPrice())).toString();
            }
            String balanceMoney = new BigDecimal(money).subtract(new BigDecimal(totalExpand)).toString();
            Balance balance = new Balance();
            balance.setUserId(userId);
            balance.setBalance(balanceMoney);
            result.add(balance);
        }

        return result;
    }

    public String queryAccount(String userId, HttpHeaders headers){
        List<Payment> payments = paymentRepository.findByUserId(userId);
        List<AddMoney> addMonies = addMoneyRepository.findByUserId(userId);
        Iterator<Payment> paymentsIterator = payments.iterator();
        Iterator<AddMoney> addMoniesIterator = addMonies.iterator();

        BigDecimal totalExpand = new BigDecimal("0");
        while(paymentsIterator.hasNext()){
            Payment p = paymentsIterator.next();
            totalExpand.add(new BigDecimal(p.getPrice()));
        }

        BigDecimal money = new BigDecimal("0");
        while(addMoniesIterator.hasNext()){
            AddMoney addMoney = addMoniesIterator.next();
            money.add(new BigDecimal(addMoney.getMoney()));
        }

        String result = money.subtract(totalExpand).toString();
        return result;
    }

    @Override
    public List<Payment> queryPayment(HttpHeaders headers){
        return paymentRepository.findAll();
    }

    @Override
    public boolean drawBack(DrawBackInfo info, HttpHeaders headers){
        if(addMoneyRepository.findByUserId(info.getUserId()) != null){
            AddMoney addMoney = new AddMoney();
            addMoney.setUserId(info.getUserId());
            addMoney.setMoney(info.getMoney());
            addMoney.setType(AddMoneyType.D);
            addMoneyRepository.save(addMoney);
            return true;
        }else{
            return false;
        }
    }

    @Override
    public boolean payDifference(PaymentDifferenceInfo info, HttpServletRequest request, HttpHeaders headers){
        QueryOrderResult result;
        String userId = info.getUserId();

        Payment payment = new Payment();
        payment.setOrderId(info.getOrderId());
        payment.setPrice(info.getPrice());
        payment.setUserId(info.getUserId());


        List<Payment> payments = paymentRepository.findByUserId(userId);
        List<AddMoney> addMonies = addMoneyRepository.findByUserId(userId);
        Iterator<Payment> paymentsIterator = payments.iterator();
        Iterator<AddMoney> addMoniesIterator = addMonies.iterator();

        BigDecimal totalExpand = new BigDecimal("0");
        while(paymentsIterator.hasNext()){
            Payment p = paymentsIterator.next();
            totalExpand.add(new BigDecimal(p.getPrice()));
        }
        totalExpand.add(new BigDecimal(info.getPrice()));

        BigDecimal money = new BigDecimal("0");
        while(addMoniesIterator.hasNext()){
            AddMoney addMoney = addMoniesIterator.next();
            money.add(new BigDecimal(addMoney.getMoney()));
        }

        if(totalExpand.compareTo(money) > 0){
            //站外支付
            OutsidePaymentInfo outsidePaymentInfo = new OutsidePaymentInfo();
            outsidePaymentInfo.setOrderId(info.getOrderId());
            outsidePaymentInfo.setUserId(userId);
            outsidePaymentInfo.setPrice(info.getPrice());

            HttpEntity requestEntityOutsidePaySuccess = new HttpEntity(outsidePaymentInfo,headers);
            ResponseEntity<Boolean> reOutsidePaySuccess = restTemplate.exchange(
                    "http://ts-payment-service:19001/payment/pay",
                    HttpMethod.POST,
                    requestEntityOutsidePaySuccess,
                    Boolean.class);
            boolean outsidePaySuccess = reOutsidePaySuccess.getBody();

//            boolean outsidePaySuccess = restTemplate.postForObject(
//                    "http://ts-payment-service:19001/payment/pay", outsidePaymentInfo,Boolean.class);
            if(outsidePaySuccess){
                payment.setType(PaymentType.E);
                paymentRepository.save(payment);
                return true;
            }else{
                return false;
            }
        }else{
            payment.setType(PaymentType.E);
            paymentRepository.save(payment);
        }

        return true;


    }

    @Override
    public List<AddMoney> queryAddMoney(HttpHeaders headers){
        return addMoneyRepository.findAll();
    }

    private ModifyOrderStatusResult setOrderStatus(String tripId,String orderId, HttpHeaders headers){
        ModifyOrderStatusInfo info = new ModifyOrderStatusInfo();
        info.setOrderId(orderId);
        info.setStatus(1);   //order paid and not collected

        ModifyOrderStatusResult result;
        if(tripId.startsWith("G") || tripId.startsWith("D")){

            HttpEntity requestEntityModifyOrderStatusResult = new HttpEntity(info,headers);
            ResponseEntity<ModifyOrderStatusResult> reModifyOrderStatusResult= restTemplate.exchange(
                    "http://ts-order-service:12031/order/modifyOrderStatus",
                    HttpMethod.POST,
                    requestEntityModifyOrderStatusResult,
                    ModifyOrderStatusResult.class);
            result = reModifyOrderStatusResult.getBody();

//            result = restTemplate.postForObject(
//                    "http://ts-order-service:12031/order/modifyOrderStatus", info, ModifyOrderStatusResult.class);
        }else{

            HttpEntity requestEntityModifyOrderStatusResult = new HttpEntity(info,headers);
            ResponseEntity<ModifyOrderStatusResult> reModifyOrderStatusResult= restTemplate.exchange(
                    "http://ts-order-other-service:12032/orderOther/modifyOrderStatus",
                    HttpMethod.POST,
                    requestEntityModifyOrderStatusResult,
                    ModifyOrderStatusResult.class);
            result = reModifyOrderStatusResult.getBody();

//            result = restTemplate.postForObject(
//                    "http://ts-order-other-service:12032/orderOther/modifyOrderStatus", info, ModifyOrderStatusResult.class);
        }
        return result;
    }

    @Override
    public void initPayment(Payment payment, HttpHeaders headers){
        Payment paymentTemp = paymentRepository.findById(payment.getId());
        if(paymentTemp == null){
            paymentRepository.save(payment);
        }else{
            System.out.println("[Inside Payment Service][Init Payment] Already Exists:" + payment.getId());
        }
    }

//    private boolean sendOrderCreateEmail(){
//        result = restTemplate.postForObject(
//                "http://ts-notification-service:12031/order/modifyOrderStatus", info, ModifyOrderStatusResult.class);
//        return true;
//    }
}
