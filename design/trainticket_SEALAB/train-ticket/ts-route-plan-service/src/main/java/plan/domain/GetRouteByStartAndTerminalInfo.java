package plan.domain;

public class GetRouteByStartAndTerminalInfo {

    private String startId;

    private String terminalId;

    public GetRouteByStartAndTerminalInfo() {
        //Default Constructor
    }

    public GetRouteByStartAndTerminalInfo(String startId, String terminalId) {
        this.startId = startId;
        this.terminalId = terminalId;
    }

    public String getStartId() {
        return startId;
    }

    public void setStartId(String startId) {
        this.startId = startId;
    }

    public String getTerminalId() {
        return terminalId;
    }

    public void setTerminalId(String terminalId) {
        this.terminalId = terminalId;
    }
}


