#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 12:20:09 2017

@author: hiram
"""
import pandas as pd
from scipy import stats

class ANOVA(object):
    """
    Arguments:
    - dataframe: a pandas dataframe containing at least two columns, a
        dependent variable and an independent variable.
    - dependent_variable: the name of the column in dataframe for 
        values for all samples from all groups
    - independent_variable: the name of the column in dataframe that 
        indicates the group corresponding to each sample
    - weighted: Specify if ANOVA will be calculated according to weighted or
        unweighted group means.     
        
    """
    def __init__(self, dataframe, dependent_variable, independent_variable, weighted=True):
        self.df = dataframe
        self.dv = dependent_variable
        self.iv = independent_variable
        self.weighted = weighted
        self.N = self.df[dependent_variable].count() #total number of samples
        self.groups = pd.unique(self.df[independent_variable].values) #array of group names
        self.k = len(pd.unique(self.df[independent_variable].values)) #total number of groups
        self.samples = self.df.groupby(independent_variable).count()[dependent_variable].to_dict() #dict of count of samples in each group
        self.means = self.df.groupby(independent_variable).mean()[dependent_variable].to_dict() # dict of mean for each group
        self.deg_freedom_between = self.k-1
        self.deg_freedom_within = self.N - self.k
        self.F_stat = self.F()
        self.P_value = self.P()

    
    def grandmean(self, weighted=None, verbose=False):
        x = y = 0
        if weighted is None:
            weighted = self.weighted
        if weighted:
            for group in self.groups:
                x += self.samples[group] * self.means[group]
                y += self.samples[group]
            if verbose:
                print ('Calculating Weighted Mean...')
                print ('Number of samples in each group:\n{}'.format(self.samples))
                print ('Mean of Each Group:\n{}'.format(self.means))
                print ('Weighted Mean: {}'.format(x/y))
            return x/y
        if not weighted:
            x = sum(self.means.values())
            y = len(self.samples)
            if verbose:
                print ('Calcuating Unweighted Mean...')
                print ('Overall Sum: {}'.format(x))
                print ('Total Samples: {}'.format(self.N))
                print ('Unweighted Mean: {}'.format(x/y))
            return x/y
    def F(self, weighted=None):
        if weighted is None:
            weighted = self.weighted        
        def groupss(group):
            temp = self.df.loc[self.df[self.iv]==group][self.dv].values
            mean = temp.mean()
            ss = 0
            for sample in temp:
                ss += (sample - mean)**2
            return ss
        sumsquares_within = sum([groupss(group) for group in self.groups]) 
        sumsquares_between = sum([self.samples[group]*((self.means[group] - self.grandmean(weighted=weighted))**2) for group in self.groups])
        meansquares_between = sumsquares_between/self.deg_freedom_between
        meansquares_within = sumsquares_within/self.deg_freedom_within
        return meansquares_between/meansquares_within
    def P(self, weighted=None):
        if weighted is None:
            weighted = self.weighted        
        return stats.f.sf(self.F(weighted=weighted), self.deg_freedom_between, self.deg_freedom_within)

    

#example
df = pd.DataFrame({'foo':[1,2,3,4,5], 'bar':['a', 'a', 'b', 'b', 'b']})
x = ANOVA(df, 'foo', 'bar')
x.grandmean(weighted=True) # = 3.0
x.grandmean(weighted=False) # = 2.75
x.F() # 9.0
x.P() # = 0.058
