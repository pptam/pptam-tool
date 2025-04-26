package fdse.microservice.domain;

import java.util.ArrayList;

public class QueryForIdBatch {

    ArrayList<String> nameList;

    public QueryForIdBatch() {
    }

    public QueryForIdBatch(ArrayList<String> nameList) {
        this.nameList = nameList;
    }

    public ArrayList<String> getNameList() {
        return nameList;
    }

    public void setNameList(ArrayList<String> nameList) {
        this.nameList = nameList;
    }
}
