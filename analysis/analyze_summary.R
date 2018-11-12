# Setup ------------------------------------------------------------------------

    # Clear the environment and console
    rm(list = ls())
    cat("\014")
    options(width = 1000)
    
    # Import libraries
    library(ggplot2)
    
    # Import data
    results <- read.csv("~/2016-Present (Michigan)/Research/12 Estimation Definitions/04 Analysis/Results/2018-11-10_08-13-06_MCResultsSummary.csv", header=FALSE)
    names(results)[1:7] <- c('index','method','fn','probability','cycles','performance','degree')
    
    # Create vectors of variables
    fns = c("sphere","ackley","rosen","stybtang")
    methods = c("current","future","best")

# Organize Data ----------------------------------------------------------------
    
    # Slice data by functions
    sphere = results[results$fn == "sphere",c(1:2,4:7)]
    ackley = results[results$fn == "ackley",c(1:2,4:7)]
    rosen = results[results$fn == "rosenbrock",c(1:2,4:7)]
    stybtang = results[results$fn == "styblinski-tang",c(1:2,4:7)]
    
    # Copy over column names
    names(sphere)[1:6] = names(results)[c(1:2,4:7)]
    names(ackley)[1:6] = names(results)[c(1:2,4:7)]
    names(rosen)[1:6] = names(results)[c(1:2,4:7)]
    names(stybtang)[1:6] = names(results)[c(1:2,4:7)]

    # Slice data by methods
    ackley.current = ackley[ackley$method == "future_est" & ackley$probability == 0,]
    ackley.future = ackley[ackley$method == "future_est" & ackley$probability == 1,]
    ackley.best = ackley[ackley$method == "best_est" & ackley$probability == 1,]
    
    # Slice data by probability
    ackley.current.prob = ackley[ackley$method == "future_est" & ackley$performance > 0 & ackley$probability < 1,]
    ackley.future.prob = ackley[ackley$method == "best_est" & ackley$performance > 0 & ackley$probability < 1,]
    
    # Create scatterplot data
    sphere.scatter = sphere[,c(4,5)]
    ackley.scatter = ackley[,c(4,5)]
    rosen.scatter = rosen[,c(4,5)]
    stybtang.scatter = stybtang[,c(4,5)]
    
# Perform Analyses -------------------------------------------------------------
    
    # Ackley T-Tests
    ackley.tcyc.CF = t.test(ackley.current$cycles,ackley.future$cycles)
    ackley.tcyc.CF
    ackley.tcyc.CB = t.test(ackley.current$cycles,ackley.best$cycles)    
    ackley.tcyc.CB
    ackley.tcyc.FB = t.test(ackley.future$cycles,ackley.best$cycles)
    ackley.tcyc.FB
    ackley.tperf.CF = t.test(ackley.current$performance,ackley.future$performance)
    ackley.tperf.CF
    ackley.tperf.CB = t.test(ackley.current$performance,ackley.best$performance)    
    ackley.tperf.CB
    ackley.tperf.FB = t.test(ackley.future$performance,ackley.best$performance)
    ackley.tperf.FB
    
    # Run regression on intermediate data (probability = 0.1 to 0.9)
    ackley.rcyc.C = lm(ackley.current.prob$cycles ~ ackley.current.prob$probability)
    summary(ackley.rcyc.C)
    ackley.rperf.C = lm(ackley.current.prob$performance ~ ackley.current.prob$probability)
    summary(ackley.rperf.C)
    ackley.rcyc.F = lm(ackley.future.prob$cycles ~ ackley.future.prob$probability)
    summary(ackley.rcyc.F)
    ackley.rperf.F = lm(ackley.future.prob$performance ~ ackley.future.prob$probability)
    summary(ackley.rperf.F)
    
# Plot Data --------------------------------------------------------------------
    
    # Generate scatterplots
    plot(ackley.current$cycles,ackley.current$performance)
    plot(ackley.future$cycles,ackley.future$performance)
    plot(ackley.best$cycles,ackley.best$performance)
    
    # Generate ackley histograms
    hist(ackley.current$cycles)
    hist(ackley.future$cycles)
    hist(ackley.best$cycles)
    hist(ackley.current$performance)
    hist(ackley.future$performance)
    hist(ackley.best$performance)

    # Plot future mean performances
    mfp00 = mean(ackley$performance[ackley$probability == 0 & ackley$method == "future_est"])
    mfp01 = mean(ackley$performance[ackley$probability == 0.1 & ackley$method == "future_est"])
    mfp02 = mean(ackley$performance[ackley$probability == 0.2 & ackley$method == "future_est"])
    mfp03 = mean(ackley$performance[ackley$probability == 0.3 & ackley$method == "future_est"])
    mfp04 = mean(ackley$performance[ackley$probability == 0.4 & ackley$method == "future_est"])
    mfp05 = mean(ackley$performance[ackley$probability == 0.5 & ackley$method == "future_est"])
    mfp06 = mean(ackley$performance[ackley$probability == 0.6 & ackley$method == "future_est"])
    mfp07 = mean(ackley$performance[ackley$probability == 0.7 & ackley$method == "future_est"])
    mfp08 = mean(ackley$performance[ackley$probability == 0.8 & ackley$method == "future_est"])
    mfp09 = mean(ackley$performance[ackley$probability == 0.9 & ackley$method == "future_est"])
    mfp10 = mean(ackley$performance[ackley$probability == 1.0 & ackley$method == "future_est"])
    
    probs = c(0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0)
    mfps = c(mfp00,mfp01,mfp02,mfp03,mfp04,mfp05,mfp06,mfp07,mfp08,mfp09,mfp10)
    plot(probs,mfps)
    
    # Plot future mean cycles
    mfc00 = mean(ackley$cycles[ackley$probability == 0 & ackley$method == "future_est"])
    mfc01 = mean(ackley$cycles[ackley$probability == 0.1 & ackley$method == "future_est"])
    mfc02 = mean(ackley$cycles[ackley$probability == 0.2 & ackley$method == "future_est"])
    mfc03 = mean(ackley$cycles[ackley$probability == 0.3 & ackley$method == "future_est"])
    mfc04 = mean(ackley$cycles[ackley$probability == 0.4 & ackley$method == "future_est"])
    mfc05 = mean(ackley$cycles[ackley$probability == 0.5 & ackley$method == "future_est"])
    mfc06 = mean(ackley$cycles[ackley$probability == 0.6 & ackley$method == "future_est"])
    mfc07 = mean(ackley$cycles[ackley$probability == 0.7 & ackley$method == "future_est"])
    mfc08 = mean(ackley$cycles[ackley$probability == 0.8 & ackley$method == "future_est"])
    mfc09 = mean(ackley$cycles[ackley$probability == 0.9 & ackley$method == "future_est"])
    mfc10 = mean(ackley$cycles[ackley$probability == 1.0 & ackley$method == "future_est"])
    
    mfcs = c(mfc00,mfc01,mfc02,mfc03,mfc04,mfc05,mfc06,mfc07,mfc08,mfc09,mfc10)
    plot(probs,mfcs)    
        
    # Plot best mean performances
    mbp00 = mean(ackley$performance[ackley$probability == 0 & ackley$method == "best_est"])
    mbp01 = mean(ackley$performance[ackley$probability == 0.1 & ackley$method == "best_est"])
    mbp02 = mean(ackley$performance[ackley$probability == 0.2 & ackley$method == "best_est"])
    mbp03 = mean(ackley$performance[ackley$probability == 0.3 & ackley$method == "best_est"])
    mbp04 = mean(ackley$performance[ackley$probability == 0.4 & ackley$method == "best_est"])
    mbp05 = mean(ackley$performance[ackley$probability == 0.5 & ackley$method == "best_est"])
    mbp06 = mean(ackley$performance[ackley$probability == 0.6 & ackley$method == "best_est"])
    mbp07 = mean(ackley$performance[ackley$probability == 0.7 & ackley$method == "best_est"])
    mbp08 = mean(ackley$performance[ackley$probability == 0.8 & ackley$method == "best_est"])
    mbp09 = mean(ackley$performance[ackley$probability == 0.9 & ackley$method == "best_est"])
    mbp10 = mean(ackley$performance[ackley$probability == 1.0 & ackley$method == "best_est"])
    
    probs = c(0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0)
    mbps = c(mbp00,mbp01,mbp02,mbp03,mbp04,mbp05,mbp06,mbp07,mbp08,mbp09,mbp10)
    plot(probs,mbps)
    
    # Plot best mean cycles
    mbc00 = mean(ackley$cycles[ackley$probability == 0 & ackley$method == "best_est"])
    mbc01 = mean(ackley$cycles[ackley$probability == 0.1 & ackley$method == "best_est"])
    mbc02 = mean(ackley$cycles[ackley$probability == 0.2 & ackley$method == "best_est"])
    mbc03 = mean(ackley$cycles[ackley$probability == 0.3 & ackley$method == "best_est"])
    mbc04 = mean(ackley$cycles[ackley$probability == 0.4 & ackley$method == "best_est"])
    mbc05 = mean(ackley$cycles[ackley$probability == 0.5 & ackley$method == "best_est"])
    mbc06 = mean(ackley$cycles[ackley$probability == 0.6 & ackley$method == "best_est"])
    mbc07 = mean(ackley$cycles[ackley$probability == 0.7 & ackley$method == "best_est"])
    mbc08 = mean(ackley$cycles[ackley$probability == 0.8 & ackley$method == "best_est"])
    mbc09 = mean(ackley$cycles[ackley$probability == 0.9 & ackley$method == "best_est"])
    mbc10 = mean(ackley$cycles[ackley$probability == 1.0 & ackley$method == "best_est"])
    
    mbcs = c(mbc00,mbc01,mbc02,mbc03,mbc04,mbc05,mbc06,mbc07,mbc08,mbc09,mbc10)
    plot(probs,mbcs)
    
    # Plot current vs future vs best
    means.cbf = data.frame(x=c("current","best","future"),y=c(mfc00,mbc10,mfc10),z=c(mfp00,mbp10,mfp10))

    qplot(x=means.cbf$x,y=means.cbf$y)
    qplot(x=means.cbf$x,y=means.cbf$z)
    
    plot(probs, mfps, col=1)
    points(probs, mbps, col=2)
    