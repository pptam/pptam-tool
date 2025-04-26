package other.domain;

public class SeatNumber {

    char position;
    int lineNum;
    int seatNumber;
    boolean isNormalSeat;

    public SeatNumber(){
        isNormalSeat = false;
    }

    public char getPosition() {
        return position;
    }

    public void setPosition(char position) {
        this.position = position;
    }

    public int getLineNum() {
        return lineNum;
    }

    public void setLineNum(int lineNum) {
        this.lineNum = lineNum;
    }

    public int getSeatNumber() {
        return seatNumber;
    }

    public void setSeatNumber(int seatNumber) {
        this.seatNumber = seatNumber;
    }

    public boolean isNormalSeat() {
        return isNormalSeat;
    }

    public void setNormalSeat(boolean normalSeat) {
        isNormalSeat = normalSeat;
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
        SeatNumber other = (SeatNumber) obj;
        return position == other.getPosition()
                && lineNum == other.getLineNum()
                && seatNumber == other.getSeatNumber()
                && isNormalSeat == other.isNormalSeat();
    }

    @Override
    public String toString(){
        if(isNormalSeat){
            return "" + seatNumber;
        }else{
            return "" + position + lineNum;
        }
    }
}
