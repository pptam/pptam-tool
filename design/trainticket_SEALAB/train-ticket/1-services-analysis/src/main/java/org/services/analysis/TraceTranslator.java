package org.services.analysis;

//
//

import java.io.*;
import java.sql.Timestamp;
import java.util.*;
import java.util.stream.Collectors;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;


public class TraceTranslator {
    public static void main(String[] args) throws JSONException {

//        String path = "src/main/resources/sample/traces1.json";
//        String path = "./sample/trace-data.json";
//        String path = "./sample/traces-error-normal.json";
//        String path = "./sample/trace-error-processes-seq.json";
//        String path = "./sample/trace-error-processes-seq(chance).json";
//        String path = "./sample/trace-error-processes-seq-status.json";
//        String path = "./sample/traces-error-cross-timeout-status.json";

//        String path = "./sample/trace-error-queue-seq-multi.json";

//        String path = "./sample/trace-error-queue-seq-multi.json";
//        String path = "./sample/traces-error-cross-timeout-status.json";
//        String path = "./sample/cross-timeout/inside-payment.json";
//        String path = "./sample/cross-timeout/order.json";
//        String path = "./sample/cross-timeout/order-other.json";
//        String path = "./sample/cross-timeout/payment.json";
//          String path = "./sample/traces-error-external-normal.json";
//        String path = "./sample/traces-error-report-ui-seq.json";
//        String path = "./sample/temp-storage/inside-payment.json";
//        String path = "./sample/processes-seq-status/travel.json";
//        String path = "./sample/processes-seq-status/preserve.json";
//        String path = "./sample/cross-timeout/paying.json";
//        String path = "./sample/preserve-other.json";
//        String path = "./sample/register.json";
//        String path = "./sample/login.json";
//        String path = "./sample/contacts.json";
//        String path = "./sample/travel2.json";
//    	String path = "./ts-large-sample/error-normal/login.json";

//        String destPath = "./output/shiviz-log-error-normal.txt";
//        String destPath = "./output/shiviz-error-processes-seq.txt";
//        String destPath = "./output/shiviz-error-processes-seq(chance).txt";
//        String destPath = "./output/shiviz-error-processes-seq-status.txt";
//        String destPath = "./output/shiviz-traces-error-cross-timeout-status.txt;
//        String destPath = "./output/shiviz-ts-inside-payment.txt";
//        String destPath = "./output/shiviz-ts-order.txt";
//        String destPath = "./output/shiviz-ts-order-other.txt";
//        String destPath = "./output/shiviz-ts-payment.txt";
//          String destPath = "./output/shiviz-error-external-normal.txt";
//        String destPath = "./output/shiviz-error-report-ui-seq.txt";
//        String destPath = "./output/shiviz-error-processes-seq-status-travel.txt";
//        String destPath = "./output/shiviz-error-processes-seq-status-preserve.txt";
//        String destPath = "./output/shiviz-error-paying.txt";
//    	String destPath = "./ts-large-output/error-normal/shiviz-error-login.txt";

//        String destPath = "./output/shiviz-error-preserve-other.txt";
//        String destPath = "./output/shiviz-error-register.txt";
//        String destPath = "./output/shiviz-error-login.txt";
//        String destPath = "./output/shiviz-error-contacts.txt";
//        String destPath = "./output/shiviz-error-travel2.txt";
    	
//    	int testCaseNumber = 30;
//    	ArrayList<ArrayList<JSONArray>> finalcomb = new ArrayList<ArrayList<JSONArray>>(30);
//
//        List<File> fileLists = getListFiles("./ts-large-sample/error-normal");
//        for(int j = 0; j < 30; j++){
//        	
//        	ArrayList<JSONArray> comb = new ArrayList<JSONArray>(testCaseNumber);
//        	
//	        for(int i = 0; i < fileLists.size(); i++){
//	        	File file = fileLists.get(i);
//	        	String path1 = file.getPath();
//	        	
//	        	System.out.println(path1);
//	        	String traceStr = readFile(path1);
//	            JSONArray tracelist = new JSONArray(traceStr);
//	            
//	            int size = tracelist.length()/testCaseNumber;
//	            int index = j*size;
//	            
//	            JSONArray objs = new JSONArray();
//	            while(size-->0){
//	            	objs.put(tracelist.get(index+size));
//	            }
//	            
//	            comb.add(objs);
//	        }
//	        
//	        finalcomb.add(comb);
//        }
//        
//        
//        System.out.println(finalcomb);
        
    	
    	List<File> fileLists = getListFiles("./ts-large-sample/error-normal");
    	String destDir = "./ts-large-output/error-normal/shiviz-error-";
        for(int x = 0; x < fileLists.size(); x++){
	    	File file = fileLists.get(x);
	    	String path = file.getPath();

	        String microserviceName = path.substring(path.lastIndexOf("/")+1,path.lastIndexOf("."));
	        int testCaseNumber = 30;
	
	
	        String traceStr = readFile(path);
	
	        JSONArray tracelist = new JSONArray(traceStr);
	
	        List<HashMap<String,String>> logs = new ArrayList<HashMap<String, String>>();
	
	        HashMap<String,String> states = new HashMap<String,String>();
	
	        for (int k = 0; k < tracelist.length(); k++) {
	
	            JSONArray traceobj = tracelist.getJSONArray(k);
	
	            List<HashMap<String, String>> serviceList = new ArrayList<HashMap<String, String>>();
	            String traceId = ((JSONObject) traceobj.get(0)).getString("traceId");
	
	            for (int j = 0; j < traceobj.length(); j++) {
	                JSONObject spanobj = (JSONObject) traceobj.get(j);
	
	                // String traceId = spanobj.getString("traceId");
	                String id = spanobj.getString("id");
	                String pid = "";
	                if (spanobj.has("parentId")) {
	                    pid = spanobj.getString("parentId");
	                }
	                String name = spanobj.getString("name");
	                String time = String.valueOf(spanobj.getLong("timestamp"));
	
	                HashMap<String, String> content = new HashMap<String, String>();
	                content.put("traceId" , traceId);
	                content.put("spanid", id);
	                content.put("parentid", pid);
	                content.put("spanname", name);
	
	
	
	                //annotation
	                if(spanobj.has("annotations")) {
	                    JSONArray annotations = spanobj.getJSONArray("annotations");
	                    for (int i = 0; i < annotations.length(); i++) {
	                        JSONObject anno = annotations.getJSONObject(i);
	                        if ("cs".equals(anno.getString("value"))) {
	                            JSONObject endpoint = anno.getJSONObject("endpoint");
	                            String service = endpoint.getString("serviceName");
	                            content.put("clientName", service);
	                            String csTime = String.valueOf(anno.getLong("timestamp"));
	                            content.put("csTime", csTime);
	                        }
	                        if ("sr".equals(anno.getString("value"))) {
	                            JSONObject endpoint = anno.getJSONObject("endpoint");
	                            String service = endpoint.getString("serviceName");
	                            content.put("serverName", service);
	                            String srTime = String.valueOf(anno.getLong("timestamp"));
	                            content.put("srTime", srTime);
	                        }
	                        if ("ss".equals(anno.getString("value"))) {
	                            JSONObject endpoint = anno.getJSONObject("endpoint");
	                            String service = endpoint.getString("serviceName");
	                            content.put("serverName", service);
	                            String ssTime = String.valueOf(anno.getLong("timestamp"));
	                            content.put("ssTime", ssTime);
	                        }
	                        if ("cr".equals(anno.getString("value"))) {
	                            JSONObject endpoint = anno.getJSONObject("endpoint");
	                            String service = endpoint.getString("serviceName");
	                            content.put("clientName", service);
	                            String crTime = String.valueOf(anno.getLong("timestamp"));
	                            content.put("crTime", crTime);
	                        }
	                    }
	                }
	
	
	
	                //if annotation doesn't exist
	                if(!spanobj.has("annotations")){
	                    content.put("time",time);
	                }
	
	
	                //binaryAnnotation
	//                if (name.contains("message:")) {
	//                    if ("message:input".equals(name)) {
	//                        content.put("api", content.get("service") + "." + "message_received");
	//                    }
	//                } else {
	                JSONArray binaryAnnotations = spanobj.getJSONArray("binaryAnnotations");
	                for (int i = 0; i < binaryAnnotations.length(); i++) {
	                    JSONObject anno = binaryAnnotations.getJSONObject(i);
	                    if ("error".equals(anno.getString("key"))) {
	                        content.put("error", anno.getString("value"));
	                    }
	                    if ("mvc.controller.class".equals(anno.getString("key"))
	                            && !"BasicErrorController".equals(anno.getString("value"))) {
	                        String classname = anno.getString("value");
	                        content.put("classname", classname);
	                    }
	                    if ("mvc.controller.method".equals(anno.getString("key"))
	                            && !"errorHtml".equals(anno.getString("value"))) {
	                        String methodname = anno.getString("value");
	                        content.put("methodname", methodname);
	                    }
	                    if ("spring.instance_id".equals(anno.getString("key"))) {
	                        String instance_id = anno.getString("value");
	                        JSONObject endpoint = anno.getJSONObject("endpoint");
	                        String ipv4 = endpoint.getString("ipv4");
	//                            String port = String.valueOf(endpoint.get("port"));
	
	                        if(content.get("serverName")!=null && instance_id.indexOf(content.get("serverName")) != -1){
	                            String key = content.get("serverName") + ":" + ipv4;
	                            String new_instance_id;
	                            if(states.containsKey(key)){
	                                new_instance_id = content.get("serverName") + ":" + states.get(key);
	                            }else{
	                                new_instance_id = content.get("serverName");
	                            }
	
	                            content.put("server_instance_id", new_instance_id);
	                        }
	                        if(content.get("clientName")!=null  && instance_id.indexOf(content.get("clientName")) != -1){
	                            String key = content.get("clientName") + ":" + ipv4;
	                            String new_instance_id;
	                            if(states.containsKey(key)){
	                                new_instance_id = content.get("clientName") + ":" + states.get(key);
	                            }else{
	                                new_instance_id = content.get("clientName") ;
	                            }
	                            content.put("client_instance_id", new_instance_id);
	                        }
	                    }
	                    if ("http.method".equals(anno.getString("key"))) {
	                        String httpMethod = anno.getString("value");
	                        content.put("httpMethod", httpMethod);
	                    }
	                    if ("class".equals(anno.getString("key"))) {
	                        String c = anno.getString("value");
	                        content.put("class", c);
	                        JSONObject endpoint = anno.getJSONObject("endpoint");
	                        String ipv4 = endpoint.getString("ipv4");
	                        String port = String.valueOf(endpoint.get("port"));
	                        String serviceName = String.valueOf(endpoint.get("serviceName"));
	
	//                        String hostId = serviceName + ":" + ipv4 ;
	                        String hostId = serviceName ;
	                        content.put("hostId", hostId);
	                        content.put("serviceName", serviceName);
	
	                    }
	                    if ("method".equals(anno.getString("key"))) {
	                        String method = anno.getString("value");
	                        content.put("method", method);
	                        JSONObject endpoint = anno.getJSONObject("endpoint");
	                        String ipv4 = endpoint.getString("ipv4");
	                        String port = String.valueOf(endpoint.get("port"));
	                        String serviceName = String.valueOf(endpoint.get("serviceName"));
	
	//                        String hostId = serviceName + ":" + ipv4 ;
	                        String hostId = serviceName ;
	                        content.put("hostId", hostId);
	                        content.put("serviceName", serviceName);
	                    }
	                    if ("controller_state".equals(anno.getString("key"))) {
	                        String state = anno.getString("value");
	                        JSONObject endpoint = anno.getJSONObject("endpoint");
	                        String ipv4 = endpoint.getString("ipv4");
	                        String serviceName = String.valueOf(endpoint.get("serviceName"));
	                        content.put("state",state);
	                        content.put("ipv4State",ipv4);
	                        content.put("serviceNameState",serviceName);
	                        states.put(serviceName +":" + ipv4, state);
	                    }
	
	
	                }
	
	
	
	                if(content.get("serverName") != null && (content.get("classname") != null || content.get("methodname") != null)){
	                    content.put("api",
	                            content.get("serverName") + "." + content.get("classname") + "." + content.get("methodname"));
	                }else if(content.get("hostId") != null && (content.get("class") != null || content.get("method") != null)){
	                    content.put("api",
	                            content.get("hostId") + "." + content.get("class") + "." + content.get("method"));
	                }
	                if (name.contains("message:")) {
	                    if(content.get("serverName") != null){
	                        if ("message:input".equals(name)) {
	                            content.put("api", content.get("serverName") + "." + "message_received");
	                        }else if("message:output".equals(name)){
	                            content.put("api", content.get("serverName") + "." + "message_send");
	                        }
	                    }else if(content.get("clientName") != null){
	                        if ("message:input".equals(name)) {
	                            content.put("api", content.get("clientName") + "." + "message_received");
	                        }else if("message:output".equals(name)){
	                            content.put("api", content.get("clientName") + "." + "message_send");
	                        }
	                    }
	                }
	
	
	                serviceList.add(content);
	            }
	
	
	
	
	            // filter validate service api
	//            List<HashMap<String, String>> processList = serviceList.stream()
	//                    .filter(elem -> !"message:output".equals(elem.get("spanname"))).collect(Collectors.toList());
	//            boolean failed = processList.stream().anyMatch(pl -> pl.containsKey("error"));
	
	            serviceList.forEach(n -> {
	
	                if(n.get("csTime") != null){
	                    HashMap<String,String> log = new HashMap<String,String>();
	                    log.put("traceId" , n.get("traceId"));
	                    log.put("spanId" , n.get("spanid"));
	                    log.put("parentId" , n.get("parentid"));
	                    log.put("timestamp",n.get("csTime"));
	                    log.put("hostName" , n.get("clientName"));
	                    log.put("host" , n.get("client_instance_id"));
	                    log.put("destName" , n.get("serverName"));
	                    log.put("dest" , n.get("server_instance_id"));
	                    log.put("api", n.get("api"));
	                    log.put("spanname",n.get("spanname"));
	
	                    if(n.get("spanname").contains("message:")){
	                        log.put("event" , n.get("api"));
	                        log.put("queue","queue");
	                    }else{
	                        log.put("event" , "");
	                    }
	
	                    log.put("type", "cs");
	                    if(null != n.get("api")){
	                        log.put("api", n.get("api"));
	                    }
	                    if(n.containsKey("error")){
	                        log.put("error", n.get("error"));
	                    }
	                    logs.add(log);
	                }
	                if(n.get("srTime") != null){
	                    HashMap<String,String> log = new HashMap<String,String>();
	                    log.put("traceId" , n.get("traceId"));
	                    log.put("spanId" , n.get("spanid"));
	                    log.put("parentId" , n.get("parentid"));
	                    log.put("timestamp",n.get("srTime"));
	                    log.put("hostName" , n.get("serverName"));
	                    log.put("host" , n.get("server_instance_id"));
	                    log.put("srcName" , n.get("clientName"));
	                    log.put("src" , n.get("client_instance_id"));
	                    log.put("api", n.get("api"));
	                    log.put("spanname",n.get("spanname"));
	                    log.put("event", n.get("api"));
	                    log.put("type", "sr");
	                    if(n.containsKey("error")){
	                        log.put("error", n.get("error"));
	                    }
	                    if(n.get("spanname").contains("message:")){
	                        log.put("queue","queue");
	                    }
	                    logs.add(log);
	                }
	                if(n.get("ssTime") != null){
	                    HashMap<String,String> log = new HashMap<String,String>();
	                    log.put("traceId" , n.get("traceId"));
	                    log.put("spanId" , n.get("spanid"));
	                    log.put("parentId" , n.get("parentid"));
	                    log.put("timestamp",n.get("ssTime"));
	                    log.put("hostName" , n.get("serverName"));
	                    log.put("host" , n.get("server_instance_id"));
	                    log.put("destName" , n.get("clientName"));
	                    log.put("dest" , n.get("client_instance_id"));
	                    log.put("api", n.get("api"));
	                    log.put("spanname",n.get("spanname"));
	
	                    log.put("event", n.get("api"));
	                    log.put("type", "ss");
	                    if(n.containsKey("error")){
	                        log.put("error", n.get("error"));
	                    }
	                    if(n.get("spanname").contains("message:")){
	                        log.put("queue","queue");
	                    }
	                    logs.add(log);
	                }
	                if(n.get("crTime") != null){
	                    HashMap<String,String> log = new HashMap<String,String>();
	                    log.put("traceId" , n.get("traceId"));
	                    log.put("spanId" , n.get("spanid"));
	                    log.put("parentId" , n.get("parentid"));
	                    log.put("timestamp",n.get("crTime"));
	                    log.put("hostName" , n.get("clientName"));
	                    log.put("host" , n.get("client_instance_id"));
	                    log.put("srcName" , n.get("serverName"));
	                    log.put("src" , n.get("server_instance_id"));
	                    log.put("api", n.get("api"));
	                    log.put("spanname",n.get("spanname"));
	
	                    if(n.get("spanname").contains("message:")){
	                        log.put("event" , n.get("api"));
	                        log.put("queue","queue");
	
	                    }else{
	                        log.put("event" , "");
	                    }
	
	                    log.put("type", "cr");
	                    if(n.containsKey("error")){
	                        log.put("error", n.get("error"));
	                    }
	                    logs.add(log);
	                }
	                if(n.get("time") != null){
	                    HashMap<String,String> log = new HashMap<String,String>();
	                    log.put("traceId" , n.get("traceId"));
	                    log.put("spanId" , n.get("spanid"));
	                    log.put("parentId" , n.get("parentid"));
	                    log.put("timestamp",n.get("time"));
	                    log.put("hostName" , n.get("serviceName"));
	                    log.put("host" , n.get("hostId"));
	                    log.put("api", n.get("api"));
	                    log.put("spanname",n.get("spanname"));
	                    log.put("event", n.get("api"));
	                    log.put("type", "async");
	                    if(n.containsKey("error")){
	                        log.put("error", n.get("error"));
	                    }
	                    if(n.get("spanname").contains("message:")){
	                        log.put("queue","queue");
	                    }
	                    logs.add(log);
	                }
	
	
	            });
	
	        }
	
	
	
	//        writeFile("./sample/trace-data-shiviz.txt", list);
	        HashMap<String,String> traceIds = new HashMap<String,String>();
	        logs.forEach(n -> {
	            if(!traceIds.containsKey(n.get("traceId"))){
	                traceIds.put(n.get("traceId"),"");
	            }
	        });
	
	        List<List<HashMap<String,String>>> list = new ArrayList<List<HashMap<String,String>>>();
	        HashMap<List<HashMap<String,String>>, Boolean> failures = new HashMap<List<HashMap<String,String>>, Boolean>();
	        traceIds.forEach((n,s) -> {
	            List l = logs.stream().filter(elem -> {
	                return n.equals(elem.get("traceId"));
	            }).collect(Collectors.toList());
	//            List<HashMap<String,String>> listWithClock = clock(l);
	            List<HashMap<String,String>> listWithClock = clock2(l);
	
	            boolean failed = listWithClock.stream().anyMatch(pl -> pl.containsKey("error"));
	            failures.put(listWithClock,failed);
	            list.add(listWithClock);
	        });
	
	        //(elem -> !"message:output".equals(elem.get("spanname"))).collect(Collectors.toList());
	//        List<HashMap<String,String>> list = clock(logs);
	//        writeFile("./output/shiviz-log-error-normal.txt", list, failures);
	//        writeFile("./output/shiviz-error-processes-seq.txt", list, failures);
	//        writeFile("./output/shiviz-error-processes-seq(chance).txt", list, failures);
	//        writeFile("./output/shiviz-error-processes-seq-status.txt", list, failures);
	//        writeFile("./output/shiviz-traces-error-cross-timeout-status.txt", list, failures);
	
	//        writeFile("./output/shiviz-error-queue-seq-multi.txt", list, failures);
	
	
	
	        List<List<HashMap<String,String>>> listSorted = sortListByTime(list);
	        listSorted.forEach(n -> {
	            System.out.println("event number:" + n.size());
	        });
//	        writeFile(destPath, listSorted, failures, microserviceName, testCaseNumber);
	        
	        writeFile(destDir+file.getName()+".txt", listSorted, failures, microserviceName, testCaseNumber);

        }
//        });



    }



    private static ArrayList<File> getListFiles(Object obj) {
        File directory = null;
        if (obj instanceof File) {
            directory = (File) obj;
        } else {
            directory = new File(obj.toString());
        }
        ArrayList<File> files = new ArrayList<File>();
        if (directory.isFile()) {
            files.add(directory);
            return files;
        } else if (directory.isDirectory()) {
            File[] fileArr = directory.listFiles();
            for (int i = 0; i < fileArr.length; i++) {
                File fileOne = fileArr[i];
                if(fileOne.getName().endsWith(".json")){
                	files.addAll(getListFiles(fileOne));
                }
            }
        }
        return files;
    }

    private static List<List<HashMap<String,String>>> sortListByTime(List<List<HashMap<String,String>>> list){
        List<List<HashMap<String,String>>> result = new ArrayList<List<HashMap<String,String>>>();
        Iterator<List<HashMap<String,String>>> iterator = list.iterator();
        List<HashMap<String,String>> logs;
        HashMap<String, String> log;
        HashMap<String, String> times = new HashMap<String, String>();
        HashMap<String, List<HashMap<String,String>>> traceIdAndList = new HashMap<String, List<HashMap<String,String>>>();

        while(iterator.hasNext()){
            logs = iterator.next();

            log = logs.get(0);
            String traceId = log.get("traceId");
            traceIdAndList.put(traceId, logs);
            for (HashMap<String, String> stringStringHashMap : logs) {
                if(stringStringHashMap.get("spanId").equals(traceId)){
                    times.put(stringStringHashMap.get("timestamp"), traceId);
                    break;
                }
            }

//            if(!times.containsKey(traceId)){
//                for (HashMap<String, String> stringStringHashMap : logs) {
//                    if(stringStringHashMap.get("parentId").equals(traceId)){
//                        times.put(stringStringHashMap.get("timestamp"), traceId);
//                        break;
//                    }
//                }
//            }
        }

        Long[] timestamps = new Long[times.size()];
        Iterator<String> iterator1 = times.keySet().iterator();
        for(int i=0; i< timestamps.length; i++){
            timestamps[i] = Long.valueOf(iterator1.next());
        }
        Arrays.sort(timestamps);

        for(int i=0; i< timestamps.length; i++){
            String traceId1 = times.get(String.valueOf(timestamps[i]));
            result.add(traceIdAndList.get(traceId1));
        }

        return result;
    }


    public static HashMap<String,Integer> findSrcClock(List<Clock> allClocks, String traceId, String spanId, String type, String queue, String parentId){
        HashMap<String,Integer> clock = null;
        Clock item;

        for(int i= allClocks.size() - 1; i >= 0 ; i--){
            item = allClocks.get(i);
            if(item.isSrc(traceId, spanId, type, queue, parentId)){
                clock = item.getClock();
                break;
            }
        }

        if(clock == null){
            System.out.println();
        }

        return (HashMap<String,Integer>)clock.clone();
    }



    //sort the log for one trace according to the calling sequences
    public static List<HashMap<String,String>> sortLog(List<HashMap<String,String>> logs){
//        List<HashMap<String,String>> list = logs.stream().sorted((log1,log2) -> {
//            Long time1 = Long.valueOf(log1.get("timestamp"));
//            Long time2 = Long.valueOf(log2.get("timestamp"));
//            return time1.compareTo(time2);
//        }).collect(Collectors.toList());
        List<HashMap<String,String>> list = null ;

        HashMap<String,String> log = logs.get(0);
        String traceId = log.get("traceId");

        HashMap<String, Span> spans = new HashMap<String, Span>();
        HashMap<String,List<String>> spanRelation = new HashMap<String, List<String>>();
        logs.forEach(n -> {
            String spanId = n.get("spanId");
            if(spans.containsKey(spanId)){
                Span span = spans.get(spanId);
                span.addLog(n);
            }else{
                Span span = new Span(n.get("traceId"), n.get("spanId"), n.get("parentId"), n.get("spanname"));
                span.addLog(n);
                spans.put(spanId,span);
            }

            if(spanRelation.containsKey(n.get("parentId"))){
                List<String> childs = spanRelation.get(n.get("parentId"));
                if(!childs.contains(spanId)){
                    childs.add(spanId);
                }
            }else{
                List<String> childs = new ArrayList<String>();
                childs.add(spanId);
                spanRelation.put(n.get("parentId"),childs);
            }
        });

        //add the event for cs & cr
        HashMap<String,String> apis = new HashMap<String, String>();
        logs.forEach(n -> {
            String api = n.get("api");
            apis.put(n.get("spanId"), n.get("api"));
        });
        logs.forEach(n -> {
            if("cs".equals(n.get("type")) || "cr".equals(n.get("type"))){
                if("".equals(n.get("event"))){
                    n.put("event", apis.get(n.get("parentId")));
                }
            }else if("sr".equals(n.get("type")) || "ss".equals(n.get("type"))){
                n.put("event", n.get("api"));
            }else if("async".equals(n.get("type"))){
                n.put("event", n.get("api"));
            }
            n.remove("api");
        });

        List<HashMap<String,String>> forwardLogs = new ArrayList<HashMap<String,String>>();
        List<HashMap<String,String>> backwardLogs = new ArrayList<HashMap<String,String>>();
        List<Span> sortedSpan = new ArrayList<Span>();

        Span entrance = spans.get(traceId);

        if(entrance == null){
            Iterator<Map.Entry<String, Span>> entries = spans.entrySet().iterator();
            while(entries.hasNext()){
                Map.Entry<String, Span> entry = entries.next();
                Span span = entry.getValue();
                if(traceId.equals(span.getParentId())){
                    entrance = span;
                    break;
                }
            }
        }

        setChilds(spanRelation,entrance,spans);

        traverse(entrance, forwardLogs, backwardLogs, spans);

        forwardLogs = mergeForwardAndBackwardLogs(forwardLogs, backwardLogs);

        forwardLogs.forEach(n -> {
            n.remove("spanname");
        });

        return forwardLogs;
    }

    public static void setChilds(HashMap<String,List<String>> spanRelation, Span entrance, HashMap<String, Span> spans){
        Span s = entrance;

        //Queue,add the src and srcName for queue receive(sr),dest& destName for queue send(cs)
        if("message:input".equals(s.getSpanname())){
            Span parent = spans.get(s.getParentId());
            HashMap<String,String> parentCs = null;
            HashMap<String,String> sr = null;

            Iterator<HashMap<String,String>> parentIterator = parent.getLogs().iterator();
            while(parentIterator.hasNext()){
                HashMap<String,String> log = parentIterator.next();
                if("cs".equals(log.get("type"))){
                    parentCs = log;
                    break;
                }
            }

            Iterator<HashMap<String,String>> sIterator = s.getLogs().iterator();
            while(sIterator.hasNext()){
                HashMap<String,String> log = sIterator.next();
                if("sr".equals(log.get("type"))){
                    sr = log;
                    break;
                }
            }

            if(sr != null && parentCs != null){
                sr.put("src",parentCs.get("host"));
                sr.put("srcName",parentCs.get("hostName"));
                parentCs.put("dest",sr.get("host"));
                parentCs.put("destName",sr.get("hostName"));
            }else{
                System.out.println(sr);
                System.out.println(parentCs);
            }

        }

        if(spanRelation.containsKey(s.getSpanId())){
            s.setChilds(spanRelation.get(s.getSpanId()));

            Iterator<String> iterator = s.getChilds().iterator();
            while(iterator.hasNext()){
                String childId = iterator.next();
                s = spans.get(childId);
                setChilds(spanRelation,s,spans);
            }
        }
    }

    public static void traverse(Span entrance, List<HashMap<String,String>> forwardLogs, List<HashMap<String,String>> backwardLogs, HashMap<String, Span> spans){
        //from the entrance to end
        Span s = entrance;

        HashMap<String,String> cs = null;
        HashMap<String,String> sr = null;
        HashMap<String,String> ss = null;
        HashMap<String,String> cr = null;
        HashMap<String,String> async = null;

        Iterator<HashMap<String,String>> iterator = s.getLogs().iterator();
        while(iterator.hasNext()){
            HashMap<String,String> log1 = iterator.next();
            if("cs".equals(log1.get("type"))){
                cs = log1;
            }
            if("sr".equals(log1.get("type"))){
                sr = log1;
            }
            if("ss".equals(log1.get("type"))){
                ss = log1;
            }
            if("cr".equals(log1.get("type"))){
                cr = log1;
            }
            if("async".equals(log1.get("type"))){
                async = log1;
            }
        }

        if(cs != null){
            forwardLogs.add(cs);
        }
        if(sr != null){
            forwardLogs.add(sr);
        }
        if(async != null){
            forwardLogs.add(async);
        }
        if(cr != null){
            backwardLogs.add(cr);
        }
        if(ss != null){
            backwardLogs.add(ss);
        }



        if(s.getChilds() != null){
            List<String> sortedChilds = s.getChilds().stream().sorted((spanId1,spanId2) -> {
                Span span1 = spans.get(spanId1);
                Span span2 = spans.get(spanId2);

                HashMap<String,String> sr1 = null;
                HashMap<String,String> sr2 = null;

                Iterator<HashMap<String,String>> ite1 = span1.getLogs().iterator();
                while(ite1.hasNext()){
                    HashMap<String,String> log1 = ite1.next();
                    if("cs".equals(log1.get("type"))){
                        sr1 = log1;
                    }else if("sr".equals(log1.get("type"))){
                        sr1 = log1;
                    }else if("async".equals(log1.get("type"))){
                        sr1 = log1;
                    }
                }

                Iterator<HashMap<String,String>> ite2 = span2.getLogs().iterator();
                while(ite2.hasNext()){
                    HashMap<String,String> log2 = ite2.next();
                    if("cs".equals(log2.get("type"))){
                        sr2 = log2;
                    }else if("sr".equals(log2.get("type"))){
                        sr2 = log2;
                    }else if("async".equals(log2.get("type"))){
                        sr2 = log2;
                    }
                }

//                System.out.println("sr1:"+sr1.get("timestamp"));
//                System.out.println("sr2:"+sr2.get("timestamp"));
                Long time1 = Long.valueOf(sr1.get("timestamp"));
                Long time2 = Long.valueOf(sr2.get("timestamp"));
                return time1.compareTo(time2);
            }).collect(Collectors.toList());

//            Iterator<String> iterator1 = sortedChilds.iterator();
//            List<HashMap<String,String>> childsLogs = new ArrayList<HashMap<String,String>>();
//
//            while(iterator1.hasNext()){
//                List<HashMap<String,String>> childForwardLogs = new ArrayList<HashMap<String,String>>();
//                List<HashMap<String,String>> childBackwardLogs = new ArrayList<HashMap<String,String>>();
//                String childId = iterator1.next();
//                traverse(spans.get(childId), childForwardLogs, childBackwardLogs, spans);
//                childsLogs.addAll(mergeForwardAndBackwardLogs(childForwardLogs,childBackwardLogs));
//            }
//            forwardLogs.addAll(childsLogs);
            Iterator<String> iterator1 = sortedChilds.iterator();
            List<List<HashMap<String,String>>> childLogLists = new ArrayList<List<HashMap<String,String>>>();

            while(iterator1.hasNext()){
                List<HashMap<String,String>> childForwardLogs = new ArrayList<HashMap<String,String>>();
                List<HashMap<String,String>> childBackwardLogs = new ArrayList<HashMap<String,String>>();
                String childId = iterator1.next();
                traverse(spans.get(childId), childForwardLogs, childBackwardLogs, spans);
                childLogLists.add(mergeForwardAndBackwardLogs(childForwardLogs,childBackwardLogs));
            }

            List<HashMap<String,String>> childsLogs = mergeChildLogLists(childLogLists);

            forwardLogs.addAll(childsLogs);
        }


    }

    private static List<HashMap<String,String>> mergeChildLogLists(List<List<HashMap<String,String>>> childLogLists){
        List<HashMap<String,String>> childsLogs = new ArrayList<HashMap<String,String>>();
        List<HashMap<String, String>> logs;
        List<HashMap<String,String>> childLogList;
        HashMap<String, String> earlist;

        while(!childLogLists.isEmpty()){
            logs = new ArrayList<HashMap<String,String>>();

            for(int i=0, size = childLogLists.size(); i<size; i++){
                childLogList = childLogLists.get(i);
                if(!childLogList.isEmpty()){
                    logs.add(childLogList.get(0));
                }
            }

            earlist = findEarliest(logs, childLogLists);
            childsLogs.add(earlist);

            for(int i=0, length = logs.size(); i<length; i++){
                if(earlist == logs.get(i)){
                    childLogList = childLogLists.get(i);
                    childLogList.remove(0);
                    if(childLogList.isEmpty()){
                        childLogLists.remove(childLogList);
                    }
                }
            }
        }

        return childsLogs;
    }

    private static HashMap<String, String> findEarliest(List<HashMap<String, String>> logs, List<List<HashMap<String, String>>> logLists){

        HashMap<String, String> earlist = logs.get(0);
        List<HashMap<String, String>> logListEarlist = logLists.get(0);

        Iterator<HashMap<String, String>> iterator1 = logs.iterator();
        Iterator<List<HashMap<String, String>>> iterator2 = logLists.iterator();
        while(iterator1.hasNext() && iterator2.hasNext()){
            HashMap<String, String> log = iterator1.next();
            List<HashMap<String, String>> logList = iterator2.next();
            if(compareLog(log, earlist, logList, logListEarlist)){
                earlist = log;
                logListEarlist = logList;
            }
        }

        return earlist;
    }


    private static boolean compareLog(HashMap<String, String> log1, HashMap<String, String> log2, List<HashMap<String, String>> logs1, List<HashMap<String, String>> logs2){
        long timestamp1 = Long.valueOf(log1.get("timestamp"));
        long timestamp2 = Long.valueOf(log2.get("timestamp"));
        String host1 = log1.get("host");
        String host2 = log2.get("host");

        if(host1.equals(host2)){
            if(timestamp1 <= timestamp2){
                return true;
            }else{
                return false;
            }
        }else{
            Iterator<HashMap<String, String>> iterator1 = logs1.iterator();
            Iterator<HashMap<String, String>> iterator2 = logs2.iterator();
            HashMap<String, String> log3 = null;
            HashMap<String, String> log4 = null;

            //log1 before log3, log3 before log2, then log1 before log2
            while(iterator1.hasNext()){
                log3 = iterator1.next();
                if(host2.equals(log3.get("host"))){
                    break;
                }
            }

            if(log3 != null){
                long timestamp = Long.valueOf(log3.get("timestamp"));
                if(timestamp <= timestamp2){
                    return true;
                }
            }

            //log2 before log4, log4 before log1, then log2 before log1
            while(iterator2.hasNext()){
                log4 = iterator2.next();
                if(host1.equals(log4.get("host"))){
                    break;
                }
            }

            if(log4 != null){
                long timestamp = Long.valueOf(log4.get("timestamp"));
                if(timestamp <= timestamp1){
                    return false;
                }
            }

            //still can't compare, then just compare timestamp, maybe wrong
            //but 1->2 or 2->1 both are meaningful
            if(timestamp1 <= timestamp2){
                return true;
            }else{
                return false;
            }
        }
    }


    public static List<HashMap<String,String>> mergeForwardAndBackwardLogs(List<HashMap<String,String>> forwardLogs, List<HashMap<String,String>> backwardLogs){
        Stack<HashMap<String,String>> stack = new Stack<HashMap<String,String>>();
        backwardLogs.forEach(n ->{
            stack.push(n);
        });

        while(!stack.isEmpty()){
            forwardLogs.add(stack.pop());
        }

        return forwardLogs;
    }

    public static List<HashMap<String,String>> clock2(List<HashMap<String,String>> logs){
        HashMap<String,HashMap<String,Integer>> clocks = new HashMap<String,HashMap<String,Integer>>();
        List<Clock> allClocks = new ArrayList<Clock>();

        List<HashMap<String,String>> list = sortLog(logs);

        list.forEach(n -> {
            if(clocks.containsKey(n.get("host"))){
                HashMap<String,Integer> clock = clocks.get(n.get("host"));

                if(n.get("src") != null){
                    HashMap<String,Integer> srcClock = findSrcClock(allClocks, n.get("traceId"), n.get("spanId"), n.get("type"), n.get("queue"), n.get("parentId"));

                    Iterator<Map.Entry<String,Integer>> iterator = srcClock.entrySet().iterator();
                    while (iterator.hasNext()) {
                        Map.Entry<String, Integer> entry = iterator.next();
                        if(clock.get(entry.getKey()) != null){
                            if(entry.getValue() <= clock.get(entry.getKey())){
                                //don't change clock
                            }else{  //update clock
                                clock.put(entry.getKey(),entry.getValue());
                            }
                        }else{   //update clock
                            clock.put(entry.getKey(),entry.getValue());
                        }
                    }

                    clock.put(n.get("host"),clock.get(n.get("host")) +1);

                }else{
                    clock.put(n.get("host"),clock.get(n.get("host")) +1);
                }
                n.put("clock",clock.toString());

                clocks.put(n.get("host"), clock);
                allClocks.add(new Clock(n.get("type"), n.get("host"), n.get("src"), n.get("traceId"), n.get("spanId"), n.get("parentId"), (HashMap<String,Integer>)clock.clone()));
            }else{
                HashMap<String,Integer> clock = new HashMap<String,Integer>();

                if(n.get("src") != null){
                    HashMap<String,Integer> srcClock = findSrcClock(allClocks, n.get("traceId"), n.get("spanId"), n.get("type"), n.get("queue"), n.get("parentId"));

                    Iterator<Map.Entry<String,Integer>> iterator = srcClock.entrySet().iterator();
                    while (iterator.hasNext()) {
                        Map.Entry<String, Integer> entry = iterator.next();
                        if(clock.get(entry.getKey()) != null){
                            if(entry.getValue() <= clock.get(entry.getKey())){
                                //don't change clock
                            }else{  //update clock
                                clock.put(entry.getKey(),entry.getValue());
                            }
                        }else{   //update clock
                            clock.put(entry.getKey(),entry.getValue());
                        }
                    }
                    clock.put(n.get("host"),1);
                }else{
                    clock.put(n.get("host"),1);
                }
                n.put("clock",clock.toString());

                clocks.put(n.get("host"), clock);
                allClocks.add(new Clock(n.get("type"), n.get("host"), n.get("src"), n.get("traceId"), n.get("spanId"), n.get("parentId"), (HashMap<String,Integer>)clock.clone()));
            }
        });

        list.forEach(n -> {
            if(n.containsKey("queue")){
                n.remove("queue");
            }
        });

        return list;
    }

    public static List<HashMap<String,String>> clock(List<HashMap<String,String>> logs){
        HashMap<String,HashMap<String,Integer>> clocks = new HashMap<String,HashMap<String,Integer>>();

        List<HashMap<String,String>> list = logs.stream().sorted((log1,log2) -> {
            Long time1 = Long.valueOf(log1.get("timestamp"));
            Long time2 = Long.valueOf(log2.get("timestamp"));
            return time1.compareTo(time2);
        }).collect(Collectors.toList());

        list.forEach(n -> {
            if(clocks.containsKey(n.get("host"))){
                HashMap<String,Integer> clock = clocks.get(n.get("host"));

                if(n.get("src") != null){
                    HashMap<String,Integer> srcClock = (HashMap<String,Integer>)clocks.get(n.get("src")).clone();

                    Iterator<Map.Entry<String,Integer>> iterator = srcClock.entrySet().iterator();
                    while (iterator.hasNext()) {
                        Map.Entry<String, Integer> entry = iterator.next();
                        if(clock.get(entry.getKey()) != null){
                            if(entry.getValue() <= clock.get(entry.getKey())){
                                //don't change clock
                            }else{  //update clock
                                clock.put(entry.getKey(),entry.getValue());
                            }
                        }else{   //update clock
                            clock.put(entry.getKey(),entry.getValue());
                        }
                    }

                    clock.put(n.get("host"),clock.get(n.get("host")) +1);

                }else{
                    clock.put(n.get("host"),clock.get(n.get("host")) +1);
                }
                n.put("clock",clock.toString());
                clocks.put(n.get("host"), clock);
            }else{
                HashMap<String,Integer> clock = new HashMap<String,Integer>();

                if(n.get("src") != null){
                    HashMap<String,Integer> srcClock = (HashMap<String,Integer>)clocks.get(n.get("src")).clone();

                    Iterator<Map.Entry<String,Integer>> iterator = srcClock.entrySet().iterator();
                    while (iterator.hasNext()) {
                        Map.Entry<String, Integer> entry = iterator.next();
                        if(clock.get(entry.getKey()) != null){
                            if(entry.getValue() <= clock.get(entry.getKey())){
                                //don't change clock
                            }else{  //update clock
                                clock.put(entry.getKey(),entry.getValue());
                            }
                        }else{   //update clock
                            clock.put(entry.getKey(),entry.getValue());
                        }
                    }
                    clock.put(n.get("host"),1);
                }else{
                    clock.put(n.get("host"),1);
                }
                n.put("clock",clock.toString());
                clocks.put(n.get("host"), clock);
            }
        });

        return list;
    }


    public static String readFile(String path) {
        File file = new File(path);
        BufferedReader reader = null;
        String laststr = "";
        try {
            reader = new BufferedReader(new FileReader(file));
            String tempString = null;
            while ((tempString = reader.readLine()) != null) {
                laststr = laststr + tempString;
//                System.out.println("reading");
            }
            reader.close();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (reader != null) {
                try {
                    reader.close();
                } catch (IOException e1) {
                }
            }
        }
        return laststr;
    }

    public static boolean write(String path, List<HashMap<String,String>> logs){
        File writer = new File(path);
        BufferedWriter out = null;
        try{
            writer.createNewFile(); // 鍒涘缓鏂版枃浠?
            out = new BufferedWriter(new FileWriter(writer));
            Iterator<HashMap<String,String>> iterator = logs.iterator();
            while(iterator.hasNext()){
                HashMap<String,String> map = iterator.next();
                out.write(map.toString() + "\r\n");
            }
        }catch(IOException e){
            e.printStackTrace();
            return false;
        }finally{
            if (out != null) {
                try {
                    out.flush();
                    out.close();
                } catch (IOException e1) {
                }
            }
        }

        return true;
    }


//    public static boolean writeFile(String path, List<HashMap<String,String>> logs){
//        File writer = new File(path);
//        BufferedWriter out = null;
//        try{
//            writer.createNewFile(); // 鍒涘缓鏂版枃浠?
//            out = new BufferedWriter(new FileWriter(writer));
//            Iterator<HashMap<String,String>> iterator = logs.iterator();
//            while(iterator.hasNext()){
//                HashMap<String,String> map = iterator.next();
//                Iterator<Map.Entry<String, String>> entries = map.entrySet().iterator();
//                out.write("{");
//                while (entries.hasNext()) {
//                    Map.Entry<String, String> entry = entries.next();
//                    if(entry.getKey().equals("clock")){
//                        String clocks = entry.getValue();
//                        String[] c = clocks.split(",");
//                        out.write("clock={");
//                        for(int i=0,length=c.length; i<length; i++){
//                            c[i] = "\"" + c[i].substring(1,c[i].indexOf("=")) + "\":"
//                                    + c[i].substring(c[i].indexOf("=")+1);
//                            if(i < length-1){
//                                out.write(c[i] + ",");
//                            }else{
//                                out.write(c[i]);
//                            }
//
//                        }
//                        out.write(", ");
//
//                    }else{
//                        out.write(entry.toString() + ", ");
//                    }
//                }
//
//                out.write("}\r\n");
//            }
//        }catch(IOException e){
//            e.printStackTrace();
//            return false;
//        }finally{
//            if (out != null) {
//                try {
//                    out.flush();
//                    out.close();
//                } catch (IOException e1) {
//                }
//            }
//        }
//
//        return true;
//    }

//    public static boolean writeFile(String path, List<List<HashMap<String,String>>> logs, HashMap<List<HashMap<String,String>>, Boolean> failures){
//        File writer = new File(path);
//        BufferedWriter out = null;
//        try{
//            writer.createNewFile(); // 鍒涘缓鏂版枃浠?
//            out = new BufferedWriter(new FileWriter(writer));
//            int fail = 0;
//            int success = 0;
//
//            Iterator<List<HashMap<String,String>>> iterator1 = logs.iterator();
//            while(iterator1.hasNext()){
//                List<HashMap<String,String>> list = iterator1.next();
//
//                boolean failed = failures.get(list);
//                if(failed){
//                    out.write("\r\n=== Fail execution " + (fail++) + " ===\r\n");
//                }else{
//                    out.write("\r\n=== Success execution " + (success++) + " ===\r\n");
//                }
//
//                Iterator<HashMap<String,String>> iterator = list.iterator();
//                while(iterator.hasNext()){
//                    HashMap<String,String> map = iterator.next();
//                    Iterator<Map.Entry<String, String>> entries = map.entrySet().iterator();
//                    out.write("{");
//                    while (entries.hasNext()) {
//                        Map.Entry<String, String> entry = entries.next();
//                        if(entry.getKey().equals("clock")){
//                            String clocks = entry.getValue();
//                            String[] c = clocks.split(",");
//                            out.write("clock={");
//                            for(int i=0,length=c.length; i<length; i++){
//                                c[i] = "\"" + c[i].substring(1,c[i].lastIndexOf("=")) + "\":"
//                                        + c[i].substring(c[i].lastIndexOf("=")+1);
//                                if(i < length-1){
//                                    out.write(c[i] + ",");
//                                }else{
//                                    out.write(c[i]);
//                                }
//
//                            }
//                            out.write(", ");
//
//                        }else{
//                            out.write(entry.toString() + ", ");
//                        }
//                    }
//
//                    out.write("}\r\n");
//                }
//            }
//
//
//
//        }catch(IOException e){
//            e.printStackTrace();
//            return false;
//        }finally{
//            if (out != null) {
//                try {
//                    out.flush();
//                    out.close();
//                } catch (IOException e1) {
//                }
//            }
//        }
//
//        return true;
//    }

    public static boolean writeFile(String path, List<List<HashMap<String,String>>> logs, HashMap<List<HashMap<String,String>>, Boolean> failures, String microserviceName, int testCaseNumber){
        File writer = new File(path);
        BufferedWriter out = null;
        try{
            writer.createNewFile();
            out = new BufferedWriter(new FileWriter(writer));
            int fail = 0;
            int success = 0;
            int testCase = 0;

            int dividend = logs.size()/testCaseNumber;
            if(dividend == 0){
                dividend = 1;
            }
            System.out.println("dividend:" + dividend);

            Iterator<List<HashMap<String,String>>> iterator1 = logs.iterator();
            while(iterator1.hasNext()){
                List<HashMap<String,String>> list = iterator1.next();

                boolean failed = failures.get(list);
                if(failed){
                    out.write("\r\n=== " + "TestCase" + ((testCase++)/dividend) + " " + microserviceName + " Fail execution " + (fail++) + " ===\r\n");
                }else{
                    out.write("\r\n=== " + "TestCase" + ((testCase++)/dividend) + " " + microserviceName + " Success execution " + (success++) + " ===\r\n");
                }

                Iterator<HashMap<String,String>> iterator = list.iterator();
                while(iterator.hasNext()){
                    HashMap<String,String> map = iterator.next();
                    out.write("{");


                    if(map.containsKey("traceId")){
                        out.write("traceId="+ map.get("traceId") + ", ");
                    }
                    if(map.containsKey("spanId")){
                        out.write("spanId="+ map.get("spanId") + ", ");
                    }
                    if(map.containsKey("hostName")){
                        out.write("hostName="+ map.get("hostName") + ", ");
                    }
                    if(map.containsKey("srcName")){
                        out.write("srcName="+ map.get("srcName") + ", ");
                    }
                    if(map.containsKey("destName")){
                        out.write("destName="+ map.get("destName") + ", ");
                    }
                    if(map.containsKey("src")){
                        out.write("src="+ map.get("src") + ", ");
                    }
                    if(map.containsKey("host")){
                        out.write("host="+ map.get("host") + ", ");
                    }
                    if(map.containsKey("api")){
                        out.write("api="+ map.get("api") + ", ");
                    }
                    if(map.containsKey("clock")){
                        String clocks = map.get("clock");
                        String[] c = clocks.split(",");
                        out.write("clock={");
                        for(int i=0,length=c.length; i<length; i++){
                            c[i] = "\"" + c[i].substring(1,c[i].lastIndexOf("=")) + "\":"
                                    + c[i].substring(c[i].lastIndexOf("=")+1);
                            if(i < length-1){
                                out.write(c[i] + ",");
                            }else{
                                out.write(c[i]);
                            }

                        }
                        out.write(", ");
                    }
                    if(map.containsKey("dest")){
                        out.write("dest="+ map.get("dest") + ", ");
                    }
                    if(map.containsKey("event")){
                        out.write("event="+ map.get("event") + ", ");
                    }
                    if(map.containsKey("type")){
                        out.write("type="+ map.get("type") + ", ");
                    }
                    if(map.containsKey("error")){
                        out.write("error="+ map.get("error") + ", ");
                    }
                    if(map.containsKey("parentId")){
                        out.write("parentId="+ map.get("parentId") + ", ");
                    }
                    if(map.containsKey("timestamp")){
                        out.write("timestamp="+ map.get("timestamp") + ", ");
                    }


                    out.write("}\r\n");
                }
            }



        }catch(IOException e){
            e.printStackTrace();
            return false;
        }finally{
            if (out != null) {
                try {
                    out.flush();
                    out.close();
                } catch (IOException e1) {
                }
            }
        }

        return true;
    }
}
