package order.domain;

public class TrainNumber {

    private int type;
    private int number;

    public int getType() {
        return type;
    }

    public void setType(int type) {
        this.type = type;
    }

    public int getNumber() {
        return number;
    }

    public void setNumber(int number) {
        this.number = number;
    }

    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (obj == null) {
            return false;
        }
        if (getClass() != obj.getClass()) {
            return false;
        }
        TrainNumber other = (TrainNumber) obj;
        return type == other.getType() && number == other.getNumber();
    }

    @Override
    public String toString(){
        return TrainType.getNameByCode(type) + number;
    }

}
