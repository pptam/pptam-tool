package other.domain;

import javax.validation.Valid;
import javax.validation.constraints.NotNull;
import java.util.Set;

public class LeftTicketInfo {
    @Valid
    @NotNull
    private Set<Ticket> soldTickets;

    public LeftTicketInfo(){

    }

    public Set<Ticket> getSoldTickets() {
        return soldTickets;
    }

    public void setSoldTickets(Set<Ticket> soldTickets) {
        this.soldTickets = soldTickets;
    }

}
