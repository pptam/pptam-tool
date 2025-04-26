package travelplan.domain;

import java.io.Serializable;

public enum TrainTypeEnum implements Serializable{

    G("G", 1), D("D", 2),
    Z("Z",3), T("T", 4), K("K", 5);

    private String name;
    private int index;

    TrainTypeEnum(String name, int index) {
        this.name = name;
        this.index = index;
    }

    public static String getName(int index) {
        for (TrainTypeEnum type : TrainTypeEnum.values()) {
            if (type.getIndex() == index) {
                return type.name;
            }
        }
        return null;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getIndex() {
        return index;
    }

    public void setIndex(int index) {
        this.index = index;
    }
}
