package inside_payment.domain;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import javax.validation.Valid;
import javax.validation.constraints.NotNull;
import java.util.UUID;


@Document(collection="addMoney")
public class AddMoney {

    @Valid
    @NotNull
    @Id
    private String id;

    @Valid
    @NotNull
    private String userId;

    @Valid
    @NotNull
    private String money;

    @Valid
    @NotNull
    private AddMoneyType type;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public AddMoney(){
        this.id = UUID.randomUUID().toString();
    }

    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public String getMoney() {
        return money;
    }

    public void setMoney(String money) {
        this.money = money;
    }

    public AddMoneyType getType() {
        return type;
    }

    public void setType(AddMoneyType type) {
        this.type = type;
    }
}
