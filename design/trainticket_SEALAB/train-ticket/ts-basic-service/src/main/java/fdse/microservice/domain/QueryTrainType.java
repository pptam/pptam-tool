package fdse.microservice.domain;

import javax.validation.Valid;


public class QueryTrainType {
    @Valid
    private String id;

    public QueryTrainType(String id) {
        this.id = id;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }
}
