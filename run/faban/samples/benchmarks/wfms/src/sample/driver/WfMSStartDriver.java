

package cloud.benchflow.experiment.drivers;


@com.sun.faban.driver.FixedTime(cycleDeviation = 5, cycleTime = 1000, cycleType = com.sun.faban.driver.CycleType.THINKTIME)
@com.sun.faban.driver.BenchmarkDriver(metric = "req/s", name = "WfMSStartDriver", opsUnit = "requests", percentiles = { "25" , "50" , "75" , "90" , "95" , "99.9" }, responseTimeUnit = java.util.concurrent.TimeUnit.MICROSECONDS, threadPerScale = 1.0F)
@com.sun.faban.driver.BenchmarkDefinition(metric = "req/s", name = "[wfmsTest.1.1] ParallelStructured11FastTestWorking Workload", version = "0.1")
public class WfMSStartDriver extends cloud.benchflow.driversmaker.generation.BenchFlowDriver {
    private cloud.benchflow.experiment.drivers.WfMSStartDriver.WfMSApi plugin = null;

    public abstract class WfMSApi {
        protected java.lang.String sutEndpoint;

        protected java.lang.String deployAPI;

        protected java.util.logging.Logger logger;

        public WfMSApi(java.lang.String se, java.lang.String d) {
            sutEndpoint = se;
            deployAPI = (sutEndpoint) + d;
            logger = java.util.logging.Logger.getLogger("WfMSApi");
            logger.info(("[WfMSApi] Deploy api: " + (deployAPI)));
        }

        public abstract java.util.Map<java.lang.String, java.lang.String> deploy(java.io.File model) throws java.io.IOException;

        public abstract java.lang.String startProcessInstance(java.lang.String processDefinitionId, java.lang.String data) throws java.io.IOException;
    }

    private java.util.Map<java.lang.String, java.lang.String> modelsStartID;

    public WfMSStartDriver() throws java.lang.Exception {
        super();
        modelsStartID = new java.util.HashMap<java.lang.String, java.lang.String>();
        loadModelsInfo();
        plugin = new WfMSPlugin(sutEndpoint);
    }

    private void loadModelsInfo() {
        int numModel = java.lang.Integer.parseInt(getContextProperty("model_num"));
        for (int i = 1; i <= numModel; i++) {
            java.lang.String name = getContextProperty((("model_" + i) + "_name"));
            java.lang.String startID = getContextProperty((("model_" + i) + "_startID"));
            modelsStartID.put(name, startID);
        }
    }

    private class WfMSPlugin extends cloud.benchflow.experiment.drivers.WfMSStartDriver.WfMSApi {
        private java.util.Map<java.lang.String, java.lang.String> JSONHeaders;

        protected java.lang.String processDefinitionAPI;

        private com.google.gson.JsonParser parser;

        public WfMSPlugin(java.lang.String sutEndpoint) {
            super(sutEndpoint, "/deployment/create");
            processDefinitionAPI = sutEndpoint + "/process-definition";
            logger.info(("Process definition api: " + (processDefinitionAPI)));
            parser = new com.google.gson.JsonParser();
            JSONHeaders = new java.util.TreeMap<java.lang.String, java.lang.String>();
            JSONHeaders.put("Content-Type", "application/json");
        }

        @java.lang.Override
        public java.util.Map<java.lang.String, java.lang.String> deploy(java.io.File model) throws java.io.IOException {
            java.util.Map<java.lang.String, java.lang.String> result = new java.util.HashMap<java.lang.String, java.lang.String>();
            org.apache.commons.httpclient.methods.multipart.StringPart deploymentName = new org.apache.commons.httpclient.methods.multipart.StringPart("deployment-name", model.getName());
            java.util.List<org.apache.commons.httpclient.methods.multipart.Part> parts = new java.util.ArrayList<org.apache.commons.httpclient.methods.multipart.Part>();
            org.apache.commons.httpclient.methods.multipart.FilePart process = new org.apache.commons.httpclient.methods.multipart.FilePart("*", model);
            parts.add(deploymentName);
            parts.add(process);
            java.lang.StringBuilder deployDef = http.fetchURL(deployAPI, parts);
            com.google.gson.JsonObject deployObj = parser.parse(deployDef.toString()).getAsJsonObject();
            java.lang.String deploymentId = deployObj.get("id").getAsString();
            java.lang.StringBuilder procDef = http.fetchURL((((processDefinitionAPI) + "?deploymentId=") + deploymentId));
            java.lang.String processDefinitionResponse = procDef.toString();
            com.google.gson.JsonArray procDefArray = parser.parse(processDefinitionResponse).getAsJsonArray();
            java.lang.String processDefinitionId = procDefArray.get(0).getAsJsonObject().get("id").getAsString();
            result.put(model.getName(), processDefinitionId);
            return result;
        }

        public java.lang.String startProcessInstance(java.lang.String processDefinitionId, java.lang.String data) throws java.io.IOException {
            java.lang.String startURL = (((sutEndpoint) + "/process-definition/") + (modelsStartID.get(processDefinitionId))) + "/start";
            java.lang.StringBuilder responseStart = http.fetchURL(startURL, "{}", JSONHeaders);
            return responseStart.toString();
        }
    }

    protected void initialize() throws java.lang.Exception {
        super.initialize();
        modelsStartID = new java.util.HashMap<java.lang.String, java.lang.String>();
    }

    @com.sun.faban.driver.BenchmarkOperation(max90th = 6.0E7, name = "11ParallelStructured.bpmn", percentileLimits = { 0.0 , 0.0 , 0.0 , 6.0E7 , 0.0 , 0.0 }, timing = com.sun.faban.driver.Timing.AUTO)
    public void do11ParallelStructuredRequest() throws java.lang.Exception {
        if (isStarted())
            plugin.startProcessInstance("11ParallelStructured.bpmn", null);
        else
            plugin.startProcessInstance("mock.bpmn", null);
        
    }
}

