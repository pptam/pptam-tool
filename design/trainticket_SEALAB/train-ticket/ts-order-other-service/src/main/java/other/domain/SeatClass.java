package other.domain;

public enum SeatClass {

    NONE        (0,"NoSeat"),
    BUSINESS    (1,"GreenSeat"),
    FIRSTCLASS  (2,"FirstClassSeat"),
    SECONDCLASS (3,"SecondClassSeat"),
    HARDSEAT    (4,"HardSeat"),
    SOFTSEAT    (5,"SoftSeat"),
    HARDBED     (6,"HardBed"),
    SOFTBED     (7,"SoftBed"),
    HIGHSOFTBED (8,"HighSoftSeat");

    private int code;
    private String name;

    SeatClass(int code, String name){
        this.code = code;
        this.name = name;
    }

    public int getCode(){
        return code;
    }

    public String getName() {
        return name;
    }

    public static String getNameByCode(int code){
        SeatClass[] seatClassSet = SeatClass.values();
        for(SeatClass seatClass : seatClassSet){
            if(seatClass.getCode() == code){
                return seatClass.getName();
            }
        }
        return seatClassSet[0].getName();
    }
}
