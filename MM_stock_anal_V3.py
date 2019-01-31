# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 20:35:53 2018

@author: freakylemon
"""
import datetime as dt
import pandas as pd
import numpy as np
from math import sqrt, log, sqrt

ddd = pd.read_pickle('./MM_stock_data_FINAL.pkl')
ddd.columns
#ddd[ddd.index.month == 3]['Adj Close']['AY']

#这个列表 里面有所有的ticker
ttic = []
for char in ddd['Open'][:0]:
    ttic.append(char)

'''Roll's effective spread '''
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
rolPrixN = {}
for char in ttic:
    rolPrixN[char] = []
    for i in range(0, 12):
        rolPrixN[char].append([]) 
#得到一个新的dictionary
for char in ttic:
    for i in range(0, 12):
        for x in range(1, len(rolPrix[char][i]) ):
            rolPrixN[char][i].append(rolPrix[char][i][x] - rolPrix[char][i][x - 1] )

esRol = {}
for char in ttic:
    esRol[char] = []
    for i in range(0, 12):
        lagL = [np.nan] + rolPrixN[char][i][1:len(rolPrixN[char][i])]
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
