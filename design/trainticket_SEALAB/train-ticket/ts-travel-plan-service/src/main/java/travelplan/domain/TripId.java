package travelplan.domain;

import java.io.Serializable;

public class TripId implements Serializable{

    private TrainTypeEnum type;

    private String number;

    public TripId(){
        //Default Constructor
    }

    public TripId(String trainNumber){
        char type = trainNumber.charAt(0);
        switch(type){
            case 'G': this.type = TrainTypeEnum.G;
                break;
            case 'D': this.type = TrainTypeEnum.D;
                break;
            case 'Z': this.type = TrainTypeEnum.Z;
                break;
            case 'T': this.type = TrainTypeEnum.T;
                break;
            case 'K': this.type = TrainTypeEnum.K;
                break;
            default:break;
        }

        this.number = trainNumber.substring(1);
    }


    public TrainTypeEnum getType() {
        return type;
    }

    public void setType(TrainTypeEnum type) {
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
