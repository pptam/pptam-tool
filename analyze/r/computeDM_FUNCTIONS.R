#Functions needed before plotting and tables

#Identify selected configurations from dataFile
mySettings <-unique(dataFile[,1:5])
#print(mySettings)

##END SETTINGS

#FUNCTIONS

#Create aggregated values (by myOrderedSplitting) of the user frequency from "operationalProfile" 
aggregateValues<-function(myOrderedSplitting, accessCount, scaledUsersLoad){
accessFrequency<-accessCount/sum(accessCount)
if(length(myOrderedSplitting)==1){
n<-myOrderedSplitting
#this case happens only when a splitting parameter "n" is given. the experiemnts are run independently 
byN<-which(scaledUsersLoad %% n == 0)
print(byN)
binProb<-c()
for(i in 1:length(byN)){
	if(i==1){
		binProb[i]<-sum(accessFrequency[1:byN[i]])
	}else{
		binProb[i]<-sum(accessFrequency[(byN[i-1]+1): byN[i]])
	}
}
aggregatedValues<-matrix(c(scaledUsersLoad[byN], binProb), ncol=2,nrow=length(binProb), dimnames=list(c(1:length(binProb)), c("Workload (number of users)", "Domain metric per workload")))
print(scaledUsersLoad[byN])
}else{
	print(myOrderedSplitting)
	binProb<-c()
	
	for(i in 1:length(myOrderedSplitting)){
		if(i==1){
		binProb[i]<-sum(accessFrequency[1: which.min(abs(scaledUsersLoad - myOrderedSplitting[i]))])
	}else{
		binProb[i]<-sum(accessFrequency[(which.min(abs(scaledUsersLoad - myOrderedSplitting[i-1]))+1): which.min(abs(scaledUsersLoad - myOrderedSplitting[i]))])
	}
	}
	aggregatedValues<-matrix(c(myOrderedSplitting, binProb), ncol=2,nrow=length(binProb), dimnames=list(c(1:length(binProb)), c("Workload (number of users)", "Domain metric per workload")))
}
return(aggregatedValues)
}

#Compute the mass for each load and each configuration
computeRelativeMass<-function(threshold, avg, mixTemp){

#Check pass/fail for each service. the "mix" value is 0 if fail and mixTemp if pass. Compute the relative mass for each configuration
passCriteria<-avg
relativeMass<-c()
mix<-as.data.frame(matrix(nrow=nrow(usedSettings), ncol=ncol(mixTemp)))
for(j in 1:nrow(passCriteria)){
	mix[j,]<-mixTemp[j,]
	for(i in 6:(5+noMicroServices)){
		if(passCriteria[j,i]>threshold[i]){mix[j,i]<-0}
	}
	relativeMass[j]<-sum(mix[j,6:(5+noMicroServices)])
}
return(relativeMass)
}

#Compute the domain metric for all configurations
computeDomainMetricsAll<-function(usedSettings, relativeMass, aggregatedValues){
tempData<-usedSettings
tempData$relativeMass<-relativeMass
absoluteMass<-c()
for(j in 1:nrow(tempData)){	
	absoluteMass[j]<-tempData[j,"relativeMass"]*aggregatedValues[match(tempData[j,"Users"], aggregatedValues[,1]),2]
}
#head(finalSettings)
tempData$absoluteMass<-absoluteMass
return(tempData)
}

#Compute the domain metric for each configuration as a list
computeDomainMetrics<-function(usedSettings, relativeMass, aggregatedValues ){
tempData<-usedSettings
tempData$relativeMass<-relativeMass
absoluteMass<-c()
for(j in 1:nrow(tempData)){	
	absoluteMass[j]<-tempData[j,"relativeMass"]*aggregatedValues[match(tempData[j,"Users"], aggregatedValues[,1]),2]
}
tempData$absoluteMass<-absoluteMass

mySettingsUnique<-unique(tempData[3:5])
set<-list()
domainMetricList<-list()
for(i in 1:nrow(mySettingsUnique)){
	set[[i]]<-tempData[which(tempData[,3] == mySettingsUnique[i,1]&tempData[,4] == mySettingsUnique[i,2]&tempData[,5] == mySettingsUnique[i,3]),]
    domainMetricList[[i]]<-set[[i]][,c(2,7)][order(set[[i]][,c(2,7)][,1]),]
}
return(domainMetricList)
}

#Compute Cumulative Domain Metric: summing up absoluteMass over loads for each configuration. Plot in a table
computeCumulativeDomainMetric<-function(usedSettings, relativeMass, aggregatedValues){
tempData<-computeDomainMetricsAll(usedSettings, relativeMass, aggregatedValues )
mySettingsUnique<-unique(tempData[3:5])
mySettingsUnique$domainMetric<-0
for(i in 1:nrow(mySettingsUnique)){
	mySettingsUnique[i,4]<-round(sum(tempData[which(tempData[,3] == mySettingsUnique[i,1]&tempData[,4] == mySettingsUnique[i,2]&tempData[,5] == mySettingsUnique[i,3]),"absoluteMass"]),4)
}
domainMetric<-mySettingsUnique
return(domainMetric)
}

