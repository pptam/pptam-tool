package execute.serivce;

import execute.domain.TicketExecuteInfo;
import execute.domain.TicketExecuteResult;
import org.springframework.http.HttpHeaders;
import sun.security.krb5.internal.Ticket;

public interface ExecuteService {

    TicketExecuteResult ticketExecute(TicketExecuteInfo info, HttpHeaders headers);

    TicketExecuteResult ticketCollect(TicketExecuteInfo info, HttpHeaders headers);

}
