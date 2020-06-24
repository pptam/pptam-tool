#Requires dataFile 

#Identify selected configurations from dataFile
mySettings <-unique(dataFile[,1:5])
#print(mySettings)

##END SETTINGS

#THRESHOLD
#Define the threshold for each service. The threshold is a vector computed as avg+3*SD for the configuration with Users=2, Memory=4, CPU=1, CartReplica=1   
noMicroServices<-ncol(dataFile)-6
tempBench<-dataFile[dataFile$Users==2,]
benchSettings<-mySettings[mySettings$Users==2,]
avgVectorB<-tempBench[tempBench$Metric=="Avg (sec)",][,-c(1:6)]
SDVectorB<- tempBench[tempBench$Metric=="SD (sec)",][,-c(1:6)]
mixB<-tempBench[tempBench$Metric=="Mix % (take failure into account)",][,-c(1:6)]
threshold<-data.frame(benchSettings,avgVectorB+3*SDVectorB)


#SELECT DATA FROM FILE
#Exclude case with user = 2 from dataFile and check whether each service pass or fail: avg<threshold (Pass). 
#Select relevant rows
usedSettings<-mySettings[!mySettings$Users==2,]
usedDataFile<-dataFile[!dataFile$Users==2,]
#average number of access
avg<-usedDataFile[usedDataFile$Metric=="Avg (sec)",-6]
#standard deviation of access
SD<-usedDataFile[usedDataFile$Metric=="SD (sec)",-6]
#This is the frequency of access to a microservice
mixTemp<-usedDataFile[usedDataFile$Metric=="Mix % (take failure into account)",-6]

