package config.domain;

import javax.validation.Valid;
import javax.validation.constraints.NotNull;


public class Information {
    @Valid
    @NotNull
    private String name;

    @Valid
    @NotNull
    private String value;

    @Valid
    private String description;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        this.value = value;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }
}
