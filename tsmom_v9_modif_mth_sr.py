# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 08:13:59 2019

@author: freakylemon

Please be note that I installed the 'arch' package additionally
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from arch import arch_model

#import data
forex = pd.read_csv('fx.csv')
bdfutures = pd.read_csv('bdfutures.csv')
comdty = pd.read_csv('comdty.csv')
indexfutures = pd.read_csv('indexfutures.csv')
rf = pd.read_csv('rf.csv')

#keep one 'Dates', drop others
bdfutures = bdfutures.drop(['Dates'], axis=1)
comdty = comdty.drop(['Dates'], axis=1)
indexfutures = indexfutures.drop(['Dates'], axis=1)
rf = rf.drop(['Dates'], axis=1)

#concatenate
whole_dset = [forex, bdfutures, comdty, indexfutures, rf]
dset = pd.concat(whole_dset, axis=1)

dset.drop(['HO1 COMDTY.1'], axis=1, inplace=True)
dset.drop(['TP1 INDEX.1'], axis=1, inplace=True)


# dset.to_csv('whole_data_set_200219.csv')

dset['Dates'] = pd.to_datetime(dset.Dates)

dset = dset.set_index('Dates')

# insert week of the day at first column
dset.insert(loc=0, column='week_of_day', value=dset.index.weekday)

c = ['AUDNZD CURNCY', 'AUDUSD CURNCY', 'EURJPY CURNCY', 'EURNOK CURNCY',
       'EURSEK CURNCY', 'EURGBP CURNCY', 'AUDJPY CURNCY', 'GBPUSD CURNCY',
       'EURUSD CURNCY', 'USDCAD CURNCY', 'USDJPY CURNCY', 'YM1 COMDTY',
       'XM1 COMDTY', 'DU1 COMDTY', 'OE1 COMDTY', 'RX1 COMDTY', 'JB1 COMDTY',
       'G 1 COMDTY', 'TU1 COMDTY', 'FV1 COMDTY', 'TY1 COMDTY', 'US1 COMDTY',
       'CO1 COMDTY', 'LC1 COMDTY', 'CC1 COMDTY', 'KC1 COMDTY', 'HG1 COMDTY',
       'C 1 COMDTY', 'CT1 COMDTY', 'CL1 COMDTY', 'QS1 COMDTY', 'GC1 COMDTY',
       'HO1 COMDTY', 'LH1 COMDTY', 'NG1 COMDTY', 'LN1 COMDTY', 'PL1 COMDTY',
       'SI1 COMDTY', 'S 1 COMDTY', 'SM1 COMDTY', 'BO1 COMDTY', 'SB1 COMDTY',
       'W 1 COMDTY', 'LX1 COMDTY', 'GX1 INDEX', 'IB1 INDEX', 'CF1 INDEX',
       'TP1 INDEX', 'Z 1 INDEX', 'SP1 INDEX', 'HI1 INDEX', 'KM1 INDEX']


'''below to scale data for  returns'''

#drop rows to get full weekly data
df_periodic_return = dset.iloc[1:5506]

#df_periodic_return.to_csv('whole_data_set_200319.csv')

#df = dset.pct_change()
df_periodic_return['week_of_day'] = df_periodic_return.index.weekday

#df = df.iloc[1:]

#return of 4 week, 12 week, and 50 week.

##drop last several rows to have full-weekly-data
#df = df.iloc[:5500]
df = df_periodic_return

#new dataframe with only price info in friday and thursday of every week.
df_fri = df[(df['week_of_day'] == 4)]
df_thu = df[(df['week_of_day'] == 3)]

df_fri = df_fri.drop(['week_of_day'], axis=1)
df_thu = df_thu.drop(['week_of_day'], axis=1)

df_fri = df_fri.reset_index(drop=True)
df_thu = df_thu.reset_index(drop=True)

df_fri.index.astype('int64', copy=True)
df_thu.index.astype('int64', copy=True)

###############################
####### monthly sign ##########
###############################

#rescale index
'''
to rebalance weekly based on monthly data,
drop the last 3 monday data,
drop the first 3 thursday data and done.
'''
#change index type
df_mth_fri = df_fri[:1098]
df_mth_thu = df_thu.iloc[3:] 

#reset index:
df_mth_fri = df_mth_fri.reset_index(drop=True)
df_mth_thu = df_mth_thu.reset_index(drop=True)

# monthly return.
# so sure is the (month end (4th thursday) - month beginning(1st monday)) / xxx
df_mthly = (df_mth_thu-df_mth_fri)/df_mth_fri

# monthly excess return.
df_mthly_ex = df_mthly.copy()

for i in c:
    df_mthly_ex[i] = df_mthly_ex[i] - df_mthly_ex['USGG10YR INDEX']
df_mthly_ex = df_mthly_ex.drop(['FEDL01 INDEX', 'USGG10YR INDEX'], axis=1)

##################################
#### transfer numbers to sign ####
##################################

df_mthly_sign = df_mthly_ex.copy()
print(len(df_mthly_sign['AUDNZD CURNCY']))

print(df_mthly_sign['AUDNZD CURNCY'][244])

for i in c:
    for t in range(1098):
        if df_mthly_ex[i][t] < 0.0:
            df_mthly_sign[i][t] = -1
        else:
            df_mthly_sign[i][t] = 1


# visualize it with chart,


###############################################
########## the monthly-window return ##########
###############################################
            
df_mthly_r = df_fri.pct_change(periods=1)

# we have sign from first month, based on this, we started to trade,
# which means return starts from the 2nd month

df_mthly_r = df_mthly_r[5:]
df_mthly_r = df_mthly_r.reset_index(drop=True)

df_mth_rf = df_mthly_r['USGG10YR INDEX']

df_mthly_r = df_mthly_r.drop(['FEDL01 INDEX', 'USGG10YR INDEX'], axis=1)
df_mthly_sign = df_mthly_sign[:1096]
df_mthly_r = df_mthly_r * df_mthly_sign

# for sharpe ratio, I calculated the excess return.
df_mthly_ex = df_mthly_r.copy()
for i in c:
    df_mthly_ex[i] = df_mthly_r[i] - df_mth_rf


# last sign does not allow us to make the position anymore(run out of date)
# we may have to drop the last some.

df_av_mthly = df_mthly_r.mean(axis=0)
plt.figure(figsize=(18, 11))
df_av_mthly.plot(kind='bar')
plt.legend()

''' the sharpe ratio ''' 
df_sr_mthly = df_mthly_ex.mean(axis=0)/df_mthly_r.std(axis=0)
plt.figure(figsize=(18, 11))
df_sr_mthly.plot(kind='bar')
plt.legend()

##############################################
##### GARCH - log return of monthly data #####
##### obtain ex-ante volatility
##############################################

df_log_rt = df_fri.copy()

for i in c:
    df_log_rt[i] = np.log(df_fri[i]) - np.log(df_fri[i].shift(1))

df_log_rt = df_log_rt[4:]
#df_log_rt = df_log_rt * 100
df_log_rt = df_log_rt.reset_index(drop=True)

df_log_rt= df_log_rt.drop(['FEDL01 INDEX', 'USGG10YR INDEX'],axis=1)

###########################################
########## monthly GARCH package ##########
###########################################

para_mth_garch = {}
for i in c:
    para = arch_model(df_log_rt[i]).fit()
    para_mth_garch[i] = para.params.values
para_mth_garch = pd.DataFrame(para_mth_garch, index=['mu', 'omega', 'alpha', 'beta'])

df_vol_mth = df_log_rt.copy()
for i in c:
    omega = para_mth_garch[i]['omega']
    alpha = para_mth_garch[i]['alpha']
    beta = para_mth_garch[i]['beta']
    df_vol_mth[i][0] = np.sqrt(omega/(1-alpha-beta))
    for t in range(1,len(df_vol_mth[i])):
        df_vol_mth[i][t] = np.sqrt(omega + alpha *df_log_rt[i][t-1]**2 +beta*df_vol_mth[i][t-1]**2)

# 2.2, for volatility scaled return

# I have already adjusted sign and rt ensuring that return_{t+1} = sign_t * return{t + 1}
# here similar reason, I have to drop the last line of the volatility dataset.

df_vol_mth = df_vol_mth[:1096]

# realized return
df_mthly_r_rescaled = df_mthly_r *0.4/(df_vol_mth*np.sqrt(50))

# check the annualized return.
print(df_mthly_r_rescaled.std(axis=0)*np.sqrt(50))

# it's exactly arount 40%, the annualized volatility!!!

# here we may proceed to the mean and sr calculation on scaled investment!!!

plt.figure(figsize=(18, 11))
df_mthly_r_rescaled.mean(axis=0).plot(kind='bar')
plt.legend()

# for sharpe ratio, I calculated the excess return.
df_mthly_ex_rescaled = df_mthly_r_rescaled.copy()
for i in c:
    df_mthly_ex_rescaled[i] = df_mthly_r_rescaled[i] - df_mth_rf
 
df_sr_mthly_rescaled = df_mthly_ex_rescaled.mean(axis=0)/df_mthly_r_rescaled.std(axis=0)
plt.figure(figsize=(18, 11))
df_sr_mthly_rescaled.plot(kind='bar')
plt.legend()



#######################
#### 12 weeks sign ####
#######################

df_qua_fri = df_fri.iloc[:1090]
df_qua_thu = df_thu.iloc[11:] 

#reset index:
df_qua_fri = df_qua_fri.reset_index(drop=True)
df_qua_thu = df_qua_thu.reset_index(drop=True)

# quaterly momemtum sign.
# so sure is the (month end (12th thursday) - month beginning(1st friday)) / xxx
df_quatly = (df_qua_thu -df_qua_fri)/df_qua_fri

df_quatly_ex = df_quatly.copy()

for i in c:
    df_quatly_ex[i] = df_quatly_ex[i] - df_quatly_ex['USGG10YR INDEX']
df_quatly_ex = df_quatly_ex.drop(['FEDL01 INDEX', 'USGG10YR INDEX'], axis=1)

df_qua_sign = df_quatly_ex.copy()
for i in c:
    for t in range(1090):
        if df_quatly_ex[i][t] < 0:
            df_qua_sign[i][t] = -1
        else:
            df_qua_sign[i][t] = 1

#########################
#### 12 weeks return ####
#########################
df_qua_r = df_fri.pct_change(periods=1)

df_qua_rf = df_qua_r['USGG10YR INDEX']
df_qua_r = df_qua_r.drop(['FEDL01 INDEX', 'USGG10YR INDEX'], axis=1)

# same as monthly data, 
# we have to drop the first return since there's no previous sign

df_qua_r = df_qua_r[13:]
df_qua_r = df_qua_r.reset_index(drop=True)

# to have same amount of signs as returns
df_qua_sign = df_qua_sign[:1088]
df_qua_r = df_qua_r * df_qua_sign

#df_quatly.to_csv('quaterly excess return_whole_set.csv')
df_qua_rf = df_qua_rf[13:]
df_qua_rf = df_qua_rf.reset_index(drop=True)

df_qua_ex = df_qua_r.copy()
for i in c:
    df_qua_ex[i] = df_qua_ex[i] - df_qua_rf

'''return'''
df_av_qua = df_qua_r.mean(axis=0)
plt.figure(figsize=(18, 11))
#df_av_qua.plot(kind='bar')
df_av_qua.plot(kind='bar')
plt.legend()


''' the sharpe ratio ''' 
df_sr_qua = df_qua_ex.mean(axis=0)/df_qua_ex.std(axis=0)
plt.figure(figsize=(18, 11))
#df_av_qua.plot(kind='bar')
df_sr_qua.plot(kind='bar')
plt.legend()

##############################################
##### GARCH - log return of quaterly data #####
##############################################

df_qua_log_rt = df_fri.copy()

for i in c:
    df_qua_log_rt[i] = np.log(df_fri[i]) - np.log(df_fri[i].shift(1))

df_qua_log_rt = df_qua_log_rt[12:]

df_qua_log_rt = df_qua_log_rt.reset_index(drop=True)

df_qua_log_rt= df_qua_log_rt.drop(['FEDL01 INDEX', 'USGG10YR INDEX'],axis=1)

###########################################
########## quaterly GARCH package ##########
###########################################

para_qua_garch = {}
for i in c:
    para = arch_model(df_qua_log_rt[i]).fit()
    para_qua_garch[i] = para.params.values
para_qua_garch = pd.DataFrame(para_qua_garch, index=['mu', 'omega', 'alpha', 'beta'])

df_vol_qua = df_qua_log_rt.copy()
for i in c:
    omega = para_qua_garch[i]['omega']
    alpha = para_qua_garch[i]['alpha']
    beta = para_qua_garch[i]['beta']
    df_vol_qua[i][0] = np.sqrt(omega/(1-alpha-beta))
    for t in range(1,len(df_vol_qua[i])):
        df_vol_qua[i][t] = np.sqrt(omega + alpha *df_qua_log_rt[i][t-1]**2 +beta*df_vol_qua[i][t-1]**2)

# 2.2

df_vol_qua = df_vol_qua[:1088]

# realized return
df_qua_r_rescaled = df_qua_r *0.4/(df_vol_qua*np.sqrt(50))

# check the annualized return.
print(df_qua_r_rescaled.std(axis=0)*np.sqrt(50))

# it's exactly arount 40%, the annualized volatility!!!

# here we may proceed to the mean and sr calculation on scaled investment!!!

plt.figure(figsize=(18, 11))
df_qua_r_rescaled.mean(axis=0).plot(kind='bar')
plt.legend()

# for sharpe ratio, I calculated the excess return.
df_qua_ex_rescaled = df_qua_r_rescaled.copy()
for i in c:
    df_qua_ex_rescaled[i] = df_qua_r_rescaled[i] - df_qua_rf
 
df_sr_qua_rescaled = df_qua_ex_rescaled.mean(axis=0)/df_qua_ex_rescaled.std(axis=0)
plt.figure(figsize=(18, 11))
df_sr_qua_rescaled.plot(kind='bar')
plt.legend()



#####################
### 50 weeks sign ###
#####################

df_ann_fri = df_fri[:1052]
df_ann_thu = df_thu[49:] 

#reset index:
df_ann_fri = df_ann_fri.reset_index(drop=True)
df_ann_thu = df_ann_thu.reset_index(drop=True)

# monthly return.
# so sure is the (month end (4th thursday) - month beginning(1st monday)) / xxx
df_annually = (df_ann_thu - df_ann_fri)/ df_ann_fri

# monthly excess return.
df_ann_ex = df_annually.copy()

for i in c:
    df_ann_ex[i] = df_ann_ex[i] - df_ann_ex['USGG10YR INDEX']
df_ann_ex = df_ann_ex.drop(['FEDL01 INDEX', 'USGG10YR INDEX'], axis=1)


df_ann_sign = df_ann_ex.copy()
for i in c:
    for t in range(1052):
        if df_ann_ex[i][t] < 0:
            df_ann_sign[i][t] = -1
        else:
            df_ann_sign[i][t] = 1

#######################
### 50 weeks return ###
#######################

df_ann_r = df_fri.pct_change(periods=1)

df_ann_rf = df_ann_r['USGG10YR INDEX']

df_ann_rf = df_ann_rf[51:]
df_ann_rf = df_ann_rf.reset_index(drop=True)

df_ann_r = df_ann_r[51:]
df_ann_r = df_ann_r.reset_index(drop=True)

df_ann_r = df_ann_r.drop(['FEDL01 INDEX', 'USGG10YR INDEX'], axis=1)

df_ann_sign = df_ann_sign[:1050]


df_ann_r = df_ann_r * df_ann_sign
df_ann_ex = df_ann_r.copy()

for i in c:
    df_ann_ex[i] = df_ann_ex[i] - df_ann_rf

'''return'''
df_av_ann = df_ann_r.mean(axis=0)
plt.figure(figsize=(18, 11))
df_av_ann.plot(kind='bar')
#df_sd_qua.plot(kind='bar')
plt.legend()

''' the sharpe ratio ''' 
df_sr_ann = df_ann_ex.mean(axis=0)/df_ann_ex.std(axis=0)
plt.figure(figsize=(18, 11))
df_sr_ann.plot(kind='bar')
#df_sd_qua.plot(kind='bar')
plt.legend()


##############################################
##### GARCH - log return of annually data #####
##############################################

df_ann_log_rt = df_fri.copy()

for i in c:
    df_ann_log_rt[i] = np.log(df_fri[i]) - np.log(df_fri[i].shift(1))

df_ann_log_rt = df_ann_log_rt[50:]
#df_ann_log_rt = df_ann_log_rt * 100
df_ann_log_rt = df_ann_log_rt.reset_index(drop=True)

df_ann_log_rt= df_ann_log_rt.drop(['FEDL01 INDEX', 'USGG10YR INDEX'],axis=1)


############################################
########## annually GARCH package ##########
############################################


para_ann_garch = {}
for i in c:
    para = arch_model(df_ann_log_rt[i]).fit()
    para_ann_garch[i] = para.params.values
para_ann_garch = pd.DataFrame(para_ann_garch, index=['mu', 'omega', 'alpha', 'beta'])

df_ann_vol = df_ann_log_rt.copy()
#df_ann_log_rt = df_ann_log_rt/100
for i in c:
    omega = para_ann_garch[i]['omega']
    alpha = para_ann_garch[i]['alpha']
    beta = para_ann_garch[i]['beta']
    df_ann_vol[i][0] = np.sqrt(omega/(1-alpha-beta))
    for t in range(1,len(df_ann_vol[i])):
        df_ann_vol[i][t] = np.sqrt(omega + alpha *df_ann_log_rt[i][t-1]**2 +beta*df_ann_vol[i][t-1]**2)


df_ann_vol = df_ann_vol[:1050]

# realized return
df_ann_r_rescaled = df_ann_r *0.4/(df_ann_vol*np.sqrt(50))

# check the annualized return.
print(df_ann_r_rescaled.std(axis=0)*np.sqrt(50))

plt.figure(figsize=(18, 11))
df_ann_r_rescaled.mean(axis=0).plot(kind='bar')
plt.legend()

# for sharpe ratio, I calculated the excess return.
df_ann_ex_rescaled = df_ann_r_rescaled.copy()
for i in c:
    df_ann_ex_rescaled[i] = df_ann_r_rescaled[i] - df_ann_rf
 
df_sr_ann_rescaled = df_ann_ex_rescaled.mean(axis=0)/df_ann_ex_rescaled.std(axis=0)
plt.figure(figsize=(18, 11))
df_sr_ann_rescaled.plot(kind='bar')
plt.legend()


###############################################################################


















