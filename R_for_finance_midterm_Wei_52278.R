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

#initial guess of a,b

a = 0.003
b = 0.4
mu = c(a,b)


#generate colum of sigmasquared
df$sigmaSquared = NA
df$sigmaSquared[2:(T-1)] = a + b * (df$logRet[1:(T-2)]^2)

####################################
TT = length(df$logRet)
df$sigmaSquared = NA
df$sigmaSquared[2:(TT)] = a + b * (df$logRet[1:(TT-1)]^2)

objML = function(mu){
  mu[1] = a
  mu[2] = b
  df$sigmaSquared = NA
  df$sigmaSquared[2:(TT)] = a + b * (df$logRet[1:(TT-1)]^2)
  obj = 0
  for (t in 2:TT){
    obj = obj + -log(2*pi*df$sigmaSquared[t])/2 - df$logRet[t]^2/(2*df$sigmaSquared[t])
    obj
  }
  -obj
}

test1 = objML(mu)
test1

optim(c(0.01, 0.004),objML)
nlminb(c(0.01, 0.004), objML, lower = 0.0001, upper = Inf)