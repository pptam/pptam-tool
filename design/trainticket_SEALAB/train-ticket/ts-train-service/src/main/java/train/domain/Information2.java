package train.domain;

import org.springframework.data.annotation.Id;

import javax.validation.Valid;


public class Information2 {
    @Valid
    @Id
    private String id;

    public Information2(){
        //Default Constructor
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }
}
