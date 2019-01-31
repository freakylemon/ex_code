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
    '''3.b_'''
    def  print(self):
        print("here below you find the payoff type as %s, strike price as %s, \
              expiry date of the option is %s, corresponding equity is %s and \
              number of options is %s." \
              %(self.payoffType,self.k,self.expiryDate, \
              self.equityTicker,self.numOptions))
        '''print (payoffType, k, expiryDate, equityTicker, numOptions)'''  
    '''3.c_'''
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
    '''3.d_'''    
    def delta(self,valuationDate, s0, sigma, rf):
        '''delta 要求dV/dS- stock price drift 0.0001'''
        '''DOUBT：N(-d1)?=? N(d1)'''
        '''好像不能在运行时候加引号注释……'''
        s0m = s0 + 0.0001 #drift
        T = (self.expiryDate - valuationDate).days/365.242    
        d1 = (math.log(s0/(self.k)) + (rf + sigma*sigma/2)*T)/(sigma*math.sqrt(T))
        d2 = d1 - sigma* math.sqrt(T)
        d1m = (math.log(s0m/(self.k)) + (rf + sigma*sigma/2)*T)/(sigma*math.sqrt(T))
        d2m = d1m - sigma* math.sqrt(T)
        if self.payoffType == 'put':
            nd1p =stats.norm.cdf(-d1,0.0,1.0)
            nd2p =stats.norm.cdf(-d2,0.0,1.0)
            putOp = self.k * math.exp(-rf * T) * nd2p - s0 * nd1p
            
            nd1pm =stats.norm.cdf(-d1m,0.0,1.0)
            nd2pm =stats.norm.cdf(-d2m,0.0,1.0)
            putOpm = self.k * math.exp( -rf * T ) * nd2pm - s0m * nd1pm
            deltaa = (putOpm - putOp) / (s0m - s0)
            return deltaa
        elif self.payoffType == 'call':
            nd1 = stats.norm.cdf(d1,0.0,1.0)
            nd2 = stats.norm.cdf(d2,0.0,1.0)
            callOp = s0*nd1 - self.k*math.exp(-rf *T)*nd2
            
            nd1m= stats.norm.cdf(d1m,0.0,1.0)
            nd2m = stats.norm.cdf(d2m,0.0,1.0)
            callOpm = s0m * nd1m - self.k * math.exp( -rf * T) * nd2m
            deltaa = (callOpm - callOp) / (s0m - s0)
            return deltaa
        else: 
            print('please enter only call or put')
            
    '''3.e_'''
    def gamma(self,valuationDate, s0, sigma, rf):
        '''def gamma = d'delta / dS'''
        '''这里的delta 我用了N(d1)来算吧'''
        s0m = s0 + 0.0001 #drift
        T = (self.expiryDate - valuationDate).days/365.242    
        d1 = (math.log(s0/(self.k)) + (rf + sigma*sigma/2)*T)/(sigma*math.sqrt(T))
        d1m = (math.log(s0m/(self.k)) + (rf + sigma*sigma/2)*T)/(sigma*math.sqrt(T))
        
        if self.payoffType == 'put':
            nd1p =stats.norm.cdf(-d1,0.0,1.0)
            nd1pm =stats.norm.cdf(-d1m,0.0,1.0)
            gammaa = (nd1pm - nd1p)/ (s0m - s0)
            return gammaa
        elif self.payoffType == 'call':
            nd1 = stats.norm.cdf(d1,0.0,1.0)
            nd1m= stats.norm.cdf(d1m,0.0,1.0)
            gammaa = (nd1m - nd1) / (s0m - s0)
            return gammaa
        else: 
            print('please enter only call or put')
    '''3.h_'''
    '''self . k/ expiryDate'''
    def impliedVolatility(self,valuationDate, s0, optionPrice, rf):
        #https://stackoverflow.com/questions/35391850/implied-volatility-calculation-in-python
        sigma = 0.001
        T = (self.expiryDate - valuationDate).days/365.242
        while sigma < 1:
            d1 = (math.log(s0/(self.k)) + (rf + sigma*sigma/2)*T)/(sigma*math.sqrt(T))
            d2 = d1 - sigma* math.sqrt(T)
            if self.payoffType == 'put':    
                nd1p =stats.norm.cdf(-d1,0.0,1.0)
                nd2p =stats.norm.cdf(-d2,0.0,1.0)
                putOp = self.k * math.exp(-rf * T) * nd2p - s0 * nd1p
                if optionPrice - putOp <0.001:
                    return sigma
                sigma += 0.001
                
            elif self.payoffType == 'call':
                nd1 = stats.norm.cdf(d1,0.0,1.0)
                nd2 = stats.norm.cdf(d2,0.0,1.0)
                callOp = s0*nd1 - self.k*math.exp(-rf *T)*nd2
                if optionPrice - callOp <0.001:
                    return sigma
                sigma += 0.001
            #这里我没有用newtonfunction
            
''''这里测试的是implied volatility'''
#ppput = vanillaOption('call',100,dt.date(2018,9,20),'APPL',10)
#ccc = ppput.impliedVolatility(dt.date(2018,3,20), 100, 11.0, 0.05)
#print (ccc)         
'''测试结束'''         

'''我需要测试一下delta能不能用'''
'''可以输出~~~'''
#pput = vanillaOption('call',100,dt.date(2018,9,20),'APPL',10)
#cc = pput.delta(dt.date(2018,3,20), 100, 0.2, 0.05)
#pput.print()
#print (cc)
'''test ends'''

'''3.f_start'''
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
    fig = plt.figure(figsize=(5, 2))#没有他就可以把所有的线都放在一个图里面惹~~~

    plt.plot(inits0,liPut)
    plt.plot(inits0,liCall)

    plt.plot(inits0,liPut)
'''结束_ 注释用ctrl + 1 恢复'''

'''3.g_'''
#sigma = 0.2
#rf = 0.05
#s0 = 100
#k = range(80,121,5)
#pType = ['put','call']
#tot = {'price':[],'delta':[],'gamma':[]}
#for tt in exDate: # different expiry date
#    
#    for ty in pType: #different payoff type
#        for i in k: #different strike price
#            calDGP = vanillaOption(ty,i,tt,'APPL',10)
#            pr = calDGP.price(dt.date(2018,6,20),s0,sigma,rf)
#            dlt = calDGP.delta(dt.date(2018,6,20),s0,sigma,rf)
#            gma = calDGP.gamma(dt.date(2018,6,20),s0,sigma,rf)
#            tot['price'].append(pr)
#            tot['delta'].append(dlt)
#            tot['gamma'].append(gma)
#            print ("Here below you find answers for 3.g when srike price is %s, \
#                   payoff type is %s, \
#                   expiry date is %s: \
#                   %s, %s, %s. " %(i, ty, tt, pr, dlt, gma))
#print (tot)
'''结束_ '''

        
