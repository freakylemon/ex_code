# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 20:35:53 2018

@author: freakylemon
"""
import datetime as dt
import pandas as pd
import numpy as np
from math import sqrt
ddd = pd.read_pickle('./MM_stock_data_NEW.pkl')
'''问题 raised -- 怎么操作-- 数据-- datetime^ '''
'''Open- High- Low- Close- Adj Close- Volume- '''
#要解决的第一个问题-- 就是参数-- 
#Ticker = [itt for itt in ddd['Open']]
#ddd.iloc[:0]
#ddd['Open'].iloc[:0] #all the Ticker
#ttic = ddd['Open'].iloc[:0].to_string()
#
#ddd['Open'].iloc[0] # Ticker with first openPrice-- 

ddd.columns
ddd['Adj Close']
ddd.High['AY'].unique()
type(ddd['High']['AY'])
retts =ddd['Open'].pct_change() #这里可以得到return！！！！！ 
#rettts = ddd['Open']['AY'].pct_change() 
#仅仅去检查-- 就是 return是一致的
ddd['High']['AY'].describe()
ddd.shape

'''这样的话…… 变成了 dictionary'''
#opBook = {}
##for char in ddd['Open'].iloc[:0]:
#for char in ddd['Open'][:0]:
#    #print(ddd['Open'][char].unique())
#    opBook[char] = ddd['Open'][char].unique()



dddOp = ddd['Open'].as_matrix()
dddOp.iloc[1:10]


'''daily trading volume'''
dtrvo = ddd.Volume.mean()

'''average daily value of the inverse of the price'''
avInvPrice = (1/ ddd['Close']).mean()

'''Daily Volatility-- I made it in average'''
#ddd.index[1] #time
#len(ddd.index)
#
#type(ddd.index)
#
#ddd.index = ddd.index.strftime('%Y %b %d)
#type(ddd.index)

#这里-- 把index变成了string-- 
#ddd.index = ddd.index.to_pydatetime('%Y %b %d')
#这里 -- 并没有变化-- 前后都是一样的type

#def dateConverter(dt):
#    dt = dt.replace('-', ' ')
#    return pd.to_datetime(dt,format = '%Y %m %d', dayfirst = True)
#
#for i in range(0, len(ddd.index)):
#    ddd.index[i] = ddd.index[i].apply(dateConverter)
#ddd['Open']['AY'].sort_index()

#以下出来了一个月的standard deviation
#ddd1 = ddd[(ddd.index >= ('2017-01-01')) & (ddd.index <= ('2017-01-31'))]
#ddd1['Adj Close']. std()

#这个列表 里面有所有的ticker
ttic = []
for char in ddd['Open'][:0]:
    ttic.append(char)

pp = ddd[ddd.index.month == 5]['Adj Close'].std()

# index 中 的年/月/日
pp = {}
for i in range (1,13):
    pp[i] = ddd[ddd.index.month == i]['Adj Close'].std()

#试一下
#pp[4]['AY']

avvList = []
for char in ttic:
    avv = 0
    for i in range(1, 13):
        avv += (pp[i][char])
    avvList.append(avv/12)    

avvDic = {}
i = 0
for char in ttic:
    if i < 30:
        avvDic[char] = avvList[i] 
        i += 1
        
'''Roll's Effective Spread??'''