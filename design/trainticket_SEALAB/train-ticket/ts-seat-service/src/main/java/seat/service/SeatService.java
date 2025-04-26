package seat.service;

import org.springframework.http.HttpHeaders;
import seat.domain.SeatRequest;
import seat.domain.Ticket;

public interface SeatService {

    Ticket distributeSeat(SeatRequest seatRequest,HttpHeaders headers);
    int getLeftTicketOfInterval(SeatRequest seatRequest,HttpHeaders headers);
}
