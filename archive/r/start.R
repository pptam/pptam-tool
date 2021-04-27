#clean console variables
rm(list=ls())

##SETTINGS

#Pre-requisites, comment these lines if you already installed the libraries
install.packages("RColorBrewer")
install.packages("gridExtra")
install.packages("gridBase")
install.packages("ggplot2")
library("RColorBrewer")
#Create the Table 
library(ggplot2)
library(gridExtra)
library(gridExtra)
library(gridBase)
library(grid)
library(scales)

#To get warnings, comment this out
oldw <- getOption("warn")
options(warn = -1)
#set working directory. Please substitute with yours
setwd("~/Research/Dropbox/OverleafGit/Microservices/Scripts/ScriptPaper")
originalDirectory<-getwd()
#originalDirectory

#Set folder for data and results. Substitute it with yours
experimentPath<-"DATA/Experiments"
myExperiments<-list.files(path= experimentPath)
print(myExperiments)

for (w in 1:length(myExperiments)){
	setwd(originalDirectory)
	setwd(paste(experimentPath,"/", myExperiments[w], sep=""))
	currentWD<-getwd()
	#Search file of experiment data
    myFiles<-list.files(path=getwd())
    myFileName<-myFiles[grep("benchflow_output.csv", myFiles)]
    allDataFileContent = readLines(myFileName)
    #The PPTAM tool exports files with the sep=, header and R does not handle that
	skipFirstLine = allDataFileContent
	dataFile <- read.csv(textConnection(skipFirstLine), header=TRUE, sep=",")
	head(dataFile)	
	#Set the maximum number of loads (myMax) your polygons will have. 
	myMax<-300
	#myMax<-max(dataFile$Users)
	#This is if you want to analyse experiments with different  granularity (50-based load or 20-based load scale). Set myLevels to either 5 or 10 if you do not need it
	if(w<4){myLevels<-5}else{myLevels<-10}
	print(paste("Analysing experiment ", myExperiments[w], sep=""))
	#extract the loads
	mySplitting<-unique(dataFile$Users)
	myOrderedSplitting<-mySplitting[order(mySplitting)][-1]
	print(myOrderedSplitting)
	#Compute the opertional profiles of the streaming video application and wikipedia
	setwd(originalDirectory)	
	source(paste(getwd(),"/computeOperationalProfile.R", sep=""), chdir = TRUE)	
	print(paste("Operational profile of Wikipedia and streaming video application for experiment  ", myExperiments[w], " have been computed", sep=""))
	#Compute the threshold of the baseline configuration. the baseline is re-computed for each of different experiment types (e.g., with or without attack) 
	source("computeThreshold.R")
	#Run all the function to compute the relative and the cumulative domain metric
	setwd(originalDirectory)
	source("computeDM_FUNCTIONS.R")
	#Sensitivity analysis and plots
	#When operational profile is given as time series of accesses like in the wikipedia case
	setwd(originalDirectory)
	source("plotWikipedia.R")
	#When operational profile is given as counts per load like in the videostreaming application case
	setwd(originalDirectory)
    source("plotVSA.R")
}

