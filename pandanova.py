#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 12:20:09 2017

@author: hiram
"""
import pandas as pd
from scipy import stats

class ANOVA(object):
    """
    Attributes:
    dependent_variable: a series or column in a dataframe that includes
        all samples from all groups
    independent_variable: a series or column from a dataframe that indicate
        the group corresponding to each sample
    """
    Fstat = 0
    def __init__(self, dataframe, dependent_variable, independent_variable):
        self.df = dataframe
        self.dv = dependent_variable
        self.iv = independent_variable
        self.N = df[dependent_variable].count() #total number of samples
        self.groups = pd.unique(df[independent_variable].values) #array of group names
        self.k = len(pd.unique(df[independent_variable].values)) #total number of groups
        self.samples = df.groupby(independent_variable).count()[dependent_variable].to_dict() #dict of count of samples in each group
        self.means = df.groupby(independent_variable).mean()[dependent_variable].to_dict() # dict of mean for each group
    
    def grandmean(self, weighted=True, verbose=False):
        x = y = 0
        if weighted:
            for group in self.groups:
                x += self.samples[group] * self.means[group]
                y += self.samples[group]
            if verbose:
                print 'Weighted Mean:'
                print 'number of samples in each group: '
                print self.samples
                print 'mean of each group: '
                print self.means
                print 'weighted mean: '
                print x/y
            return x/y
        if not weighted:
            x = sum(self.means.values())
            y = len(self.samples)
            if verbose:
                print 'Unweighted Mean:'
                print 'overall sum: '
                print x
                print 'total samples: '
                print self.N
                print 'unweighted mean: '
                print x/y
            return x/y       
    def F(self):
        def groupss(group):
            temp = df.loc[df[self.iv]==group][self.dv].values
            mean = temp.mean()
            ss = 0
            for sample in temp:
                ss += (sample - mean)**2
            return ss
        global dfb
        dfb = self.k-1  #degress of freedom between groups
        global dfw
        dfw = self.N - self.k #degress of freedom within groups
        GM = self.grandmean()
        sumsquareswithin = sum([groupss(group) for group in self.groups]) 
        sumsquaresbetween = sum([self.samples[group]*((self.means[group] - GM)**2) for group in self.groups])
        meansquaresbetween = sumsquaresbetween/dfb
        meansquareswithin = sumsquareswithin/dfw
        global Fstat
        Fstat = meansquaresbetween/meansquareswithin
        return Fstat
    def P(self):
        global P
        P = stats.f.sf(self.F(), dfb, dfw)
        return P

    
    
#example
# df = pd.DataFrame({'foo':[1,2,3,4,5], 'bar':['a', 'a', 'b', 'b', 'b']})
# x = ANOVA(df, 'foo', 'bar')
# x.grandmean(weighted=True) # = 3.0
# x.grandmean(weighted = False) # = 2.75
# x.Fstat() # 9.0
# x.P() # = 0.058
