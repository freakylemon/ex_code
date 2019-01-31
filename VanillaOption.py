# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 21:54:45 2018

@author: freakylemon
"""

import datetime as dt
import math
from scipy import stats
from scipy import optimize
class vanillaOption(object):
    def __init__(self,payoffType, k, expiryDate, equityTicker, numOptions):
        if payoffType not in ['CALL', 'PUT']:
            print ('please enter CALL or PUT' )
        
        self.payoffType = str(payoffType)
        self.k = float(k)
        self.expiryDate = expiryDate
        self.equityTicker = str(equityTicker)
        self.numOptions = int(numOptions)
        
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
        T = (self.expiryDate - valuationDate).days/365.242
        d1 = (math.log(s0/(self.k)) + (rf + sigma*sigma/2)*T)/(sigma*math.sqrt(T))
        d2 = d1 - sigma* math.sqrt(T)

        if self.payoffType == 'PUT':
            nd1p =stats.norm.cdf(-d1,0.0,1.0)
            nd2p =stats.norm.cdf(-d2,0.0,1.0)
            putOp = self.k*math.exp(-rf *T)*nd2p - s0*nd1p
            return putOp
        elif self.payoffType == 'CALL':
            nd1 = stats.norm.cdf(d1,0.0,1.0)
            nd2 = stats.norm.cdf(d2,0.0,1.0)
            callOp = s0*nd1 - self.k*math.exp(-rf *T)*nd2
            return callOp
        else: 
            print('please enter only call or put')
    
    '''3.d_'''    
    def delta(self,valuationDate, s0, sigma, rf):
        '''delta  == dV/dS- stock price drift 0.0001'''
        s0m = s0 + 0.0001 #drift
        T = (self.expiryDate - valuationDate).days/365.242    
        d1 = (math.log(s0/(self.k)) + (rf + sigma*sigma/2)*T)/(sigma*math.sqrt(T))
        d2 = d1 - sigma* math.sqrt(T)
        d1m = (math.log(s0m/(self.k)) + (rf + sigma*sigma/2)*T)/(sigma*math.sqrt(T))
        d2m = d1m - sigma* math.sqrt(T)
        if self.payoffType == 'PUT':
            nd1p =stats.norm.cdf(-d1,0.0,1.0)
            nd2p =stats.norm.cdf(-d2,0.0,1.0)
            putOp = self.k * math.exp(-rf * T) * nd2p - s0 * nd1p
            
            nd1pm =stats.norm.cdf(-d1m,0.0,1.0)
            nd2pm =stats.norm.cdf(-d2m,0.0,1.0)
            putOpm = self.k * math.exp( -rf * T ) * nd2pm - s0m * nd1pm
            deltaa = (putOpm - putOp) / (s0m - s0)
            return deltaa
        elif self.payoffType == 'CALL':
            nd1 = stats.norm.cdf(d1,0.0,1.0)
            nd2 = stats.norm.cdf(d2,0.0,1.0)
            callOp = s0*nd1 - self.k*math.exp(-rf *T)*nd2
            
            nd1m= stats.norm.cdf(d1m,0.0,1.0)
            nd2m = stats.norm.cdf(d2m,0.0,1.0)
            callOpm = s0m * nd1m - self.k * math.exp( -rf * T) * nd2m
            deltaa = (callOpm - callOp) / (s0m - s0)
            return deltaa
        else: 
            print('please enter only CALL or PUT')
            
    '''3.e_'''
    def gamma(self,valuationDate, s0, sigma, rf):
        '''def gamma = d'delta / dS'''
        '''这里的delta 我用了N(d1)来算吧'''
        s0m = s0 + 0.0001 #drift
        T = (self.expiryDate - valuationDate).days/365.242    
        d1 = (math.log(s0/(self.k)) + (rf + sigma*sigma/2)*T)/(sigma*math.sqrt(T))
        d1m = (math.log(s0m/(self.k)) + (rf + sigma*sigma/2)*T)/(sigma*math.sqrt(T))
        
        if self.payoffType == 'PUT':
            nd1p =stats.norm.cdf(-d1,0.0,1.0)
            nd1pm =stats.norm.cdf(-d1m,0.0,1.0)
            gammaa = (nd1pm - nd1p)/ (s0m - s0)
            return gammaa
        elif self.payoffType == 'CALL':
            nd1 = stats.norm.cdf(d1,0.0,1.0)
            nd1m= stats.norm.cdf(d1m,0.0,1.0)
            gammaa = (nd1m - nd1) / (s0m - s0)
            return gammaa
        else: 
            print('please enter only CALL or PUT')
    '''3.h_1_'''
    '''self . k/ expiryDate'''
    def impliedVolatility(self,sigma, s0, optionPrice, rf):

        valuationDate = dt.date(2018,3,20)
        
        T = (self.expiryDate - valuationDate).days/365.242
        d1 = (math.log(s0/(self.k)) + (rf + sigma*sigma/2)*T)/(sigma*math.sqrt(T))
        d2 = d1 - sigma* math.sqrt(T)
        if self.payoffType == 'PUT':    
            nd1p =stats.norm.cdf(-d1,0.0,1.0)
            nd2p =stats.norm.cdf(-d2,0.0,1.0)
            putOp = self.k * math.exp(-rf * T) * nd2p - s0 * nd1p
            return (optionPrice - putOp)
                
        elif self.payoffType == 'CALL':
            nd1 = stats.norm.cdf(d1,0.0,1.0)
            nd2 = stats.norm.cdf(d2,0.0,1.0)
            callOp = s0*nd1 - self.k*math.exp(-rf *T)*nd2
            return (optionPrice - callOp)
            #这里我没有用newtonfunction               
        
            
'''3.i_ '''
if __name__ == '__main__':
    '''3.h_2_'''
    ''''TEST implied volatility'''
    ppput = vanillaOption('CALL',100,dt.date(2018,9,20),'APPL',10)
    
    sigma = 0.2
    s0 = 100
    optionPrice = 11.1
    rf = 0.05
    ccc = optimize.newton(ppput.impliedVolatility, \
                          sigma, \
                          args = (s0, optionPrice, rf,), \
                          tol = 10 ** (-5), \
                          maxiter = 100000)
    print (ccc)         
    '''测试结束'''         
    
    '''TO TEST DELTA'''
    pput = vanillaOption('call',100,dt.date(2018,9,20),'APPL',10)
    cc = pput.delta(dt.date(2018,3,20), 100, 0.2, 0.05)
    pput.print()
    print (cc)
    '''test ends'''
    
    '''3.f_start'''
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(25, 22))
    inits0 = [x for x in range(80,121,5)]
    print(len(inits0))
    exDate = [dt.date(2018,7,20),dt.date(2018,9,20),dt.date(2018,12,20)]
    
    legends = []
    legends.append('2018/07/20 PUT')
    legends.append('2018/07/20 CALL')
    legends.append('2018/09/20 PUT')
    legends.append('2018/09/20 CALL')
    legends.append('2018/12/20 PUT')
    legends.append('2018/12/20 CALL')
    
    for tt in exDate:
        liPut = []
        liCall = []
        for ini in inits0:
            loPut = vanillaOption('PUT',100,tt,'APPL',10)
            liPut.append(loPut.price(dt.date(2018,6,20),ini,0.20,0.05))
            loCall = vanillaOption('CALL',100,tt,'APPL',10)
            liCall.append(loCall.price(dt.date(2018,6,20),ini,0.20,0.05)) 
        #fig = plt.figure(figsize=(15, 12))#没有他就可以把所有的线都放在一个图里面惹~~~
            
        plt.plot(inits0,liPut)
        plt.plot(inits0,liCall)
        
    plt.legend(legends)    
    plt.xlabel('Terminal stock price')
    plt.ylabel('Option value')
    

    '''ENDS_ RECOVER WITH ctrl + 1 '''
    
    '''3.g_'''
    sigma = 0.2
    rf = 0.05
    s0 = 100
    k = range(80,121,5)
    pType = ['PUT','CALL']
    tot = {'price':[],'delta':[],'gamma':[]}
    for tt in exDate: # different expiry date
        for ty in pType: #different payoff type
            for i in k: #different strike price
                calDGP = vanillaOption(ty,i,tt,'APPL',10)
                pr = calDGP.price(dt.date(2018,6,20),s0,sigma,rf)
                dlt = calDGP.delta(dt.date(2018,6,20),s0,sigma,rf)
                gma = calDGP.gamma(dt.date(2018,6,20),s0,sigma,rf)
                print ("when srike price is %5.3f, \
                       payoff type is %s, \
                       expiry date is %s, \
                       price is %1.3f, delta is %3.3f, gamma is %5.3f. " %(i, ty, tt, pr, dlt, gma))
    '''ENDS_ '''

        
