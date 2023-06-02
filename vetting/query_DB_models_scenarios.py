# -*- coding: utf-8 -*-
"""
Created on Sat May 27 15:00:01 2023

@author: byers
"""

# Query all scenarios in database

import ixmp
import pandas as pd
import pyam
from vetting_functions import *


#%%

wd = 'C:\\Users\\byers\\IIASA\\ECE.prog - Documents\\Projects\\EUAB\\'


instance_s = 'eu_climate_submission'
config_s = f'{wd}euab_submission.properties'

instance_i = 'eu_climate_internal'
config_i = f'{wd}euab_internal.properties'


# Submissions

mp_s = ixmp.Platform(dbprops=config_s)
sl_s = mp_s.scenario_list()

models_s = sl_s.model.unique()

sl_s['model_stripped'] = sl_s.reset_index()['model'].apply(strip_version).values

#%%
# Internal
mp_i = ixmp.Platform(dbprops=config_i)
sl_i = mp_i.scenario_list()

models_i = sl_i.model.unique()

sl_i['model_stripped'] = sl_i.reset_index()['model'].apply(strip_version).values


#%% #mdoels
# Models in submission not in internal
mod_sub = list(set(models_s) - set(models_i))
# ['REMIND 3.1', 'RECC 2.4', 'TIMES-Ireland Model v1.0', 'OSeMBE v1.0.0']
# REMIND 3.1 is duplicate of 3.2, so ignore. # 3 models submitted but not further considered as lacking regional information / country level only.
# TIMES-Ireland - country only
# RECC 2.4 - only 3 variables
# OSeMBE v1.0.0 - no emissions variables
instance = 'eu_climate_submission'
instance = 'eu-climate-advisory-board-internal'

# qp = pyam.read_iiasa(instance,
#                         model='OSeMBE v1.0.0',
#                         meta=False)

# Models in internal not in submission
mod_int = list(set(models_i) - set(models_s))
# 'WITCH 5.1', 'TIAM-ECN 1.2', 'Euro-Calliope 2.0', 'REMIND 3.2'


# Additional scenarios brought in for ECEMF
mylist = list(dict.fromkeys(list(models_i)+list(models_s)))

# Total of 54 models in dbs, but
#  REMIND 3.1 is the first version of the extra REMIND 3.2 scenarios
# 52 models submitted, + REMIND 3.2 solicited =  53
# minus 3 above inelgible, thus 50 in internal = GOOD

#%% scenarios
len(sl_i) #1102 internal (inlcudes 29 REMIND 3.2 scenarios to be removed)
len(sl_s) #1097 submission (includes 59 REMIND 3.1 scenarios)

# msc = sl_i[['model','scenario']]
msc = pd.concat([sl_i[['model','scenario']], sl_s[['model','scenario']]])
msc.drop_duplicates(inplace=True) #len = 1222

msc = msc.loc[~(msc.model=='REMIND 3.1')] # 1161 after removal
# Now drop extra REMIND 3.2 (without ICEPhOP)
msc = msc.loc[~((msc.model=='REMIND 3.2') & (msc.scenario.str.contains('withICEPhOP')==False))] # = 1132 (29 dropped)

# 8 scenarios not transferred = 1126 = 
# 6 * NGFS (renamed
# 2 * DIAG_NZero (REM + PROM) (willbe included so ignore here)
msc = msc.loc[~(msc.scenario=='DIAG-NZero')] # these two not in but will be
msc = msc.loc[~(msc.scenario=='NGFS-Delayed transition')]
msc = msc.loc[~(msc.scenario=='NGFS-Below 2°C')]

# 1126 scenarios considered

# 3 models removed due to lacking info (see above) = 51 scenarios
msc = msc.loc[~(msc.model.isin([ 'RECC 2.4', 'TIMES-Ireland Model v1.0', 'OSeMBE v1.0.0']))] 
len(msc)  # 1075 (should be) in internal


# + extra 3 also not transferred, lacking info
# ALADIN x2
# ENERGYVILLE x2
# ROADMAP x7

mscl = list(zip(msc.model, msc.scenario))

mss = list(zip(sl_s.model, sl_s.scenario))
msi = list(zip(sl_i.model, sl_i.scenario))

not_in_int = set(mss)-set(msi)
not_in_sub = set(msi)-set(mss)

not_in_int_shouldb = set(mscl)-set(msi) #  empty = good
in_int_not_shouldb = set(msi)-set(mscl) # if only REMIND 3.2 this is fine

# =============================================================================
# 1102 in internal, -29 REMIND 3.2 = 1073
# =============================================================================

# Narrative:
# 1094 scenarios submitted + 30 extra REMIND 3.2 = 1124
# 51 scenarios, 3 models lacking info = 1073 from 50 models



# Q: Not transferred? = 11
# ALADIN x2
# ENERGYVILLE x2
# ROADMAP x7

# EnergyVille TIMES BE 1.0.0	Net-Zero_CENTRAL
# EnergyVille TIMES BE 1.0.0	Net-Zero_ELECTRIFICATION
# Roadmap v1.8	CO2 Gap Study Baseline
# Roadmap v1.8	CO2 Gap Study European Climate Law
# Roadmap v1.8	CO2 Gap Study Manufactured aligned zero emission targets
# Roadmap v1.8	CO2 Gap Study Sustainable and Smart Mobility Strategy
# Roadmap v1.8	ZEVTC Study Ambitious
# Roadmap v1.8	ZEVTC Study Baseline
# Roadmap v1.8	ZEVTC Study Progress


# Climate assessed but not transferred, so +2
# PROMETHEUS 1.2	DIAG-NZero
# REMIND 2.1	DIAG-NZero

# Through vetting = 1064 (including the 2 DIAG-NZero ones)

