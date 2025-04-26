package notification.service;

import notification.domain.Mail;
import notification.domain.NotifyInfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;
import java.util.HashMap;
import java.util.Map;

@Service
public class NotificationServiceImpl implements NotificationService{

    @Autowired
    private JavaMailSender mailSender;

    @Autowired
    MailService mailService;

    @Override
    public boolean preserve_success(NotifyInfo info, HttpHeaders headers){
        Mail mail = new Mail();
        mail.setMailFrom("fdse_microservices@163.com");
        mail.setMailTo(info.getEmail());
        mail.setMailSubject("Preserve Success");

        Map<String, Object> model = new HashMap<String, Object>();
        model.put("username", info.getUsername());
        model.put("startingPlace",info.getStartingPlace());
        model.put("endPlace",info.getEndPlace());
        model.put("startingTime",info.getStartingTime());
        model.put("date",info.getDate());
        model.put("seatClass",info.getSeatClass());
        model.put("seatNumber",info.getSeatNumber());
        model.put("price",info.getPrice());
        mail.setModel(model);

        try {
            mailService.sendEmail(mail,"preserve_success.ftl");
            return true;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    @Override
    public boolean order_create_success(NotifyInfo info, HttpHeaders headers){
        Mail mail = new Mail();
        mail.setMailFrom("fdse_microservices@163.com");
        mail.setMailTo(info.getEmail());
        mail.setMailSubject("Order Create Success");

        Map<String, Object> model = new HashMap<String, Object>();
        model.put("username", info.getUsername());
        model.put("startingPlace",info.getStartingPlace());
        model.put("endPlace",info.getEndPlace());
        model.put("startingTime",info.getStartingTime());
        model.put("date",info.getDate());
        model.put("seatClass",info.getSeatClass());
        model.put("seatNumber",info.getSeatNumber());
        model.put("orderNumber", info.getOrderNumber());
        mail.setModel(model);

        try {
            mailService.sendEmail(mail,"order_create_success.ftl");
            return true;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    @Override
    public boolean order_changed_success(NotifyInfo info, HttpHeaders headers){
        Mail mail = new Mail();
        mail.setMailFrom("fdse_microservices@163.com");
        mail.setMailTo(info.getEmail());
        mail.setMailSubject("Order Changed Success");

        Map<String, Object> model = new HashMap<String, Object>();
        model.put("username", info.getUsername());
        model.put("startingPlace",info.getStartingPlace());
        model.put("endPlace",info.getEndPlace());
        model.put("startingTime",info.getStartingTime());
        model.put("date",info.getDate());
        model.put("seatClass",info.getSeatClass());
        model.put("seatNumber",info.getSeatNumber());
        model.put("orderNumber", info.getOrderNumber());
        mail.setModel(model);

        try {
            mailService.sendEmail(mail,"order_changed_success.ftl");
            return true;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    @Override
    public boolean order_cancel_success(NotifyInfo info, HttpHeaders headers){
        Mail mail = new Mail();
        mail.setMailFrom("fdse_microservices@163.com");
        mail.setMailTo(info.getEmail());
        mail.setMailSubject("Order Cancel Success");

        Map<String, Object> model = new HashMap<String, Object>();
        model.put("username", info.getUsername());
        model.put("price",info.getPrice());
        mail.setModel(model);

        try {
            mailService.sendEmail(mail,"order_cancel_success.ftl");
            return true;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }
}
