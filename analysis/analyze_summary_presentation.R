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
    results <- read.csv("~/2016-2020 (Michigan)/Research/12 Estimation Definitions/04 Analysis/Results/2019-05-08_22-32-25_MCResultsSummary.csv", header=FALSE)
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
    
    # Ackley
    plotmeans(performance ~ probability,
              data=ackley,
              xlab="Probability of Strategic Response",
              ylab="Organizational Performance Degradation",
              n.label = FALSE,
              barcol = "#00274C")
