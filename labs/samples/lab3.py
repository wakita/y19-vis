#!/usr/bin/env python

'''
spi2019.xlsx: Social Progress Index
    Obtained on 2019-12-18 from: 

m49.csv: Standard country or area codes for statistical use (M49)
    Obtained on 2019-12-18 from: https://unstats.un.org/unsd/methodology/m49/overview/
'''

import pandas as pd

spi_xl = pd.read_excel('../spi2019.xlsx', sheet_name=None)

spi19 = spi_xl['2019']

keys = ['Country', 'Code', 'Basic Human Needs', 'Foundations of Wellbeing', 'Opportunity']

spi19_NWO = spi19[keys]
print(spi19_NWO)
