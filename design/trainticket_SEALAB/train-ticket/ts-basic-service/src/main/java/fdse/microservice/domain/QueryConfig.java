package fdse.microservice.domain;

import javax.validation.Valid;
import javax.validation.constraints.NotNull;


public class QueryConfig {

    @Valid
    @NotNull
    private String name;

    public QueryConfig(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
