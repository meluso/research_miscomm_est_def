# Setup ------------------------------------------------------------------------

    # Clear the environment and console
    rm(list = ls())
    cat("\014")
    options(width = 1000)
    
    # Import libraries
    library(psych)
    library(ggplot2)
    library(gplots)
    
    # Import data
    results <- read.csv("~/2016-Present (Michigan)/Research/12 Estimation Definitions/04 Analysis/Results/2019-05-08_22-32-25_MCResultsSummary.csv", header=FALSE)
    names(results)[1:7] <- c('index','method','fn','probability','cycles','performance','degree')
    
    # Create vectors of variables
    fns = c("sphere","ackley","rosen","stybtang")
    methods = c("current","future")

    # Slice data by functions
    sphere = results[results$fn == "sphere",c(1,4:6)]
    ackley = results[results$fn == "ackley",c(1,4:6)]
    rosen = results[results$fn == "rosenbrock",c(1,4:6)]
    stybtang = results[results$fn == "styblinski-tang",c(1,4:6)]
    
    # Copy over column names
    names(sphere)[1:4] = names(results)[c(1,4:6)]
    names(ackley)[1:4] = names(results)[c(1,4:6)]
    names(rosen)[1:4] = names(results)[c(1,4:6)]
    names(stybtang)[1:4] = names(results)[c(1,4:6)]
    
    # Slice data by methods
    sphere.current = cbind(sphere[sphere$probability == 0,],"current")
    sphere.future = cbind(sphere[sphere$probability == 1,],"future")
    ackley.current = cbind(ackley[ackley$probability == 0,],"current")
    ackley.future = cbind(ackley[ackley$probability == 1,],"future")
    rosen.current = cbind(rosen[rosen$probability == 0,],"current")
    rosen.future = cbind(rosen[rosen$probability == 1,],"future")
    stybtang.current = cbind(stybtang[stybtang$probability == 0,],"current")
    stybtang.future = cbind(stybtang[stybtang$probability == 1,],"future")
    
    # Rename the new methods column
    names(sphere.current)[5] = "method"
    names(sphere.future)[5] = "method"
    names(ackley.current)[5] = "method"
    names(ackley.future)[5] = "method"
    names(rosen.current)[5] = "method"
    names(rosen.future)[5] = "method"
    names(stybtang.current)[5] = "method"
    names(stybtang.future)[5] = "method"
    
    # Combine the data by method
    sphere.methods = rbind(sphere.current,sphere.future)
    ackley.methods = rbind(ackley.current,ackley.future)
    rosen.methods = rbind(rosen.current,rosen.future)
    stybtang.methods = rbind(stybtang.current,stybtang.future)

# Plot by Methods --------------------------------------------------------------

    # Ackley function
    par(mar=c(4,4,2,2)+0.1)
    plotmeans(performance ~ method,
              xlab="Estimate Definition",
              ylab="Mean Converged Objective Value",
              n.label = FALSE,
              data = ackley.methods)
    
    # Rosenbrock function
    plotmeans(cycles ~ method,
              xlab="Estimate Definition",
              ylab="Mean Convergence Cycles",
              n.label=FALSE,
              data = rosen.methods)

# Re-Organize Data -------------------------------------------------------------
    
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
    
# Plot Ackley ------------------------------------------------------------------

    # Scatterplot
    plot(ackley$probability,ackley$performance,
         xlab = "Probability",
         ylab = "System Performance")
    
    # Mean plot
    plotmeans(performance ~ probability,
              data=ackley,
              xlab="Probability",
              ylab="System Performance",
              n.label = FALSE)
