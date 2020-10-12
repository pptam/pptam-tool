
setwd(currentWD)
relativeMass<-computeRelativeMass(threshold, avg, mixTemp)  

domainMetricList<-computeDomainMetrics(usedSettings, relativeMass, aggregatedValuesWikipedia)
if(w<4){
aggregatedValuesWikipedia<-aggregatedValuesWikipedia[-1,]
}else{aggregatedValuesWikipedia}
#PLOTS & TABLES
print("Plot ranking table for Wikipedia")
#Plot cumulative domain metric as a table
pdf("TableWikipedia.pdf", height=5, width=5)
domainMetric<-computeCumulativeDomainMetric(usedSettings, relativeMass, aggregatedValuesWikipedia)
bestConfiguration<-domainMetric[order(-domainMetric[,4]),][1,1:3]
p<-tableGrob(round(domainMetric[order(-domainMetric[,4]),],3), rows=NULL)
grid.arrange(p)

print("Plot polygons for Wikipedia")
#Plot operationalProfile against domain metric for each configuration. Polygons
jpeg(filename="PolygonsWikipedia.jpeg", width = 480, height = 480, units = "px", pointsize = 12,
     quality = 75,
     bg = "white", res = NA)
plot(aggregatedValuesWikipedia, xlim=c(aggregatedValuesWikipedia[1,1], aggregatedValuesWikipedia[nrow(aggregatedValuesWikipedia),1]), ylim=c(0, max(aggregatedValuesWikipedia[,2])*(1+5/100)),cex.lab=1.3)
polygon(c(min(aggregatedValuesWikipedia[, 1]),aggregatedValuesWikipedia[,1],max(aggregatedValuesWikipedia[, 1])),c(0,aggregatedValuesWikipedia[,2],0), col=adjustcolor("darkblue",alpha.f = 0.2), lty = 1, lwd = 3, border = "darkblue")
	color=heat.colors(nrow(unique(usedSettings[,3:5])))
color_transparent <- adjustcolor(color, alpha.f = 0.2) 


myL<-list()
myValue<-c()
for(i in 1:nrow(unique(usedSettings[,3:5]))){
	#print(domainMetricList[[i]][,2]>=aggregatedValuesWikipedia[,2])
	myL[[i]]<-domainMetricList[[i]][,2]>=aggregatedValuesWikipedia[,2]
	myValue[i]<-min(which(myL[[i]] %in% FALSE))-1
	}
bestApproachingLine<-which.max(myValue)
bestDMLine<-which.max(domainMetric[,4])


# for(i in 1:nrow(unique(usedSettings[,3:5]))){
    # lines(domainMetricList[[i]], type="l", col=heat.colors(nrow(unique(usedSettings[,3:5])))[i])
    # polygon(c(min(aggregatedValuesWikipedia[, 1]),t(domainMetricList[[i]][1]),max(aggregatedValuesWikipedia[, 1])),c(0,t(domainMetricList[[i]][2]),0), col=color_transparent[i], lty = 1, lwd = 1 , border = rainbow(nrow(unique(usedSettings[,3:5])))[i])
# }

for(i in c(1:nrow(unique(usedSettings[,3:5])))[-c(bestApproachingLine, bestDMLine)]){
   lines(domainMetricList[[i]], type="l",lwd = 2)
    polygon(c(min(aggregatedValuesWikipedia[, 1]),t(domainMetricList[[i]][1]),max(aggregatedValuesWikipedia[, 1])),c(0,t(domainMetricList[[i]][2]),0), col=NA, lty = 1, lwd = 2,  border =heat.colors(20)[i])
}


lines(domainMetricList[[bestDMLine]], type="l",lwd = 2) 
polygon(c(min(aggregatedValuesWikipedia[, 1]),t(domainMetricList[[bestDMLine]][1]),max(aggregatedValuesWikipedia[, 1])),c(0,t(domainMetricList[[bestDMLine]][2]),0), col=adjustcolor("blue", alpha.f = 0.2), lty = 1, lwd = 2,  border ="blue")

lines(domainMetricList[[bestApproachingLine]], type="l",lwd = 2)
polygon(c(min(aggregatedValuesWikipedia[, 1]),t(domainMetricList[[bestApproachingLine]][1]),max(aggregatedValuesWikipedia[, 1])),c(0,t(domainMetricList[[bestApproachingLine]][2]),0), col=adjustcolor("red", alpha.f = 0.2) , lty = 1, lwd = 2,  border ="red")

text(aggregatedValuesWikipedia,labels = round(aggregatedValuesWikipedia[1:nrow(aggregatedValuesWikipedia),2],3), pos=3, col="black")
graphics.off()


#SENSITIVITY ANALYSIS
setwd(originalDirectory)
aggregatedValues<-aggregatedValuesWikipedia
print(paste("Analysing sensitivity for wikipedia experiment ", myExperiments[w], sep="" ))
print(aggregatedValues)
source("SensitivityAnalysis.R")
if (length(k) == 1) {
  pdf(paste("SensitivityAnalysis_BestConfigurationWikipedia.pdf", sep = ""))
  computeSensitivityPerConfiguration(k, domainMatricVariant, scale, 0, 50, 0)
  print(paste("Analysing sensitivity for wikipedia experiment", myExperiments[w], sep="" ))
} else{
  pdf(paste("SensitivityAnalysis_BestConfigurationWikipedia.pdf", sep = ""))
  computeSensitivityPerConfiguration(k[1], domainMatricVariant, scale, 0, 50, 0)
  pdf(paste("SensitivityAnalysisBestConfigurationsTable_Wikipedia.pdf", sep = ""))
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
print(paste("End computeMetrics for wikipedia experiment", myExperiments[w], sep="" ))