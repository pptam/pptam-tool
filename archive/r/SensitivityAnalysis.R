#sensitivity analysis
#Require computeDomainMetric.R and computeThreshold
#PRE-PROCESSING
originalThreshold <- threshold
domainMatricVariantLower <- list()
relativeMassItem <- list()
scaledThresholdLower <- c()
for (m in c(1:50)) {
  l <- m / 50
  scaledThresholdLower <- l * originalThreshold
  relativeMassItem <-
    computeRelativeMass(scaledThresholdLower, avg, mixTemp)
  domainMatricVariantLower[[m]] <-
    computeDomainMetrics(usedSettings, relativeMassItem, aggregatedValues)
}

domainMatricVariantGreater <- list()
relativeMassItem <- list()
for (m in c(1:49)) {
  l <- (m + 50) / 50
  scaledThresholdGreater <- l * originalThreshold
  relativeMassItem <-
    computeRelativeMass(scaledThresholdGreater, avg, mixTemp)
  domainMatricVariantGreater[[m]] <-
    computeDomainMetrics(usedSettings, relativeMassItem, aggregatedValues)
}

domainMatricVariantIntegers <- list()
relativeMassItem <- list()
for (m in c(1:49)) {
  scaledThresholdIntegers <- (m + 1) * originalThreshold
  relativeMassItem <-
    computeRelativeMass(scaledThresholdIntegers, avg, mixTemp)
  domainMatricVariantIntegers[[m]] <-
    computeDomainMetrics(usedSettings, relativeMassItem, aggregatedValues)
}

scaleLower <- 1 / 50 * c(1:50)
scaleGreater <- 1 / 50 * c(51:99)
scaleIntegers <- c(2:50)

#all in once plots
domainMatricVariant <- list()
domainMatricVariant <- append(domainMatricVariantLower, domainMatricVariantGreater)
domainMatricVariant <- append(domainMatricVariant, domainMatricVariantIntegers)
scale <- c()
scale <- append(scaleLower, scaleGreater)
scale <- append(scale, scaleIntegers)
#print(head(domainMatricVariant))
#print(head(scale))
#xbottom<-0
# xtop<-50
# ybottom<-0

#FUNCTIONS
#set current directory as in Start.R
setwd(currentWD)
print("Definition of computeSensitivityPerConfiguration in SensitivityAnalysis.R")
computeSensitivityPerConfiguration <-function(k,domainMatricVariant,scale,xbottom,xtop,ybottom) {
    #r=load or users,
    #m= repetition
    originalValues <- scale * originalThreshold
    temp <- sum(originalThreshold[-c(1:5)])
    myTicks <- scale * temp
    t <- par(
      mfrow = c(4, 2),
      mar = c(2, 2.5, 2, 1),
      oma = c(3, 2, 3, 0.5)
    )
    
    for (r in c(1:nrow(domainMatricVariant[[1]][[1]]))) {
      if (aggregatedValues[r,2]>0){
      mass <- c()
      for (m in c(1:148)) {
        myList <- domainMatricVariant[[m]]
        mass[m] <- myList[[k]][r, 2]
      }
      #dev.new()
      plot(
        scale,
        mass,
        frame.plot = F,
        ylab = "",
        xlab = "",
        xaxt = "n",
        yaxt = "n",
        pch = "*",
        cex = 0.5,
        xlim = c(xbottom, xtop),
        ylim = c(ybottom, aggregatedValues[r, 2] * (1 + 5 / 100))
      )
      lines(
        scale,
        mass,
        type = "o",
        col = "black",
        pch = "*",
        cex = 1
      )
      abline(
        h = aggregatedValues[r, 2],
        col = "blue",
        lty = 3,
        cex = 0.1
      )
      abline(
        v = 1,
        col = "red",
        lty = 3,
        cex = 0.1
      )
      myDiff <- c()
      tempDiff <- -mass[148] + aggregatedValues[r, 2]
      if (tempDiff < 0.0001)
        tempDiff <- 0
      myDiff <- percent(max((tempDiff) / aggregatedValues[r, 2], 0))
      
      print(paste(mass[148], " ", aggregatedValues[r, 2], sep = ""))
      bestK <- c()
      bestK <- scale[which(mass == max(mass))[1]]
      print(bestK)
      legend(
        "bottomright",
        legend = paste("Load: ", r * aggregatedValues[1,1], ", Final Gap: ", myDiff , ", Scale:", bestK, sep =
                         "")
      )
      ticklabels <-
        round(myTicks[c(
          which(scale == 1),
          which(scale == 10),
          which(scale == 20),
          which(scale == 30),
          which(scale == 40),
          which(scale == 50)
        )], 2)
      axis(
        1,
        at = c(1, 10, 20, 30, 40, 50),
        labels = ticklabels,
        line = 1.5,
        tck = 0.01,
        padj = -3.8
      )
      axis(
        1,
        at = c(1, 10, 20, 30, 40, 50),
        labels = c(1, 10, 20, 30, 40, 50),
        line = 1.5,
        padj = -1,
        tck = -0.01
      )
      axis(2, tck = -0.01, padj = 1)
      title(xlab = "Scale", mgp = c(1.8, 1, 0))
      title(ylab = "Domain metric", mgp = c(1.5, 1, 0))
      }
       }
    #Plot aggregated polygon and experiemnt with best configuration
    k=2
    plot(
      aggregatedValues,
      frame.plot = F,
      xlim = c(aggregatedValues[1, 1], aggregatedValues[nrow(aggregatedValues), 1]),
      xaxt = "n",
      yaxt = "n",
      ylim = c(0, max(aggregatedValues[, 2]) * (1 + 5 / 100)),
      cex.lab = 1
    )
    polygon(
      c(
        min(aggregatedValues[, 1]),
        aggregatedValues[, 1],
        max(aggregatedValues[, 1])
      ),
      c(0, aggregatedValues[, 2], 0),
      col = adjustcolor("darkblue",alpha.f = 0.2),
      lty = 1,
      lwd = 2,
      border = "darkblue",
      cex = 0.5
    )
    #color = heat.colors(nrow(unique(usedSettings[, 3:5])))
    #color_transparent <- adjustcolor(color, alpha.f = 0.2)
    
    lines(domainMetricList[[k]], type = "l", col = "red")
    polygon(
      c(
        min(aggregatedValues[, 1]),
        t(domainMetricList[[k]][1]),
        max(aggregatedValues[, 1])
      ),
      c(0, t(domainMetricList[[k]][2]), 0),
      #col = color_transparent[i],
      col=adjustcolor("red", alpha.f = 0.2),
      lty = 1,
      lwd = 1,
      border = "red"
    )
    axis(2, tck = -0.01, padj = 1)
    axis(1, tck = -0.01, padj = -1)
    title(xlab = "load", mgp = c(1, 1, 0))
    title(ylab = "Domain Metric", mgp = c(1.5, 1, 0))
    
    #Plot configuration relative domain metric
    plot.new()
    vps <- baseViewports()
    pushViewport(vps$figure)
    vp1 <- plotViewport()
    tt <-
      ttheme_default(colhead = list(fg_params = list(parse = TRUE)))
    grid.table(
      round(domainMetricList[[k]], 3),
      rows = NULL,
      theme = ttheme_minimal(
        base_size = 8,
        core = list(padding = unit(c(1, 1), "mm")),
        colhead = list(fg_params = list(parse = TRUE))
      )
    )
    popViewport()
    
    mtext(
      paste(
        "Configuration: Memory=",
        sortedDomainMetric[k, 1],
        " CPU=",
        sortedDomainMetric[k,
                           2],
        " Replicas=",
        sortedDomainMetric[k, 3],
        sep = ""
      ),
      side = 3,
      line = 37,
      outer = F,
      cex = 0.8
    )
  }

# #Deprecated
# computeSensitivity <- function(domainMatricVariant, scale, xbottom, xtop, ybottom) {
# #k=configuration,
# #r=load or users,
# #m= repetition
# for (k in c(1:nrow(sortedDomainMetric))) {
# jpeg(filename=paste(k,"_sensitivity.jpeg", sep=""), width = 480, height = 480, units = "px", pointsize = 12,
# quality = 75,
# bg = "white", res = NA)
# computeSensitivityPerConfiguration(k, domainMatricVariant, scale, xbottom, xtop, ybottom)
# }
# }

#k=best configuration; domainMetric is computed in the ComputeDomainMetric file
sortedDomainMetric <-
  domainMetric[order(domainMetric[, 1], domainMetric[, 2], domainMetric[, 3]), ]
k <- which(sortedDomainMetric[, 4] == max(sortedDomainMetric[, 4]))
j<-min(which(domainMetric[,4]==sortedDomainMetric[k[1], 4]))

#Uncomment this to compute sensitivity analysis for all configuration
#computeSensitivityPerConfiguration(k,domainMatricVariantLower, scaleLower, 0,1.1, 0)
#computeSensitivityPerConfiguration(k,domainMatricVariantGreater, scaleGreater, 1,2.1, 0)
#computeSensitivityPerConfiguration(k,domainMatricVariantIntegers, scaleIntegers, 1,50, 0)
# print("Next print all cumulative DM for all configurations")
# for (k in 1:nrow(sortedDomainMetric)){
# pdf(paste("SensitivityAnalysis_",k,".pdf", sep=""))
# computeSensitivityPerConfiguration(k,domainMatricVariant,scale,0, 50, 0)
# print(k)
# graphics.off()
# }

#dev.off()