package fdse.microservice.domain;

import org.springframework.data.annotation.Id;

import javax.validation.Valid;
import javax.validation.constraints.NotNull;


public class QueryStation {
    @Valid
    @NotNull
    private String name;

    public QueryStation(){
        //Default Constructor
    }

    public QueryStation(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
