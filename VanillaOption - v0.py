# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 21:54:45 2018

@author: freakylemon
"""

"""
疑问： 

"""
import scipy
import datetime as dt
import math
from scipy import stats
class vanillaOption(object):
    def __init__(self,payoffType, k, expiryDate, equityTicker, numOptions):
        self.payoffType = payoffType
        self.k = k
        self.expiryDate = expiryDate
        self.equityTicker = equityTicker
        self.numOptions = numOptions
    def  print(self):
        print("here below you find the payoff type as %s, strike price as %s, \
              expiry date of the option is %s, corresponding equity is %s and \
              number of options is %s." \
              %(self.payoffType,self.k,self.expiryDate, \
              self.equityTicker,self.numOptions))
        '''print (payoffType, k, expiryDate, equityTicker, numOptions)'''
    def price(self,valuationDate, s0, sigma, rf):
        '''公式待完善;需要判断valuationDate and sigma'''      
        T = (self.expiryDate - valuationDate).days/365.242
        d1 = (math.log(s0/(self.k)) + (rf + sigma*sigma/2)*T)/(sigma*math.sqrt(T))
        d2 = d1 - sigma* math.sqrt(T)

        if self.payoffType == 'put':
            nd1p =stats.norm.cdf(-d1,0.0,1.0)
            nd2p =stats.norm.cdf(-d2,0.0,1.0)
            putOp = self.k*math.exp(-rf *T)*nd2p - s0*nd1p
            return putOp
        elif self.payoffType == 'call':
            nd1 = stats.norm.cdf(d1,0.0,1.0)
            nd2 = stats.norm.cdf(d2,0.0,1.0)
            callOp = s0*nd1 - self.k*math.exp(-rf *T)*nd2
            return callOp
        else: 
            print('please enter only call or put')
            
    def delta(self,valuationDate, s0, sigma, rf):
        '''delta 要求dV/dS- stock price drift 0.0001'''
        T = (self.expiryDate - valuationDate).days/365.242
        d1 = (math.log(s0/(self.k)) + (rf + sigma*sigma/2)*T)/(sigma*math.sqrt(T))
        delta = stats.norm.cdf(d1,0.0,1.0)
        return delta
    
    def gamma(self,valuationDate, s0, sigma, rf):
        T = (self.expiryDate - valuationDate).days/365.242
        d1 = (math.log(s0/(self.k)) + (rf + sigma*sigma/2)*T)/(sigma*math.sqrt(T))
        delta = stats.norm.cdf(d1,0.0,1.0)
        gamma = math.gamma(delta)
        return gamma
    
    def impliedVolatility(self,valuationDate, optionPrice):
        #https://stackoverflow.com/questions/35391850/implied-volatility-calculation-in-python
        pass    
    
pput = vanillaOption('put',100,dt.date(2018,9,20),'APPL',10)
pput.price(dt.date(2018,3,20),100,0.2,0.05)
#pput.print()


import matplotlib.pyplot as plt
inits0 = [x for x in range(80,121,5)]
print(len(inits0))
exDate = [dt.date(2018,7,20),dt.date(2018,9,20),dt.date(2018,12,20)]

for tt in exDate:
    liPut = []
    liCall = []
    for ini in inits0:
        loPut = vanillaOption('put',100,tt,'APPL',10)
        liPut.append(loPut.price(dt.date(2018,6,20),ini,0.20,0.05))
        loCall = vanillaOption('call',100,tt,'APPL',10)
        liCall.append(loCall.price(dt.date(2018,6,20),ini,0.20,0.05)) 
    #fig = plt.figure(figsize=(5, 2))
    plt.plot(inits0,liPut)
    plt.plot(inits0,liCall)
#    plt.plot(inits0,liPut)
'''这里的问题就是 我把plot放在了循环里面，然后他还是报错说，9-18 xy 轴不匹配'''
'''我不知道delta,gamma公式怎么写'''
#print(liPut,liCall)
#(self,payoffType, k, expiryDate, equityTicker, numOptions):
#price(self,valuationDate, s0, sigma, rf):
sigma = 0.2
rf = 0.05
s0 = 100
k = range(80,121,5)
pType = ['put','call']
tot = {'price':[],'delta':[],'gamma':[]}
for tt in exDate: # different expiry date
    for ty in pType: #different payoff type
        for i in k: #different strike price
            calDGP = vanillaOption(ty,i,tt,'APPL',10)
            pr = calDGP.price(dt.date(2018,6,20),s0,sigma,rf)
            dlt = calDGP.delta(dt.date(2018,6,20),s0,sigma,rf)
            gma = calDGP.gamma(dt.date(2018,6,20),s0,sigma,rf)
            #print (pr,dlt,gma)


        
