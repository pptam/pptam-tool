package fdse.microservice.domain;

import java.io.Serializable;


public class TripId implements Serializable{
    private Type type;
    private String number;

//    public TripId(Type type, String number){
//        this.type = type;
//        this.number = number;
//    }

    public TripId(){}

    public TripId(String trainNumber){
        char type = trainNumber.charAt(0);
        switch(type){
            case 'G': this.type = Type.G;
                break;
            case 'D': this.type = Type.D;
                break;
            case 'Z': this.type = Type.Z;
                break;
            case 'T': this.type = Type.T;
                break;
            case 'K': this.type = Type.K;
                break;
            default:break;
        }

        this.number = trainNumber.substring(1);
    }


    public Type getType() {
        return type;
    }

    public void setType(Type type) {
        this.type = type;
    }

    public String getNumber() {
        return number;
    }

    public void setNumber(String number) {
        this.number = number;
    }

    @Override
    public String toString(){
        return type.getName() + number;
    }
}
