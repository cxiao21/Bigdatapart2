"""
Author: Lira Mota, lmota20@gsb.columbia.edu
Course: Big Data in Finance (Spring 2020)
Date: 2020-02
Code:
    Homework II skeleton. Portfolio sorts.

------

Dependence:
fire_pytools

"""

# %% Packages
import pandas as pd
import numpy as np

import stock_annual as stock_annual
import stock_monthly as stock_monthly

# Packages from fire_pytools
from utils.monthly_date import *

from portools.find_breakpoints import find_breakpoints
from portools.sort_portfolios import sort_portfolios

desired_width = 10
pd.set_option('display.width', desired_width)
idx = pd.IndexSlice

# %% Set Up

# %% Download Data
# Monthly Data
mdata = stock_monthly.main()

# Annual Data
adata = stock_annual.main()
adata.drop(columns='inv',inplace=True)
# we need to drop inv here otherwise we will have two "inv" in the following dataframes

# Set names
adata.rename(columns={'mesum_june': 'me', 'inv_gvkey': 'inv'}, inplace=True) #inv_permco

# %% Create Filters
# shrcd must be (10,11)
# ---------------------
print('Data deleted due to shrcd: %f' % np.round((1-adata.shrcd.isin([10, 11]).mean())*100, 2))
sort_data = adata[adata.shrcd.isin([10, 11])].copy()

# exchcd must be (1, 2, 3)
# ------------------------
print('Data deleted due to exchcd: %f' % np.round((1-sort_data.exchcd.isin([1, 2, 3]).mean())*100, 2))
sort_data = sort_data[sort_data.exchcd.isin([1, 2, 3])]


sort_mdata=mdata[mdata.shrcd.isin([10, 11])].copy()
sort_mdata=sort_mdata[sort_mdata.exchcd.isin([1, 2, 3])]
#del adata, mdata

# %% Portfolio Sorts
## ME X BEME
# notice that the way we defined beme or beme is null if be<=0
sample_filters = ((sort_data.me > 0) &
                  (sort_data.mesum_dec > 0) &
                  (sort_data.beme.notnull()))

beme_sorts = sort_portfolios(data=sort_data[sample_filters],
                             quantiles={'me': [0.5], 'beme': [0.3, 0.7]},
                             id_variables=['rankyear', 'permno', 'exchcd'],
                             exch_cd=[1]
                             )

# TODO: ME X OP
# I do the following 3 parts according to the code in the ME X BEME part
sample_filters2 = ((sort_data.me > 0) &
                  (sort_data.mesum_dec > 0) &
                  (sort_data.op.notnull()))

opbe_sorts = sort_portfolios(data=sort_data[sample_filters2],
                             quantiles={'me': [0.5], 'opbe': [0.3, 0.7]},
                             id_variables=['rankyear', 'permno', 'exchcd'],
                             exch_cd=[1]
                             )
# TODO: ME X INV
sample_filters3 = ((sort_data.me > 0) &
                  (sort_data.mesum_dec > 0) &
                  (sort_data.inv.notnull()))
inv_sorts = sort_portfolios(data=sort_data[sample_filters3],
                             quantiles={'me': [0.5], 'inv': [0.3, 0.7]},
                             id_variables=['rankyear', 'permno', 'exchcd'],
                             exch_cd=[1]
                             )

# TODO: ME X ret_11_1 (sorts at each month - id_variables=['date', 'permno', 'exchcd'])
sample_filters4 = ((sort_data.me > 0) &
                  (sort_data.mesum_dec > 0) &
                  (sort_data.ret_11_1.notnull()))

meret_sorts = sort_portfolios(data=sort_data[sample_filters],
                             quantiles={'me': [0.5], 'ret_11_1': [0.3, 0.7]},
                             id_variables=['date', 'permno', 'exchcd'],
                             exch_cd=[1]
                             )

##I use os to store the outputed data as following
import os
os.chdir("C:\1notes\Spring 2020\Big data\Part2HW")
meret_sorts.to_csv("meret_sorts.to_csv",index=False)
beme_sorts.to_csv("beme_sorts",index=False)
opbe_sorts.to_csv("opbe_sorts",index=False)
inv_sorts.to_csv("inv_sorts",index=False)





