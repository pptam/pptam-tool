

package cloud.benchflow.experiment.harness;


public class WfMSBenchmark extends cloud.benchflow.driversmaker.generation.BenchFlowBenchmark {
    private cloud.benchflow.experiment.harness.WfMSBenchmark.WfMSApi plugin = null;

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

    private static java.util.logging.Logger logger = java.util.logging.Logger.getLogger(cloud.benchflow.experiment.harness.WfMSBenchmark.class.getName());

    private java.util.Map<java.lang.String, java.lang.String> modelsStartID;

    private class WfMSPlugin extends cloud.benchflow.experiment.harness.WfMSBenchmark.WfMSApi {
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

    public void initialize() throws java.lang.Exception {
        super.initialize();
        modelsStartID = new java.util.HashMap<java.lang.String, java.lang.String>();
    }

    @com.sun.faban.harness.Configure
    public void configure() throws java.lang.Exception {
        super.configure();
        cloud.benchflow.experiment.harness.WfMSBenchmark.logger.info("About to configure wfms plugin...");
        plugin = new WfMSPlugin(sutEndpoint);
    }

    public void addModel(org.w3c.dom.Element properties, int modelNum, java.lang.String modelName, java.lang.String processDefinitionId) throws java.lang.Exception {
        runXml.addProperty(properties, (("model_" + modelNum) + "_name"), modelName);
        runXml.addProperty(properties, (("model_" + modelNum) + "_startID"), processDefinitionId);
    }

    @com.sun.faban.harness.PreRun
    public void preRun() throws java.lang.Exception {
        cloud.benchflow.experiment.harness.WfMSBenchmark.logger.info("START: Deploying processes...");
        int numDeplProcesses = 0;
        java.nio.file.Path modelDir = benchmarkDir.resolve("models");
        java.io.File[] listOfModels = modelDir.toFile().listFiles();
        java.lang.String agentName = "WfMSStartDriver";
        java.lang.String driverToUpdate = ("fa:runConfig/fd:driverConfig[@name=\"" + agentName) + "\"]";
        org.w3c.dom.Element properties = ((org.w3c.dom.Element) (runXml.getNode((driverToUpdate + "/properties"))));
        if (properties == null) {
            cloud.benchflow.experiment.harness.WfMSBenchmark.logger.info("Adding properties node for driver WfMSStartDriver");
            properties = runXml.addConfigurationNode(driverToUpdate, "properties", "");
        } 
        for (int i = 0; i < (listOfModels.length); i++) {
            if (listOfModels[i].isFile()) {
                java.lang.String modelName = listOfModels[i].getName();
                java.lang.String modelPath = (modelDir + "/") + modelName;
                java.io.File modelFile = new java.io.File(modelPath);
                java.lang.String processDefinitionId = null;
                processDefinitionId = plugin.deploy(modelFile).get(modelName);
                addModel(properties, (i + 1), modelName, processDefinitionId);
                numDeplProcesses++;
                cloud.benchflow.experiment.harness.WfMSBenchmark.logger.info(("PROCESS DEFINITION ID: " + processDefinitionId));
            } 
        }
        runXml.addProperty(properties, "model_num", java.lang.String.valueOf(numDeplProcesses));
        cloud.benchflow.experiment.harness.WfMSBenchmark.logger.info("END: Deploying processes...");
    }
}

