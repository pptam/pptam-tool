# Steps used to compile

1. rm -rf ~/.m2/repository/*
 
1. Added to ./trainticket/pom.xml:

    ```
    </project>
        </build>
            </plugins>
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-compiler-plugin</artifactId>
                    <version>3.8.1</version>
                    <configuration>
                        <annotationProcessorPaths>
                            <path>
                                <groupId>org.projectlombok</groupId>
                                <artifactId>lombok</artifactId>
                                <version>1.18.32</version>
                            </path>
                        </annotationProcessorPaths>
                        <source>1.8</source>
                        <target>1.8</target>
                    </configuration>
                </plugin>
            </plugins>
        </build>
    </project>
3. Set compilation level to 8 in
    ````
    <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <configuration>
            <source>8</source>
            <target>8</target>
        </configuration>
    </plugin>
2. Used `mvn clean install -Dmaven.test.skip=true` to compile