package notification.service;


import javax.mail.internet.MimeMessage;

import notification.domain.Mail;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.stereotype.Service;
import org.springframework.ui.freemarker.FreeMarkerTemplateUtils;

import freemarker.template.Configuration;
import freemarker.template.Template;

@Service
public class MailService {

    @Autowired
    private JavaMailSender sender;

    @Autowired
    @Qualifier("freeMarkerConfiguration")
    private Configuration freemarkerConfig;


    public void sendEmail(Mail mail,String template) throws Exception {
        MimeMessage message = sender.createMimeMessage();

        MimeMessageHelper helper = new MimeMessageHelper(message);

        // Using a subfolder such as /templates here
        freemarkerConfig.setClassForTemplateLoading(this.getClass(), "/templates");

        Template t = freemarkerConfig.getTemplate(template);
        String text = FreeMarkerTemplateUtils.processTemplateIntoString(t, mail.getModel());

        helper.setTo(mail.getMailTo());
        helper.setText(text, true);
        helper.setFrom("fdse_microservices@163.com");
        helper.setSubject(mail.getMailSubject());

        sender.send(message);
    }
}
