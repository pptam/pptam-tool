
rest url:
http://rest-service-end:16000/greeting?cal=50
return json:
{"id":2,"result":false}


run:
java -jar target/rest-service-end-0.1.0.jar
java -jar /Users/admin/work/workspace_microservices/1-services/rest-service-end/target/rest-service-end-0.1.0.jar

dtrace run:
su root
/Users/admin/work/workspace_jvm/java-source-samples/sample/dtrace/hotspot/method_invocation_tree.d -c "java -jar /Users/admin/work/workspace_microservices/1-services/rest-service-end/target/rest-service-end-0.1.0.jar"
/Users/admin/work/workspace_jvm/java-source-samples/sample/dtrace/hotspot/method_invocation_tree.d -p 20985