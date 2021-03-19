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

# Organize Data ----------------------------------------------------------------
    
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
    
# Calculate descriptive statistics ---------------------------------------------
    
    sphere.current.desc = print(describe(sphere.current)[3:4,],digits = 4)
    sphere.future.desc = print(describe(sphere.future)[3:4,],digits = 4)
    ackley.current.desc = print(describe(ackley.current)[3:4,],digits = 4)
    ackley.future.desc = print(describe(ackley.future)[3:4,],digits = 4)
    rosen.current.desc = print(describe(rosen.current)[3:4,],digits = 4)
    rosen.future.desc = print(describe(rosen.future)[3:4,],digits = 4)
    stybtang.current.desc = print(describe(stybtang.current)[3:4,],digits = 4)
    stybtang.future.desc = print(describe(stybtang.future)[3:4,],digits = 4)
    
    

# Plot by Methods --------------------------------------------------------------
    
    # Sphere function
    plotmeans(performance ~ method,
              main="Sphere Function Performance Comparison",
              xlab="Estimate Definition",
              ylab="Mean Converged Objective Value",
              data = sphere.methods)
    plotmeans(cycles ~ method,
              main="Sphere Function Cycles Comparison",
              xlab="Estimate Definition",
              ylab="Mean Convergence Cycles",
              data = sphere.methods)
    
    # Ackley function
    plotmeans(performance ~ method,
              main="Ackley Function Performance Comparison",
              xlab="Estimate Definition",
              ylab="Mean Converged Objective Value",
              n.label = FALSE,
              data = ackley.methods)
    plotmeans(cycles ~ method,
              main="Ackley Function Cycles Comparison",
              xlab="Estimate Definition",
              ylab="Mean Convergence Cycles",
              data = ackley.methods)
    
    # Rosenbrock function
    plotmeans(performance ~ method,
              main="Rosenbrock Function Performance Comparison",
              xlab="Estimate Definition",
              ylab="Mean Converged Objective Value",
              data = rosen.methods)
    plotmeans(cycles ~ method,
              main="Rosenbrock Function Cycles Comparison",
              xlab="Estimate Definition",
              ylab="Mean Convergence Cycles",
              n.label=FALSE,
              data = rosen.methods)
    
    # Styblinski-Tang function
    plotmeans(performance ~ method,
              xlab="Estimate Definition",
              ylab="Mean Converged Objective Value",
              data = stybtang.methods)
    plotmeans(cycles ~ method,
              xlab="Estimate Definition",
              ylab="Mean Convergence Cycles",
              data = stybtang.methods)
    
# Statistics & ANOVA -----------------------------------------------------------
    
    # Sphere function
    sphere.summary = describeBy(sphere.methods[c(2:4)],
                                group=sphere.methods$method,
                                digits=4,
                                mat=TRUE)
    sphere.aov.perf = aov(performance ~ method,data=sphere.methods)
    sphere.aov.cyc = aov(cycles ~ method,data=sphere.methods)
    summary(sphere.aov.perf)
    summary(sphere.aov.cyc)
    coefficients(sphere.aov.perf)
    coefficients(sphere.aov.cyc)
    TukeyHSD(sphere.aov.perf)
    TukeyHSD(sphere.aov.cyc)
    
    # Ackley function
    ackley.summary = describeBy(ackley.methods[c(2:4)],
                                group=ackley.methods$method,
                                digits=4,
                                mat=TRUE)
    ackley.aov.perf = aov(performance ~ method,data=ackley.methods)
    ackley.aov.cyc = aov(cycles ~ method,data=ackley.methods)
    summary(ackley.aov.perf)
    summary(ackley.aov.cyc)
    coefficients(ackley.aov.perf)
    coefficients(ackley.aov.cyc)
    TukeyHSD(ackley.aov.perf)
    TukeyHSD(ackley.aov.cyc)
    
    # Rosenbrock function
    rosen.summary = describeBy(rosen.methods[c(2:4)],
                                group=rosen.methods$method,
                                digits=4,
                                mat=TRUE)
    rosen.aov.perf = aov(performance ~ method,data=rosen.methods)
    rosen.aov.cyc = aov(cycles ~ method,data=rosen.methods)
    summary(rosen.aov.perf)
    summary(rosen.aov.cyc)
    coefficients(rosen.aov.perf)
    coefficients(rosen.aov.cyc)
    TukeyHSD(rosen.aov.perf)
    TukeyHSD(rosen.aov.cyc)
    
    # Styblinski-Tang function
    stybtang.summary = describeBy(stybtang.methods[c(2:4)],
                                group=stybtang.methods$method,
                                digits=4,
                                mat=TRUE)
    stybtang.aov.perf = aov(performance ~ method,data=stybtang.methods)
    stybtang.aov.cyc = aov(cycles ~ method,data=stybtang.methods)
    summary(stybtang.aov.perf)
    summary(stybtang.aov.cyc)
    coefficients(stybtang.aov.perf)
    coefficients(stybtang.aov.cyc)
    TukeyHSD(stybtang.aov.perf)
    TukeyHSD(stybtang.aov.cyc)
    
# Distribution fit -------------------------------------------------------------
    
    # Ackley & Rosenbrock Mean Disproval
    shapiro.test(rosen.current$cycles)
    shapiro.test(rosen.current$performance)
    shapiro.test(rosen.future$cycles)
    shapiro.test(rosen.future$performance)
    shapiro.test(ackley.current$cycles)
    shapiro.test(ackley.current$performance)
    shapiro.test(ackley.future$cycles)
    shapiro.test(ackley.future$performance)
    
    # Wilcoxon-Mann-Whitney Test of Rosenbrock Cycles
    wilcox.test(rosen.current$cycles,
                rosen.future$cycles,
                alternative = "two.sided",
                conf.int = TRUE,
                conf.level = 0.95)
    
    # Wilcoxon-Mann-Whitney Test of Rosenbrock Performance
    wilcox.test(rosen.current$performance,
                rosen.future$performance,
                alternative = "greater",
                conf.int = TRUE,
                conf.level = 0.95)
    
    # Wilcoxon-Mann-Whitney Test of Ackley Cycles
    wilcox.test(ackley.current$cycles,
                ackley.future$cycles,
                alternative = "two.sided",
                conf.int = TRUE,
                conf.level = 0.95)
    
    # Wilcoxon-Mann-Whitney Test of Ackley Performance
    wilcox.test(ackley.current$performance,
                ackley.future$performance,
                alternative = "less",
                conf.int = TRUE,
                conf.level = 0.95)
    
    