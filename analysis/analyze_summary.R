# Setup ------------------------------------------------------------------------

    # Clear the environment and console
    rm(list = ls())
    cat("\014")
    options(width = 1000)
    
    # Import libraries
    library(ggplot2)
    library(fitdistrplus)
    
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
    sphere.current = sphere[sphere$probability == 0,]
    sphere.future = sphere[sphere$probability == 1,]
    ackley.current = ackley[ackley$probability == 0,]
    ackley.future = ackley[ackley$probability == 1,]
    rosen.current = rosen[rosen$probability == 0,]
    rosen.future = rosen[rosen$probability == 1,]
    stybtang.current = stybtang[stybtang$probability == 0,]
    stybtang.future = stybtang[stybtang$probability == 1,]

    # Slice data by probability
    sphere.prob = sphere[sphere$performance > 0 & sphere$probability < 1,]
    ackley.prob = ackley[ackley$performance > 0 & ackley$probability < 1,]
    rosen.prob = rosen[rosen$performance > 0 & rosen$probability < 1,]
    stybtang.prob = stybtang[stybtang$performance > 0 & stybtang$probability < 1,]

    # Create scatterplot data
    sphere.scatter = sphere[,c(3,4)]
    ackley.scatter = ackley[,c(3,4)]
    rosen.scatter = rosen[,c(3,4)]
    stybtang.scatter = stybtang[,c(3,4)]
    
# Perform Analyses -------------------------------------------------------------

    # Sphere T-Tests
    sphere.tcyc.CF = t.test(sphere.current$cycles,sphere.future$cycles)
    sphere.tcyc.CF
    sphere.tperf.CF = t.test(sphere.current$performance,sphere.future$performance)
    sphere.tperf.CF
    
    # Ackley T-Tests
    ackley.tcyc.CF = t.test(ackley.current$cycles,ackley.future$cycles)
    ackley.tcyc.CF
    ackley.tperf.CF = t.test(ackley.current$performance,ackley.future$performance)
    ackley.tperf.CF
    
    # Rosenbrock T-Tests
    rosen.tcyc.CF = t.test(rosen.current$cycles,rosen.future$cycles)
    rosen.tcyc.CF
    rosen.tperf.CF = t.test(rosen.current$performance,rosen.future$performance)
    rosen.tperf.CF
        
    # Styblinski-Tang T-Tests
    stybtang.tcyc.CF = t.test(stybtang.current$cycles,stybtang.future$cycles)
    stybtang.tcyc.CF
    stybtang.tperf.CF = t.test(stybtang.current$performance,stybtang.future$performance)
    stybtang.tperf.CF
    
    # Run regression on intermediate data (probability = 0.1 to 0.9)
    ackley.rcyc.C = lm(ackley.prob$cycles ~ ackley.prob$probability)
    summary(ackley.rcyc.C)
    ackley.rperf.C = lm(ackley.prob$performance ~ ackley.prob$probability)
    summary(ackley.rperf.C)
    
# Plot Data --------------------------------------------------------------------
    
    # Generate scatterplots
    plot(ackley.current$cycles,ackley.current$performance)
    plot(ackley.future$cycles,ackley.future$performance)
    
    # Generate ackley histograms
    hist(ackley.current$cycles)
    hist(ackley.future$cycles)
    hist(ackley.current$performance)
    hist(ackley.future$performance)

    # Plot future mean performances
    mfp00 = mean(ackley$performance[ackley$probability == 0])
    mfp01 = mean(ackley$performance[ackley$probability == 0.1])
    mfp02 = mean(ackley$performance[ackley$probability == 0.2])
    mfp03 = mean(ackley$performance[ackley$probability == 0.3])
    mfp04 = mean(ackley$performance[ackley$probability == 0.4])
    mfp05 = mean(ackley$performance[ackley$probability == 0.5])
    mfp06 = mean(ackley$performance[ackley$probability == 0.6])
    mfp07 = mean(ackley$performance[ackley$probability == 0.7])
    mfp08 = mean(ackley$performance[ackley$probability == 0.8])
    mfp09 = mean(ackley$performance[ackley$probability == 0.9])
    mfp10 = mean(ackley$performance[ackley$probability == 1.0])
    
    probs = c(0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0)
    mfps = c(mfp00,mfp01,mfp02,mfp03,mfp04,mfp05,mfp06,mfp07,mfp08,mfp09,mfp10)
    plot(probs,mfps)
    
    # Plot future mean cycles
    mfc00 = mean(ackley$cycles[ackley$probability == 0])
    mfc01 = mean(ackley$cycles[ackley$probability == 0.1])
    mfc02 = mean(ackley$cycles[ackley$probability == 0.2])
    mfc03 = mean(ackley$cycles[ackley$probability == 0.3])
    mfc04 = mean(ackley$cycles[ackley$probability == 0.4])
    mfc05 = mean(ackley$cycles[ackley$probability == 0.5])
    mfc06 = mean(ackley$cycles[ackley$probability == 0.6])
    mfc07 = mean(ackley$cycles[ackley$probability == 0.7])
    mfc08 = mean(ackley$cycles[ackley$probability == 0.8])
    mfc09 = mean(ackley$cycles[ackley$probability == 0.9])
    mfc10 = mean(ackley$cycles[ackley$probability == 1.0])
    
    mfcs = c(mfc00,mfc01,mfc02,mfc03,mfc04,mfc05,mfc06,mfc07,mfc08,mfc09,mfc10)
    plot(probs,mfcs)    
    
    # Plot current vs future vs best
    means.cf = data.frame(x=c("current","future"),y=c(mfc00,mfc10),z=c(mfp00,mfp10))

    qplot(x=means.cf$x,y=means.cf$y)
    qplot(x=means.cf$x,y=means.cf$z)
    

    
# Fit distributions ------------------------------------------------------------
    
    # Reduce dataset to get datapoints for distribution fit
    ackley.currfut = ackley[ackley$method == "future_est",c(3,5)]
    plot(ackley.currfut)
    
    # Fit Ackley to piecewise model
    f.lrp <- function(x,a,b,t.x){
        ifelse(x<t.x,a+b*t.x,a+b*x)
    }
    
    ackley.currfut.pw = nls(performance ~ I(exp(1)^(a + b * probability)), data = ackley.currfut, start = list(a=0,b=1),trace=T)
    summary(ackley.currfut.pw)

    plot(probs, mfps)
    
    # Temp exponential model
    fit.future = nls(performance ~ I(exp(1)^(a + b * probability)), data = ackley.currfut, start = list(a=0,b=1),trace=T)
    a <- round(summary(fit.future)$coefficients[1,1],4)
    b <- round(summary(fit.future)$coefficients[2,1],4)
    s <- seq(0,1,length=100)
    lines(s,predict(fit.future,list(probability=s)),lty=1,col=1)
    