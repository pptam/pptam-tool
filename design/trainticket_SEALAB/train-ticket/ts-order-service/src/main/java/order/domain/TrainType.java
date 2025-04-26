package order.domain;

public enum TrainType {

    GAOTIE    (0,"G"),
    DONGCHE   (1,"D"),
    CHENGJI   (2,"C"),
    ZHIDA     (3,"Z"),
    TEKUAI    (4,"T"),
    KUAISU    (5,"K"),
    LINKE     (6,"L"),
    YOULAN    (7,"Y"),
    CHENGJIAO (8,"S"),
    OTHER     (9,"");

    private int code;
     private String name;

    TrainType(int code, String name){
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
        TrainType[] trainTypeSet = TrainType.values();
        for(TrainType trainType : trainTypeSet){
            if(trainType.getCode() == code){
                return trainType.getName();
            }
        }
        return trainTypeSet[0].getName();
    }
}
