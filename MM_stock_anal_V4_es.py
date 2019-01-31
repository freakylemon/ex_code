# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 20:35:53 2018

@author: freakylemon
"""
import datetime as dt
import pandas as pd
import numpy as np
from math import sqrt, log

ddd = pd.read_pickle('./MM_stock_data_FINAL.pkl')
ddd.columns
#ddd[ddd.index.month == 3]['Adj Close']['AY']

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
            d = abs(adTempp[char][i][x] /adTempp[char][i][x - 1] - 1)
            e = dTrVo[char][i]
            adRe[char][i]. append(d/e)

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

#用这个方法好像会出问题-- 重来把-- 
#arMid = {}
#for char in ttic:
#    arMid[char] = []
#    for i in range(0, 12):
#        arMid[char].append( 0.5 * (arHigh[char][i] + arLow[char][i]))
##转换为对数价格
#for char in ttic:
#    for i in range(0, 12):
#        for x in range(1, len(arMid[char][i]) ):
#            arMid[char][i][x] = log(arMid[char][i][x])


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
#        if covRol > 0:
#            covRol = 0

#
#type(rolPrixN['AY'][11])
#
#ppp = np.nan
#e = [np.nan] + rolPrixN['AY'][11][1:len(rolPrixN['AY'][11])]
#b = np. cov(rolPrixN['AY'][11], e)
#c = 2 * sqrt(- np.cov(rolPrixN['AY'][11][3] - rolPrixN['AY'][11][2]))

#TEST
#log(rolPrix['AY'][3][7])
#len(rolPrix['AY'][11])
#for i in range(0, len(rolPrix['AY'][3])):
#    print(log(rolPrix['AY'][3][i]))
##TEST ENDS
#    
#type(rolPrix['AY'][3])
#
#for x in range(0, 19):
#    print(x) 
    
#刚刚出问题 是因为-- 价格-- dictionary 只能由key value（可以是列表）
#这里只能出来 一个dictionary 的对数价格-- 但是-- 日期index 没有了……
#rolPrixN = {}
#for char in ttic:
#    rolPrixN[char] = []
#    for i in range(0, 12):
#        for x in range(0, len(rolPrix[char][i])):
#            rolPrixN[char].append(log(rolPrix[char][i][x]))

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


'''average daily value of the inverse of the price'''
advTemp = {}
for i in range (1, 13):
    advTemp[i] = (1/ ddd[ddd.index.month == i]['Adj Close']).mean()
dTrVa = {}
for char in ttic: 
    dTrVa[char] = []
    for i in range(1, 13):
        dTrVa[char].append(advTemp[i][char])
        
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


#avvList = []
#for char in ttic:
#    avv = 0
#    for i in range(1, 13):
#        avv += (pp[i][char])
#    avvList.append(avv/12)    

#这里是一种方法 存储-- ticker-volatility pair
#avvDic = {}
#i = 0
#for char in ttic:
#    if i < 30:
#        avvDic[char] = avvList[i] 
#        i += 1
##这是另一种方法-- 存储-- ticker-volatility pair
#ppp = pd.DataFrame([avvList], columns = [char for char in ttic], index = ['Volatility']).T
##我碰到了问题-- 为什么 dataframe 是列-- 不能是行-- 
#ppp['dailyTradingVolume'] = dtrvo
#ppp['avDailyValue'] = list1

'''Roll's Effective Spread??'''
