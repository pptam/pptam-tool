package travel2.domain;

import org.springframework.data.annotation.Id;

import javax.validation.Valid;

public class GetTrainTypeInformation {
    
    @Valid
    @Id
    private String id;

    public GetTrainTypeInformation(){
        //Default Constructor
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }
}
