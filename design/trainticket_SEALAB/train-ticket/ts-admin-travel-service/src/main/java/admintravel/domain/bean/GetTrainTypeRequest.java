package admintravel.domain.bean;

import org.springframework.data.annotation.Id;

import javax.validation.Valid;


public class GetTrainTypeRequest {
    @Valid
    @Id
    private String id;

    public GetTrainTypeRequest(){
        //Default Constructor
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }
}
