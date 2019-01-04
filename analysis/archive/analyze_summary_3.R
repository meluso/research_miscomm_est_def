# Setup ------------------------------------------------------------------------

    # Clear the environment and console
    rm(list = ls())
    cat("\014")
    options(width = 1000)
    
    # Import libraries
    library(ggplot2)
    library(fitdistrplus)
    
    # Import data
    results <- read.csv("~/2016-Present (Michigan)/Research/12 Estimation Definitions/04 Analysis/Results/2018-11-10_08-13-06_MCResultsSummary.csv", header=FALSE)
    names(results)[1:7] <- c('index','method','fn','probability','cycles','performance','degree')
    
    # Create vectors of variables
    methods = c("future_est","best_est")
    prob = c(0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0)

# Organize Data ----------------------------------------------------------------
    
    # Slice data by functions
    ackley = results[results$fn == "ackley",c(1:2,4:7)]

    # Copy over column names
    names(ackley)[1:6] = names(results)[c(1:2,4:7)]

# Create Plot Data -------------------------------------------------------------

    # Create data frames for estimate type results
    plotdata = data.frame()
    len = 3
    
    # Create future performances
    for (i in 1:length(prob)){
        
        # Fill table probability
        plotdata[i,1] = prob[i]
        
        # Iterate over each method for columns
        for (j in 1:length(methods)){
            
            # Define the base column from which to work
            b = (j-1)*len + 1
            
            # Get the data for the respective method
            input = ackley$performance[ackley$probability == prob[i] & ackley$method == methods[j]]
            
            # Fill the mean & standard error range
            mean_and_stderr = mean_se(input)
            plotdata[i,b+1] = mean_and_stderr[1] # Mean
            plotdata[i,b+2] = mean_and_stderr[2] # Lower
            plotdata[i,b+3] = mean_and_stderr[3] # Upper
        }
    }
    names(plotdata) = c("prob","f.perf","f.min","f.max","b.perf","b.min","b.max")
    
# Fit distributions ------------------------------------------------------------
    
    # Reduce dataset to get datapoints for distribution fit
    ackley.future = ackley[ackley$method == "future_est",c(3,5)]
    ackley.best = ackley[ackley$method == "best_est",c(3,5)]
    
    # Fit Ackley to piecewise model
    f.lrp <- function(x,a,b,t.x){
        ifelse(x<t.x,a+b*t.x,a+b*x)
        }
    ackley.future.pw = nls(performance ~ I(exp(1)^(a + b * probability)), data = ackley.future, start = list(a=0,b=1),trace=T)
    
    # Fit future exponential model
    fit.future = nls(performance ~ I(exp(1)^(a + b * probability)), data = ackley.future, start = list(a=0,b=1),trace=T)
    summary(fit.future)
    a <- summary(fit.future)$coefficients[1,1]
    b <- summary(fit.future)$coefficients[2,1]
    s <- seq(0,1,length=100)
    lines(s,predict(fit.future,list(probability=s)),lty=1,col=1)
    
    # Fit future exponential model
    fit.best = nls(performance ~ I(exp(1)^(a + b * probability)), data = ackley.best, start = list(a=0,b=1),trace=T)
    summary(fit.best)
    a <- summary(fit.best)$coefficients[1,1]
    b <- summary(fit.best)$coefficients[2,1]
    s <- seq(0,1,length=100)
    lines(s,predict(fit.best,list(probability=s)),lty=1,col=2)

# Plot results -----------------------------------------------------------------
    
    # Plot future
    pl.future = ggplot(plotdata,aes(x = prob, y = value)) + 
        geom_point(aes(x = prob, y = f.perf)) +
        geom_errorbar(aes(x = prob, ymin = f.min, ymax = f.max), inherit.aes = FALSE)
    pl.future
    
    # Plot best
    pl.best = ggplot(plotdata,aes(x = prob, y = value)) + 
        geom_point(aes(x = prob, y = b.perf)) +
        geom_errorbar(aes(x = prob, ymin = b.min, ymax = b.max), inherit.aes = FALSE)
    pl.best
    
    # Plot all
    pl = ggplot(plotdata,aes(x = prob, y = value, color = variable)) + 
        geom_point(aes(x = prob, y = f.perf), inherit.aes = FALSE, data=plotdata) +
        geom_errorbar(aes(x = prob, ymin = f.min, ymax = f.max), inherit.aes = FALSE, data=plotdata) + 
        geom_point(aes(x = prob, y = b.perf), inherit.aes = FALSE, data=plotdata) +
        geom_errorbar(aes(x = prob, ymin = b.min, ymax = b.max), inherit.aes = FALSE, data=plotdata)
    pl    
    