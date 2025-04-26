package notification.service;

import notification.domain.NotifyInfo;
import org.springframework.http.HttpHeaders;

/**
 * Created by Wenyi on 2017/6/15.
 */
public interface NotificationService {
    boolean preserve_success(NotifyInfo info, HttpHeaders headers);
    boolean order_create_success(NotifyInfo info, HttpHeaders headers);
    boolean order_changed_success(NotifyInfo info, HttpHeaders headers);
    boolean order_cancel_success(NotifyInfo info, HttpHeaders headers);
}
