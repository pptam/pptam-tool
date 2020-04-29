#Requires myOrderedSplitting, accessCount, scaled.number.of.users, computeThreshold.R, usedSettings

#Set to the working directory defined in Start.R
setwd(currentWD)

aggregatedValuesVSA<-aggregateValues(myOrderedSplitting, accessCount, scaled.number.of.users)
print(head(aggregatedValuesVSA))

domainMetric<-computeCumulativeDomainMetric(usedSettings, relativeMass, aggregatedValuesVSA)
print("Plot ranking table for VSA")
#PLOTS & TABLES
#Plot cumulative domain metric as a table
pdf("TableVSA.pdf", height=5, width=5)
p<-tableGrob(round(domainMetric[order(-domainMetric[,4]),],3), rows=NULL)
grid.arrange(p)

print("Plot polygons for VSA")
#Plot operationalProfile against domain metric for each configuration
jpeg(filename="PolygonsVSA.jpeg", width = 480, height = 480, units = "px", pointsize = 12,
     quality = 75,
     bg = "white", res = NA)

plot(aggregatedValuesVSA, xlim=c(aggregatedValuesVSA[1,1], aggregatedValuesVSA[nrow(aggregatedValuesVSA),1]), ylim=c(0, max(aggregatedValuesVSA[,2])+0.05),cex.lab=1.3)
polygon(c(min(aggregatedValuesVSA[, 1]),aggregatedValuesVSA[,1],max(aggregatedValuesVSA[, 1])),c(0,aggregatedValuesVSA[,2],0), col=adjustcolor("darkblue",alpha.f = 0.2), lty = 1, lwd = 3, border = "darkblue")
color<-cm.colors(nrow(unique(usedSettings[,3:5])))
color_transparent <- adjustcolor(color, alpha.f = 0.2) 

relativeMass<-computeRelativeMass(threshold, avg, mixTemp)  

domainMetricList<-computeDomainMetrics(usedSettings, relativeMass, aggregatedValuesVSA)

myL<-list()
myValue<-c()
for(i in 1:nrow(unique(usedSettings[,3:5]))){
	#print(domainMetricList[[i]][,2]>=aggregatedValuesVSA[,2])
	myL[[i]]<-domainMetricList[[i]][,2]>=aggregatedValuesVSA[,2]
	myValue[i]<-min(which(myL[[i]] %in% FALSE))-1
	}
bestApproachingLine<-which.max(myValue)
bestDMLine<-which.max(domainMetric[,4])

# for(i in 1:nrow(unique(usedSettings[,3:5]))){
   # lines(domainMetricList[[i]], type="l",lwd = 3, col=color[i])
    
    # polygon(c(min(aggregatedValuesVSA[, 1]),t(domainMetricList[[i]][1]),max(aggregatedValuesVSA[, 1])),c(0,t(domainMetricList[[i]][2]),0), col=color_transparent[i], lty = 1, lwd = 3,  border =NA)
# }
for(i in c(1:nrow(unique(usedSettings[,3:5])))[-c(bestApproachingLine, bestDMLine)]){
   lines(domainMetricList[[i]], type="l",lwd = 2)
    polygon(c(min(aggregatedValuesVSA[, 1]),t(domainMetricList[[i]][1]),max(aggregatedValuesVSA[, 1])),c(0,t(domainMetricList[[i]][2]),0), col=NA, lty = 1, lwd = 2,  border =heat.colors(10)[i])
}

lines(domainMetricList[[bestDMLine]], type="l",lwd = 2) 
polygon(c(min(aggregatedValuesVSA[, 1]),t(domainMetricList[[bestDMLine]][1]),max(aggregatedValuesVSA[, 1])),c(0,t(domainMetricList[[bestDMLine]][2]),0), col=adjustcolor("blue", alpha.f = 0.2), lty = 1, lwd = 2,  border ="blue")

lines(domainMetricList[[bestApproachingLine]], type="l",lwd = 2)
polygon(c(min(aggregatedValuesVSA[, 1]),t(domainMetricList[[bestApproachingLine]][1]),max(aggregatedValuesVSA[, 1])),c(0,t(domainMetricList[[bestApproachingLine]][2]),0), col=adjustcolor("red", alpha.f = 0.2) , lty = 1, lwd = 2,  border ="red")

text(aggregatedValuesVSA,labels =round(aggregatedValuesVSA[1:nrow(aggregatedValuesVSA),2],3), pos=3, col="black")
graphics.off()

#SENSITIVITY ANALYSIS
#k is the vector of indexes of the configuration (in sortedDomainMetric) for which the domain metric is maximal, j is the the mimimum index of domainMetric corresponding to the minimum value of k.
setwd(originalDirectory)
aggregatedValues<-aggregatedValuesVSA
source("SensitivityAnalysis.R")
if (length(k) == 1) {
  pdf(paste("SensitivityAnalysis_BestConfiguration_VSA.pdf", sep = ""))
  computeSensitivityPerConfiguration(j, domainMatricVariant, scale, 0, 50, 0)
  graphics.off()
} else{
  pdf(paste("SensitivityAnalysis_BestConfigurationVSA.pdf", sep = ""))
  computeSensitivityPerConfiguration(j, domainMatricVariant, scale, 0, 50, 0)
  pdf(paste("SensitivityAnalysisBestConfigurationsTable_VSA.pdf", sep = ""))
  plot.new()
  vps <- baseViewports()
  pushViewport(vps$figure)
  vp1 <- plotViewport()
  tt <-
    ttheme_default(colhead = list(fg_params = list(parse = TRUE)))
  grid.table(
    round(sortedDomainMetric[k, ], 3),
    rows = NULL,
    theme = ttheme_minimal(
      base_size = 9,
      core = list(padding = unit(c(1, 1), "mm")),
      colhead = list(fg_params = list(parse = TRUE))
    )
  )
  popViewport()
  graphics.off()
}
print("end of sensitivity analysis for VSA")