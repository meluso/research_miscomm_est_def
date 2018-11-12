# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 13:28:36 2018

@author: Juango the Blue
"""

# Import packages
import csv

# Import simulation results summary data
with open('C:/Users/Juango the Blue/Documents/2016-Present (Michigan)/' +
          'Research/12 Estimation Definitions/04 Analysis/Results' +
          '/2018-11-10_08-13-06_MCResultsSummary.csv','rb') as f:
    reader = csv.reader(f)
    results = map(tuple,reader)

# Slice the results by different groups
