package other.domain;

import java.util.ArrayList;

public class QueryByIdBatchResult {

    private ArrayList<String> stationNameList;

    public QueryByIdBatchResult() {
    }

    public QueryByIdBatchResult(ArrayList<String> stationNameList) {
        this.stationNameList = stationNameList;
    }

    public ArrayList<String> getStationNameList() {
        return stationNameList;
    }

    public void setStationNameList(ArrayList<String> stationNameList) {
        this.stationNameList = stationNameList;
    }
}
