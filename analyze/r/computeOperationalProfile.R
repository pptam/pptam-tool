#Provide accessCount and scaledUsersLoad

## Options
max.num.users <-myMax
num.load.levels <- myLevels
## END Options

#Operational profile of Wikipedia
profile.project <- "de"
profile.filename <- paste("wikipedia-profile-", profile.project, ".csv", sep = "")
project.count.data <- read.csv2(profile.filename)
head(project.count.data)
options(repr.plot.width=10, repr.plot.height=6)
#plot(project.count.data, type = "l", col = "blue", lwd = 1.5)
#graphics.off()

#scale the load
max.requests <- max(project.count.data$requests)
scale.factor <- max.num.users / max.requests
print(paste("Maximum is", max.requests, "requests, scale factor is", scale.factor))
scaled.number.of.users <- scale.factor * project.count.data$requests
#set a number of load leavels to plot the operational profile
#num.load.levels<-50
#identify bins
options(repr.plot.width=10, repr.plot.height=6)
num.users.hist <- hist(scaled.number.of.users,
     breaks = num.load.levels,
     col = "darkgray", border = "white",
     xlab = "scaled number of users", main = "Histogram of scaled number of users", plot=T)     
#To plot relative frequencies instead of density, uncomment the following and set plot=F in previous line in the hist options
num.users.hist$frequency<-num.users.hist$counts / sum(num.users.hist$counts)

#num.users.hist$breaks

frequencies.of.occurrence <- data.frame(
     scaled.number.of.users = num.users.hist$breaks,
     frequency.of.occurrence = c(0,num.users.hist$frequency)
)

aggregatedValuesWikipedia<-frequencies.of.occurrence

#quartz(). Use the below script only with not particular myOrderedSplitting
aggregatedValuesWikipedia<-subset(aggregatedValuesWikipedia, aggregatedValuesWikipedia$scaled.number.of.users<=max(myOrderedSplitting))
scaled.number.of.users<-aggregatedValuesWikipedia$scaled.number.of.users
accessCount<-aggregatedValuesWikipedia$accessCount
colnames(aggregatedValuesWikipedia)<-c("Workload situation (number of users)", "frequency")
#this plots the operational profile as a line curve. Use it in combination of the num.load.levels. Uncomment this to plot the operational profile
#plot(aggregatedValuesWikipedia, type="b", bty="n")

print(aggregatedValuesWikipedia)

########

#Operational profile from APM tool here. Streaming video application. Returns AccessCount and scaled.number.of.users
operationalProfile<-read.csv("OperationalProfileData.csv", header= TRUE,sep=",")[,1:2]
#quartz()
#options(repr.plot.width=10, repr.plot.height=6)
#plot(operationalProfile, type = "l", col = "blue", lwd = 1.5)
#graphics.off()

usersLoad<-operationalProfile[,1]
accessCount<-operationalProfile[,2]

#scale the load
max.requests <- max(usersLoad)
scale.factor<-max.num.users/max.requests
print(paste("Maximum is", max.requests, "requests, scale factor is", scale.factor))

scaled.number.of.users<-scale.factor*usersLoad
newSet<-data.frame(scaled.number.of.users,accessCount)
quartz()
newSet<-subset(newSet, newSet$scaled.number.of.users<=max(myOrderedSplitting))
scaled.number.of.users<-newSet$scaled.number.of.users
accessCount<-newSet$accessCount
accessCountFrequency<-accessCount/sum(accessCount)
newSet$frequency<-accessCountFrequency
colnames(newSet)<-c("Workload situation (number of users)", "count","frequency")
plot(newSet[,c(1,3)], type="b", bty="n")

# scaled.number.of.requests<-c()
# for(i in 1:length(accessCount)){scaled.number.of.requests<-c(scaled.number.of.requests,rep(scaled.number.of.users[i], accessCount[i]))}

# options(repr.plot.width=10, repr.plot.height=6)
# num.users.hist <- hist(scaled.number.of.requests,
     # breaks = num.load.levels,
     # col = "darkgray", border = "white",
     # xlab = "scaled number of users", main = "Histogram of scaled number of users")     

# num.users.hist$breaks

# #identify bins
# options(repr.plot.width=10, repr.plot.height=6)
# num.users.hist <- hist(scaled.number.of.requests,
     # breaks = num.load.levels,
     # col = "darkgray", border = "white",
     # xlab = "scaled number of users", main = "Histogram of scaled number of users", plot=T)
# # create a data.frame() with loads and frequencies. Pay attention if original dataset contains values greater than the first break, the data.frame will not contain 0.    
# frequencies.of.occurrence <- data.frame(
    # scaled.number.of.users = (num.users.hist$breaks)[-15],
    # frequency.of.occurrence = num.users.hist$density
# )


 graphics.off()

# #To cut down to 100 load uncomment these lines
# frequencies.of.occurrence<-subset(frequencies.of.occurrence,
# frequencies.of.occurrence$scaled.number.of.users<101)