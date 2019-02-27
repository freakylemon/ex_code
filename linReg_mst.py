# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 16:03:49 2019

@author: freakylemon
"""

from sklearn.model_selection import train_test_split
from sklearn import linear_model

'''
under Linear Regression, by excluding one feature at a time, 
see the accuracy change
'''
def theMstI(dataSet, lbl):
    allFea = dataSet.columns
    feaLst = []
    for i in allFea:
        feaLst.append(i)
    feaLst.remove(lbl)
    
    for i in feaLst:
        X = dataSet.drop([i],axis=1)
        y = dataSet[lbl]
        X.drop([lbl],axis = 1,inplace = True)
        X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.30,random_state=9999)
        regr = linear_model.LinearRegression()
        regr.fit(X_train, y_train)
#         y_pred = logRe.predict(X_train)

#         y_pred_test = logRe.predict(X_test)
        accu = regr.score(X_train,y_train)
        print("by excluding feature",
              i,
    #           X.columns,
              "the accuracy of test set is: {:3f}".format(accu)
              )