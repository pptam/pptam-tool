package hello;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public class Value {

    private Long id;
    private boolean result;

    public Value() {
    }

    public Long getId() {
        return this.id;
    }

    public boolean getContent() {
        return this.result;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public void setContent(boolean result) {
        this.result = result;
    }

    @Override
    public String toString() {
        return "Value{" +
                "id=" + id +
                ", result='" + result + '\'' +
                '}';
    }
}
