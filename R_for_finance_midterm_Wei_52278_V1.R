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
  rt = df$logRet
  c = x[1]
  d = x[2]
  term1 = rep(0, (TT-1))
  term2 = rep(0, (TT-1))
  for (t in 1:(TT-1)){
    term1[t] = 0.5*log(2*pi*(c+d*rt[t]^2))
    term2[t] = (rt[t+1]^2)/(2*(c+d*rt[t]^2))
  }
  sum(term1) + sum(term2)
}

test1 = objML2(c(0.001,0.00003))
test1

# numerical optimization with 2 methods.
optim(c(1,3),objML2)
nlminb(c(0.001,0.00003),objML2)