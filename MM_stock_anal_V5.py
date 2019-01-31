# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 20:35:53 2018

@author: freakylemon
"""
import datetime as dt
import pandas as pd
import numpy as np
from math import sqrt, log
from linearmodels.panel import PooledOLS

ddd = pd.read_pickle('./MM_stock_data_FINAL.pkl')
ddd.columns



#这个列表 里面有所有的ticker
ttic = []
for char in ddd['Open'][:0]:
    ttic.append(char)

#这部分可以重复用-- 
#检索方法-- rolPrix[Ticker-- ][]
rolTemp = {}
for i in range (1, 13):
    rolTemp[i] = ddd[ddd.index.month == i]['Adj Close']
rolPrix = {}
for char in ttic: 
    rolPrix[char] = []
    for i in range(1, 13):
        rolPrix[char].append(rolTemp[i][char])
#这里我得到了 一个 dictionary-- 用ticker 分类-- 
# 每个ticker 里面 有12个月的adj close 价格-- 接下来--要得到的是-- 
##对数价格-- 
for char in ttic:
    for i in range(0, 12):
        for x in range(0, len(rolPrix[char][i])):
            rolPrix[char][i][x] = log(rolPrix[char][i][x]) 
#接下来用pct change！！！！
#现在 rolPrix 里面的数都是对数价格惹！！！

'''A. illiquidity ratio'''
# absolute value of daily return
adTemp = {}
for i in range (1, 13):
    adTemp[i] = ddd[ddd.index.month == i]['Adj Close']
adTempp = {}
for char in ttic: 
    adTempp[char] = []
    for i in range(1, 13):
        adTempp[char].append(adTemp[i][char])
        
adTempp['AY'][11]

### 重复项###
'''daily trading volume'''
dtvTemp = {}
for i in range (1, 13):
    dtvTemp[i] = ddd[ddd.index.month == i].Volume.mean()
dTrVo = {}
for char in ttic: 
    dTrVo[char] = []
    for i in range(1, 13):
        dTrVo[char].append(dtvTemp[i][char])
###重复项###

adRe = {}
for char in ttic: 
    adRe[char] = []
    for i in range(0,12):
        adRe[char].append([])
        for x in range( 1, len(adTempp[char])):
            adRe[char][i] = 0
            d = abs(adTempp[char][i][x] /adTempp[char][i][x - 1] - 1)
            e = dTrVo[char][i]
            adRe[char][i] += d/e * (1/ (len(adTempp[char])- 1))

#for char in ttic: 
#    for i in range(0,12):
#        adRe[char][i] = adRe[char][i]/ (len(adTempp[char]) - 1)


'''Abdi and Ranaldo estimator of the effective spread'''
#to Get high price-- 
arHighTemp = {}
for i in range (1, 13):
    arHighTemp[i] = ddd[ddd.index.month == i]['High']
arHigh = {}
for char in ttic: 
    arHigh[char] = []
    for i in range(1, 13):
        arHigh[char].append(arHighTemp[i][char])

arLowTemp = {}
for i in range (1, 13):
    arLowTemp[i] = ddd[ddd.index.month == i]['Low']
arLow = {}
for char in ttic: 
    arLow[char] = []
    for i in range(1, 13):
        arLow[char].append(arLowTemp[i][char])

#这是ηt
arMidd = {}
for char in ttic:
    arMidd[char] = []
    for i in range(0, 12):
        arMidd[char]. append([])
for char in ttic:
    for i in range(0, 12):
        for x in range(0, len(arHigh[char][i])):
            arMidd[char][i].append(log(0.5 * (arHigh[char][i][x] + arLow[char][i][x])))

arMidd['AY'][11]

#η_t - 1
armLag = {}
for char in ttic:
    armLag[char] = []
    for i in range(0, 12):
        armLag[char]. append([])
for char in ttic:
    for i in range(0, 12):
        armLag[char][i] = [np.nan] + arMidd[char][i][0: len(arMidd[char][i]) - 1]

#effective spread
arES = {}
for char in ttic:
    arES[char] = [] 
    for i in range(0, 12):
        a = rolPrix[char][i] - arMidd[char][i]
        b = rolPrix[char][i] - armLag[char][i]
        c = np.cov(a, b)
        arES[char]. append( 2 * sqrt( c[0][0]))

arES['AY']

'''Roll's effective spread '''
#得到一个新的dictionary -- 
##这里的都是Δpt = log(pt) - log(pt-1)
rolPrixN = {}
for char in ttic:
    rolPrixN[char] = []
    for i in range(0, 12):
        rolPrixN[char].append([]) 

for char in ttic:
    for i in range(0, 12):
        for x in range(1, len(rolPrix[char][i]) ):
            rolPrixN[char][i].append(rolPrix[char][i][x] - rolPrix[char][i][x - 1] )

esRol = {}
for char in ttic:
    esRol[char] = []
    for i in range(0, 12):
#        lagL = [np.nan] + rolPrixN[char][i][1:len(rolPrixN[char][i])]
        lagL = [np.nan] + rolPrixN[char][i][0 :len(rolPrixN[char][i]) - 1]
        covRol = np.cov(rolPrixN[char][i], lagL)
        esRol[char].append(2 * sqrt(covRol[0][0]))

'''average daily market cap'''
admTemp = {}
for i in range (1, 13):
    admTemp[i] = ddd[ddd.index.month == i].MarketCap.mean()
dMaCa = {}
for char in ttic: 
    dMaCa[char] = []
    for i in range(1, 13):
        dMaCa[char].append(admTemp[i][char])

'''daily trading volume'''
dtvTemp = {}
for i in range (1, 13):
    dtvTemp[i] = ddd[ddd.index.month == i].Volume.mean()
dTrVo = {}
for char in ttic: 
    dTrVo[char] = []
    for i in range(1, 13):
        dTrVo[char].append(dtvTemp[i][char])
        
'''Daily Volatility-- I made it in average''' 
pp = {}
for i in range (1,13):
#    tempVol = []
    tempVol = ddd[ddd.index.month == i]['Adj Close'].std()
    pp[i]= tempVol
vVol = dict()
for char in ttic:
    vVol[char] = []
    for i in range (1,13):
        vVol[char].append(pp[i][char])

'''average daily value of the inverse of the price'''
advTemp = {}
for i in range (1, 13):
    advTemp[i] = (1/ ddd[ddd.index.month == i]['Adj Close']).mean()
dTrVa = {}
for char in ttic: 
    dTrVa[char] = []
    for i in range(1, 13):
        dTrVa[char].append(advTemp[i][char])

'''correlation matrix btw all variables '''
esRol_pd = pd.DataFrame.from_dict(esRol)
esRol.get('AY')
esRol_pd.info()
esRol_pd.columns

arES_pd = pd.DataFrame.from_dict(arES)
arES.get('AY')

adRe_pd = pd.DataFrame.from_dict(adRe)
adRe.get('AY') #??????

dMaCa_pd = pd.DataFrame.from_dict(dMaCa)
dMaCa.get('AY')

dTrVo_pd = pd.DataFrame.from_dict(dTrVo)
dTrVo.get('AY')

vVol_pd = pd.DataFrame.from_dict(vVol)
vVol.get('AY')

dTrVa_pd = pd.DataFrame.from_dict(dTrVa)
dTrVa.get('AY')

#corrMat = pd.concat([esRol_pd['AY'], 
#           arES_pd['AY'], 
#           adRe_pd['AY'], 
#           dMaCa_pd['AY'], 
#           dTrVo_pd['AY'], 
#           vVol_pd['AY'], 
#           dTrVa_pd['AY']], 
#    axis=1, 
#    keys=['esRol_pd', 
#          'arES_pd',
#          'adRe_pd',
#          'dMaCa_pd',
#          'dTrVo_pd',
#          'vVol_pd', 
#          'dTrVa_pd',])
#corrMatt = corrMat.corr()

corrMattt = {}
for char in ttic:
    corrMattt[char] = []
    corrMat = pd.concat([
               esRol_pd[char], 
               arES_pd[char], 
               adRe_pd[char], 
               dMaCa_pd[char], 
               dTrVo_pd[char], 
               vVol_pd[char], 
               dTrVa_pd[char]], 
        axis=1, 
        keys=['esRol_pd', 
              'arES_pd',
              'adRe_pd',
              'dMaCa_pd',
              'dTrVo_pd',
              'vVol_pd', 
              'dTrVa_pd',])
    corrMatt = corrMat.corr()
    corrMattt[char] = corrMatt

#Pooled regression:
    #https://bashtage.github.io/linearmodels/doc/panel/examples/examples.html
#这里有问题…… 我不会pooled OLS……
pReg = pd.concat([dMaCa_pd['AY'], 
           dTrVo_pd['AY'], 
           vVol_pd['AY']])
pRegg = PooledOLS(esRol_pd['AY'], pReg)
pooled_res = pRegg.fit()