# -*- coding: utf-8 -*-

"""
Created on Thu Apr  4 00:16:28 2019

@author: freakylemon
"""

import numpy as np
import pandas as pd
from linearmodels import PooledOLS
from scipy.optimize import minimize

# i'll deal with usd
# i'll transfer them to dict
# then use pooled regression
# I finished with the weights calculation



#from return index to return: usd based index
df_rt = pd.read_csv('taa_RI_usd.csv')

df_rt['dates'] = pd.to_datetime(df_rt.dates)

df_rt = df_rt.set_index('dates')

df_rt = df_rt.pct_change(periods=1).reset_index(drop=True)
# double checked

estimates = {}
for i in df_rt.columns:
    estimates[i] = {}
for i in df_rt.columns:
    estimates[i]['rt'] = df_rt[i]





tickers = df_rt.columns
print(tickers)





# dividend yield
df_dy = pd.read_csv('taa_ori_dy.csv')
df_dy['Date'] = pd.to_datetime(df_dy.Date)
df_dy = df_dy.set_index('Date').reset_index(drop=True)
df_dy = df_dy/100

for i in df_dy.columns:
    estimates[i]['dividendYield'] = df_dy[i].shift(1)












# short rates
df_stir = pd.read_csv('taa_ori_short_rates.csv')
df_stir['Name'] = pd.to_datetime(df_stir.Name)

df_stir = df_stir.set_index('Name').reset_index(drop=True)
df_stir = df_stir/100

# used shift so that regressor is at t-1 while regressands is at t
for i in df_stir.columns:
    estimates[i]['shortRates'] = df_stir[i].shift(1)









# slope of term structure
# my understanding... 
df_ts = pd.read_csv('taa_ori_short_rates.csv')

df_ts['Name'] = pd.to_datetime(df_ts.Name)
df_ts = df_ts.set_index('Name').reset_index(drop=True)

df_ts = df_ts.pct_change(periods=1)

# deal with missing informations
df_ts = df_ts.fillna(0)

for i in df_ts.columns:
    for t in range(len(df_ts[i])):
        if df_ts[i][t] == np.NINF:
            df_ts[i][t] = -1
        elif df_ts[i][t] == np.inf:
            df_ts[i][t] = -1

for i in df_ts.columns:
    estimates[i]['slopeTermstructure'] = df_ts[i].shift(1)










# MVOL- usd
df_mvol = pd.read_csv('TAA_RI_us $_daily_1.csv')

df_mvol['dates'] = pd.to_datetime(df_mvol.dates)

df_mvol = df_mvol.set_index('dates')
df_mvol = df_mvol.pct_change(periods=1)

df_mvol = df_mvol.groupby(pd.Grouper(level='dates', freq='1M')).std() # groupby each 1 month
df_mvol = df_mvol[:431].reset_index(drop=True)


for i in df_mvol.columns:
    estimates[i]['monthlyVolatility'] = df_mvol[i].shift(1)











# momentum, 12-month, usd, 
# df_3 = pd.read_csv('taa_RI_usd.csv')
df_mom = pd.read_csv('taa_RI_usd.csv')
df_mom['dates'] = pd.to_datetime(df_mom.dates)
df_mom = df_mom.set_index('dates').reset_index(drop=True)

df_mom = df_mom.pct_change(periods=12)

for i in df_mom.columns:
    for t in range(len(df_mom[i])):
        if df_mom[i][t] < 0:
            df_mom[i][t] = -1
        elif df_mom[i][t] >= 0:
            df_mom[i][t] = 1
        else:
            df_mom[i][t] = np.nan        
df_mom = df_mom.shift(periods=1)

df_mom =df_rt * df_mom


for i in df_mom.columns:
    estimates[i]['12mthMomentum'] = df_mom[i].shift(1)


















# here below I start pooling data
    
# loop below takes almost 5 mins to finish, CAREFUL
resReg = {} # should be 357......
for t in range(356): #430 lines of data minus (14+60(5yrs data))
    panel = pd.DataFrame()
    for ticker in tickers:

        tickerData = pd.DataFrame(estimates[ticker]).iloc[14:(14+60+t),]
        tickerData['ticker'] = ticker# so it's growing window

        panel = panel.append(tickerData)

    dependent = ['rt']
    exog = ['12mthMomentum',
            'dividendYield',
            'monthlyVolatility',
            'shortRates',
            'slopeTermstructure']

    panel = panel.set_index(['ticker',panel.index])

    mod = PooledOLS(panel[dependent], panel[exog])
    resReg[74+t] = mod.fit().params

resReg1 = pd.DataFrame(resReg).transpose()

resReg1.index = np.arange(74, len(resReg1) + 74)












# forcast return based on the panel regression estimators
df_rt_pred = pd.DataFrame()

for ticker in tickers:
    df_rt_pred[ticker] = estimates[ticker]['12mthMomentum'][74:430] * resReg1['12mthMomentum'].ix[74:430] + \
    estimates[ticker]['dividendYield'][74:430] * resReg1['dividendYield'].ix[74:430] + \
    estimates[ticker]['monthlyVolatility'][74:430] * resReg1['monthlyVolatility'].ix[74:430] + \
    estimates[ticker]['shortRates'][74:430] * resReg1['shortRates'].ix[74:430] + \
    estimates[ticker]['slopeTermstructure'][74:430] * resReg1['slopeTermstructure'].ix[74:430]














# start dealing with weights

def gmv(weigh, varCov, rt):
    up = np.dot(weigh.T,rt)
    down = np.sqrt(np.dot(np.dot(weigh.T,varCov), weigh))
    return up/down


weighs = np.repeat(np.array([1/17]), 17, axis=0)
cons = ({'type': 'eq', 'fun': lambda x: 1-sum(x)})
bnds = ((-0.2,0.2), (-0.2,0.2), (-0.2,0.2), (-0.2,0.2), (-0.2,0.2), (-0.2,0.2), 
        (-0.2,0.2), (-0.2,0.2), (-0.2,0.2), (-0.2,0.2), (-0.2,0.2), (-0.2,0.2), 
        (-0.2,0.2), (-0.2,0.2), (-0.2,0.2), (-0.2,0.2), (-0.2,0.2))

#weighs = np.array([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

weighRes = {}
for i in range(296):
    df_rt_pred1 = pd.DataFrame()
    df_rt_pred1 = df_rt_pred.ix[74:134+i,]
    varCov = []
    for ticker in tickers:
        varCov.append(df_rt_pred1[ticker])
    varCov = pd.DataFrame(np.cov(varCov), columns=tickers, index=tickers)    
    ret = df_rt_pred.ix[134+i,]
    weighRes[i+134] = minimize(gmv, weighs, args=(varCov, ret), bounds=bnds, constraints=cons).x

weighRes = pd.DataFrame(weighRes)
weighRes = weighRes.transpose()


#weighRes.to_csv('gmv_weights.csv')