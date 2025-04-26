package order.domain;

import java.util.ArrayList;

public class QueryByIdBatch {

    private ArrayList<String> stationIdList;

    public QueryByIdBatch() {
    }

    public QueryByIdBatch(ArrayList<String> stationIdList) {
        this.stationIdList = stationIdList;
    }

    public ArrayList<String> getStationIdList() {
        return stationIdList;
    }

    public void setStationIdList(ArrayList<String> stationIdList) {
        this.stationIdList = stationIdList;
    }
}
