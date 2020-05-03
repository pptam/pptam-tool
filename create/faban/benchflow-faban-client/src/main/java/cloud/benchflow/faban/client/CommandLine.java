package cloud.benchflow.faban.client;

import cloud.benchflow.faban.client.configurations.FabanClientConfig;
import cloud.benchflow.faban.client.configurations.FabanClientConfigImpl;
import cloud.benchflow.faban.client.exceptions.*;
import cloud.benchflow.faban.client.responses.DeployStatus;
import cloud.benchflow.faban.client.responses.RunId;
import cloud.benchflow.faban.client.responses.RunInfo;
import cloud.benchflow.faban.client.responses.RunStatus;

import java.net.URI;
import java.net.URISyntaxException;
import java.nio.file.Path;
import java.nio.file.Paths;

public class CommandLine {
    public static void main(String[] args) throws URISyntaxException, FabanClientIOException, DeployException, JarFileNotFoundException, FabanClientBadRequestException, MalformedURIException, FabanClientHttpResponseException, BenchmarkNameNotFoundRuntimeException, EmptyHarnessResponseException, IllegalRunIdException, IllegalRunStatusException, RunIdNotFoundException, IllegalRunInfoResultException {

        String faban_master = args[0];
        String action = args[1];

        //get an instance of faban client
        FabanClientConfig fcprova = new FabanClientConfigImpl("deployer", "adminadmin", new URI(faban_master));
        FabanClient client = new FabanClient().withConfig(fcprova);

        if(action.equals("deploy")){
            String testName = args[2];
            String driver = args[3];
            String conf = args[4];

            Path bm = Paths.get(driver);

            try {
                client.deploy(bm.toFile());
                RunId RunID = client.submit(testName, testName, Paths.get(conf).toFile());
                System.out.println(RunID);
            } catch (JarFileNotFoundException | ConfigFileNotFoundException e) {
                e.printStackTrace();
            }
        } else if(action.equals("status")){
            String runId = args[2];
            RunStatus status = client.status(new RunId(runId));
            System.out.println(status.getStatus());
        } else if(action.equals("info")){
            String runId = args[2];
            RunInfo runInfo = client.runInfo(new RunId(runId));
            System.out.println(runInfo.toString());
        }

    }
}
