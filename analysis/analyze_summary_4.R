# Setup ------------------------------------------------------------------------

    # Clear the environment and console
    rm(list = ls())
    cat("\014")
    options(width = 1000)
    
    # Import libraries
    library(ggplot2)
    library(gplots)
    library(fitdistrplus)
    
    # Import data
    results <- read.csv("~/2016-Present (Michigan)/Research/12 Estimation Definitions/04 Analysis/Results/2019-05-08_22-32-25_MCResultsSummary.csv", header=FALSE)
    names(results)[1:7] <- c('index','method','fn','probability','cycles','performance','degree')
    
    # Create vectors of variables
    fns = c("sphere","ackley","rosen","stybtang")
    methods = c("current","future")

# Organize Data ----------------------------------------------------------------
    
    # Slice data by functions
    sphere = results[results$fn == "sphere",c(1:2,4:7)]
    ackley = results[results$fn == "ackley",c(1:2,4:7)]
    rosen = results[results$fn == "rosenbrock",c(1:2,4:7)]
    stybtang = results[results$fn == "styblinski-tang",c(1:2,4:7)]
    
    # Extra slice of ackley
    ackley.future = ackley[ackley$probability == 1,]
    
    # Copy over column names
    names(sphere)[1:6] = names(results)[c(1:2,4:7)]
    names(ackley)[1:6] = names(results)[c(1:2,4:7)]
    names(rosen)[1:6] = names(results)[c(1:2,4:7)]
    names(stybtang)[1:6] = names(results)[c(1:2,4:7)]
    
# Plot means -------------------------------------------------------------------
    
    # Sphere
    plotmeans(performance ~ probability,
              data=sphere,
              main="Sphere Mean Performance by Estimate Definition Probability",
              xlab="Probability",
              ylab="System Performance",
              n.label = FALSE,
              barcol = "#00274C")
    
    # Ackley
    plotmeans(performance ~ probability,
              data=ackley,
              main="Ackley Mean Performance by Estimate Definition Probability",
              xlab="Probability",
              ylab="System Performance",
              n.label = FALSE,
              barcol = "#00274C")
    
    # Rosenbrock
    plotmeans(performance ~ probability,
              data=rosen,
              main="Rosenbrock Mean Performance by Estimate Definition Probability",
              xlab="Probability",
              ylab="System Performance",
              n.label = FALSE,
              barcol = "#00274C")
    
    # Styblinski-Tang
    plotmeans(performance ~ probability,
              data=stybtang,
              main="Styblinski-Tang Mean Performance by Estimate Definition Probability",
              xlab="Probability",
              ylab="System Performance",
              n.label = FALSE,
              barcol = "#00274C")
    
# Fit distributions ------------------------------------------------------------
    
    # Scatterplots
    plot(ackley$probability,ackley$performance,
         main="Ackley System Performance vs. Estimate Definition Probability",
         xlab = "Probability",
         ylab = "System Performance")
    
    # Fit Ackley to piecewise model
    f.lrp <- function(x,a,b,t.x){
        ifelse(x<t.x,a+b*t.x,a+b*x)
    }
    
    ackley.pw = nls(performance ~ I(exp(1)^(a + b * probability)), data = ackley, start = list(a=0,b=1),trace=T)
    summary(ackley.pw)

    plotmeans(performance ~ probability,
              data=ackley,
              main="Ackley Mean Performance by Estimate Definition Probability",
              xlab="Probability",
              ylab="System Performance",
              n.label = FALSE)
    
    # Temp exponential model
    fit.future = nls(performance ~ I(exp(1)^(a + b * probability)), data = ackley, start = list(a=0,b=1),trace=T)
    a <- round(summary(fit.future)$coefficients[1,1],4)
    b <- round(summary(fit.future)$coefficients[2,1],4)
    s <- seq(0,1,length=100)
    lines(10*s+1,predict(fit.future,list(probability=s)),lty=1,col=2)
    summary(fit.future)
    
# Examine future causes --------------------------------------------------------
    
    # Create scatterplot of performance vs cycles
    plot(ackley.future$cycles,ackley.future$performance)
    
    # Plots means of performance vs cycles
    plotmeans(performance ~ cycles,
              data=ackley.future,
              xlab="Number of Cycles",
              ylab="System Performance",
              n.label = FALSE)
    
    corfut = cor(ackley.future$cycles,ackley.future$performance)
    cor.test(ackley.future$cycles,ackley.future$performance,method="pearson",alternative="greater")    
    