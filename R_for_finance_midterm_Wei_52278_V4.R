###################
####### 1a ########
###################

# read data
a = 'https://sites.google.com/site/czellarveronika/NKE.txt'
A = read.table(a, 
               header = TRUE,
               sep = '\t')
# calculate log return
T = length(A$AdjClose)
A$logRet = NA
A$logRet[2:T] = log(A$AdjClose[2:T]/ A$AdjClose[1:(T - 1)])

df = A[-c(1),] 

rownames(df) = NULL

####################################
TT = length(df$logRet)

# repeat and modified
# set return data default
objML2 = function(x){
  set.seed(1)
#  rsim = rep(0, (TT-1))
  rt = df$logRet
  c = x[1]
  d = x[2]
  term1 = rep(0, (TT-1))
  term2 = rep(0, (TT-1))
  for (t in 1:(TT-1)){
    term1[t] = 0.5*log(2*pi*(c+d*rt[t]^2))
 #   rsim[t] = sqrt(c+d*rt[t]^2) * rnorm(1)
    term2[t] = (rt[t+1]^2)/(2*(c+d*rt[t]^2))
  }
  sum(term1) + sum(term2)
}

test1 = objML2(c(0.001,0.00003))
test1

# numerical optimization with 2 methods.
optim(c(1,3),objML2)
paraArch = nlminb(c(0.001,0.00003),objML2)$par

###################
####### 1b ########
###################

# to predict logRet on 4-Jan-2016
# to generate a column of sigma_t
# generate a column of log return based on 95% VaR
df$sigmaSim = NA
df$VaR = NA

for (t in 2:(TT)){
  set.seed(1)
  df$sigmaSim[t] = sqrt(paraArch[1] + paraArch[2] * df$logRet[t-1]^2)
  df$VaR[t] = -qnorm(0.05, 0, df$sigmaSim[t])
}

###################
####### 1c ########
###################

#a = st[E$Date == strptime('01/02/2013', format = '%m/%d/%Y')]
#df[df$Date == strptime('1/4/2016', format='%m/%d/%Y')]
df$Date = strptime(df$Date, format='%m/%d/%Y')

#Data1<-subset(Data, (Date=="16/12/2006" ))
#myData[myData$myDate >= "1970-01-01" & myData$myDate <= "2016-06-27",]
df_1 = subset(df, df$Date>='2016-01-04' & df$Date<='2019-02-27')

df_2 = subset(df_1, df_1$logRet < df_1$VaR)

# so the proportion 
pct =1 - length(df_2$VaR)/length(df_1$VaR)

###################
####### 1d ######## I modified code from V3
###################

sigmaAd = sqrt(paraArch[1] + paraArch[2] * df$logRet[(df$Date == '2019-02-27')]^2)


set.seed(1)
logRSim = sigmaAd * rnorm(10000)

logRSim = as.data.frame(logRSim)

# negative of 95% VaR
nVarAd = qnorm(0.05, 0, sigmaAd)

# 95% expected shortfall
eRt = -mean(logRSim[logRSim < nVarAd])

###################
####### 2a ########
###################


df_2a = subset(df, df$Date>='2010-01-04' & df$Date <='2015-12-31')

T_2a = length(df_2a$logRet)

# repeat and modified
# set return data default
objML_2a = function(x){
  set.seed(1)
  #  rsim = rep(0, (T_2a-1))
  rt = df_2a$logRet
  c = x[1]
  d = x[2]
  term1 = rep(0, (T_2a-1))
  term2 = rep(0, (T_2a-1))
  for (t in 1:(T_2a-1)){
    term1[t] = 0.5*log(2*pi*(c+d*rt[t]^2))
    #   rsim[t] = sqrt(c+d*rt[t]^2) * rnorm(1)
    term2[t] = (rt[t+1]^2)/(2*(c+d*rt[t]^2))
  }
  sum(term1) + sum(term2)
}

test1 = objML_2a(c(0.001,0.00003))
test1

# numerical optimization with 2 methods.
optim(c(1,3),objML_2a)
paraArch_2a = nlminb(c(0.001,0.00003),objML_2a)$par

###################
####### 2b ########
###################

# rt follows laplace distribution with(after study) mu = 0 and b = sqrt(2)/2*sigma

df_2a$sigmaSim = NA
df_2a$VaR = NA

for (t in 2:(T_2a)){
  set.seed(1)
  df_2a$sigmaSim[t] = sqrt(paraArch_2a[1] + paraArch_2a[2] * df_2a$logRet[t-1]^2)
  df_2a$VaR[t] = -qlaplace(0.05, 0, sqrt(2)*df_2a$sigmaSim[t]/2)
}

# below it's the 95% VaR based on sigma at date 2016-01-04 
sigmaAd_2a = sqrt(paraArch_2a[1] + paraArch_2a[2] * df_2a$logRet[df_2a$Date == '2015-12-31']^2)
var_2a = -qlaplace(0.05, 0, sqrt(2)*sigmaAd_2a/2)

###################
####### 2c ########
###################

# load subset data only to obtain date info
df_2c = subset(df, df$Date>='2016-01-04')

# clean data panel
df_2c$sigmaSim = NA
df_2c$VaR = NA

df_2c$sigmaSim[1] = sqrt(paraArch_2a[1] + paraArch_2a[2] * df_2a$logRet[df_2a$Date == '2015-12-31']^2)
df_2c$VaR[1] = -qlaplace(0.05, 0, sqrt(2)*df_2c$sigmaSim[1]/2)

T_2c = length(df_2c$sigmaSim)

for (t in 2:T_2c){
  df_2c$sigmaSim[t] = sqrt(paraArch_2a[1] + paraArch_2a[2] * df_2c$logRet[t-1]^2)
  df_2c$VaR[t] = -qlaplace(0.05, 0, sqrt(2)*df_2c$sigmaSim[t]/2)
}

# df_2 = subset(df_1, df_1$logRet < df_1$rtSim)
# 
# # so the proportion 
# pct =1 - length(df_2$rtSim)/length(df_1$rtSim)

df_2c1 = subset(df_2c, df_2c$logRet < -df_2c$VaR)
pct_2c = length(df_2c1$VaR)/length(df_2c$VaR)

###################
####### 2d ########
###################

sigmaAd_2d = sqrt(paraArch_2a[1] + paraArch_2a[2] * df_2c$sigmaSim[df_2c$Date == '2019-02-27']^2)
set.seed(1)

logRSim_2d = rlaplace(10000, 0, sqrt(2)*sigmaAd_2d/2)
nVarAd_2d = qlaplace(0.05, 0, sqrt(2)*sigmaAd_2d/2)

eRt_2d = -mean(logRSim_2d[logRSim_2d<nVarAd_2d])

###################
####### 4 #########
###################

mean(df_1$VaR) < mean(df_2c$VaR)
