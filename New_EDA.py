import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sm as sm
from ggplot import *

filename2 = "~\PycharmProjects\Capstone-project\SB-capstone-project\Data\incd.csv"
filename3 = "~\PycharmProjects\Capstone-project\SB-capstone-project\Data\death.csv"
filename4 = '~\PycharmProjects\Capstone-project\SB-capstone-project\Data\MUA_DET.csv'

# Set Paths for github
#filename2 = "~SB-capstone-project\Data\incd.csv"
#filename3 = "~SB-capstone-project\Data\death.csv"
#filename4 = "~SB-capstone-project\Data\MUA_DET.csv"

df2= pd.read_csv(filename2,skiprows=8,nrows=3141,encoding = "ISO-8859-1")

df2 = df2.rename(columns={' FIPS': 'FIPS'})
df2 = df2.rename(columns={'Recent 5-Year Trend () in Incidence Rates': '5YearTrendIncdRates'})
df2 = df2.rename(columns={'Average Annual Count': 'AvgAnnIncdCount'})
df2 = df2.rename(columns={'Age-Adjusted Incidence Rate() - cases per 100,000': 'AgeIncdRateper100K'})

# Remove columns not wanted to use in further analysis
# First create a list of columns in case you decide to go back and change list later
col_drop2 = ['Met Healthy People Objective of ***?',\
            'Lower 95% Confidence Interval','Upper 95% Confidence Interval','Recent Trend',\
            'Lower 95% Confidence Interval.1','Upper 95% Confidence Interval.1']
df2.drop(col_drop2,inplace=True,axis=1)

df2['AvgAnnIncdCount'] = pd.to_numeric(df2['AvgAnnIncdCount'], errors='coerce')
df2['5YearTrendIncdRates'] = pd.to_numeric(df2['5YearTrendIncdRates'], errors='coerce')
df2['AgeIncdRateper100K'] = pd.to_numeric(df2['AgeIncdRateper100K'], errors='coerce')

#df2.plot(x='County',y='Avg Ann Incd Count')
# US is the first row which has a very large number (i.e outlier) plotting w/o first row
# County names in X can't be read
df2 = df2[1:]

df3= pd.read_csv(filename3,skiprows=8,nrows=3141,encoding = "ISO-8859-1")

# We see that the FIPS column has a empty space so we rename it. This column is very important for our analysis as
# FIPS can be used to correlate to other Datasets and their variables
df3 = df3.rename(columns={' FIPS': 'FIPS'})
df3 = df3.rename(columns={'Recent 5-Year Trend () in Death Rates': '5YearTrendDeathRates'})
df3 = df3.rename(columns={'Average Annual Count': 'AvgAnnualDeathCount'})
df3 = df3.rename(columns={'Age-Adjusted Death Rate() - deaths per 100,000': 'AgeDeathRateper100K'})

# Remove columns not wanted to use in further analysis
# First create a list of columns in case you decide to go back and change list later
col_drop3 = ['Met Healthy People Objective of 161.4?',\
            'Lower 95% Confidence Interval','Upper 95% Confidence Interval','Recent Trend',\
            'Lower 95% Confidence Interval.1','Upper 95% Confidence Interval.1','County']
df3.drop(col_drop3,inplace=True,axis=1)

df3['AvgAnnualDeathCount'] = pd.to_numeric(df3['AvgAnnualDeathCount'], errors='coerce')
df3['5YearTrendDeathRates'] = pd.to_numeric(df3['5YearTrendDeathRates'], errors='coerce')
df3['AgeDeathRateper100K'] = pd.to_numeric(df3['AgeDeathRateper100K'], errors='coerce')

# US is the first row which has a very large number (i.e outlier) plotting w/o first row
df3 = df3[1:]

df4 = pd.read_csv(filename4)

# rename column to match Incd FIPS column
df4 = df4.rename(columns={'Common State County FIPS Code': 'FIPS'})
df4 = df4.rename(columns={'Percent of Population with Incomes at or Below 100 Percent of the U.S. Federal Poverty Level':\
                              'PercofPopwIncomesatorBelowFedPov'})
df4 = df4.rename(columns={'Providers per 1000 Population':\
                              'Providersper1000Pop'})
print(df4['FIPS'].value_counts(dropna=False))

# decide which columns you want to keep then drop rest..so we can merge later w death count and incd rates
col_drop4 = ['MUA/P ID','MUA/P Area Code',\
            'Minor Civil Division FIPS Code','Minor Civil Division Census Code','Minor Civil Division Name',\
            'Census Tract','Designation Date','Designation Date.1','IMU Score','MUA/P Service Area Name','MUA/P Update Date',\
           'MUA/P Update Date.1','U.S. - Mexico Border 100 Kilometer Indicator','U.S. - Mexico Border County Indicator',\
           'County or County Equivalent Federal Information Processing Standard Code','County Equivalent Name',\
             'County Description','HHS Region Code','HHS Region Name','State FIPS Code','Infant Mortality Rate',\
             'Infant Mortality Rate IMU Score','Ratio of Providers per 1000 Population IMU Score','Data Warehouse Record Create Date',\
             'Common County Name with State Abbreviation','Break in Designation',\
       'Medically Underserved Area/Population (MUA/P) Component Designation Date',\
       'Medically Underserved Area/Population (MUA/P) Component Designation Date.1',\
       'Medically Underserved Area/Population (MUA/P) Component Geographic Name',\
       'Medically Underserved Area/Population (MUA/P) Component Geographic Type Code',\
       'Medically Underserved Area/Population (MUA/P) Component Geographic Type Description',\
       'Medically Underserved Area Geography Type Surrogate Key',\
       'Medically Underserved Area/Population (MUA/P) Component Last Update Date']

df4.drop(col_drop4,inplace=True,axis=1)

# Merge df2 Incd Rate with df4 into fulldf
fulldf = df4.merge(df2[['FIPS', 'County','AvgAnnIncdCount','5YearTrendIncdRates','AgeIncdRateper100K']], on='FIPS', how='inner')
# Merge df3 Death Rate with df4 into fulldf
completedf = fulldf.merge(df3[['FIPS','AvgAnnualDeathCount','5YearTrendDeathRates','AgeDeathRateper100K']], on='FIPS', how='inner')

# Need to verify the same amount of FIPS codes are in each dataset 3140 per number of counties
print(completedf['FIPS'].value_counts(dropna=False))

# Create summaries of OLS (Ordinary Least Square) linear regression modeling using DV(Death count,Incd count and
# Providers vs IV(Low income population)

result_IC_LI = sm.ols("AvgAnnIncdCount ~ PercofPopwIncomesatorBelowFedPov",data=completedf).fit()
result_IC_LI.summary()

result_DC_LI = sm.ols("AvgAnnualDeathCount ~ PercofPopwIncomesatorBelowFedPov",data=completedf).fit()
result_DC_LI.summary()

result_P1k_LI = sm.ols("Providersper1000Pop ~ PercofPopwIncomesatorBelowFedPov",data=completedf).fit()
result_P1k_LI.summary()


# Use Seaborn to create regression of mortality, incidence, Age against Poverty and providers with merged Dataframes

sns.set(color_codes=True)
sns.regplot(x="AvgAnnualDeathCount", y="PercofPopwIncomesatorBelowFedPov", data=completedf, lowess=False)
sns.regplot(x="AvgAnnIncdCount", y="PercofPopwIncomesatorBelowFedPov", data=completedf, lowess=False)

sns.regplot(x="AgeDeathRateper100K", y="PercofPopwIncomesatorBelowFedPov", data=completedf, lowess=False)
sns.regplot(x="AgeIncdRateper100K", y="PercofPopwIncomesatorBelowFedPov", data=completedf, lowess=False)

sns.regplot(x="Providersper1000Pop", y="PercofPopwIncomesatorBelowFedPov", data=completedf, lowess=False)
sns.regplot(x="Providersper1000Pop", y="AgeDeathRateper100K", data=completedf, lowess=False)


# Continue EDA using ggplot on merged Datasets - tell your story!
#cdfp1 = ggplot(completedf, aes(x='5 Year Trend Death Rates',y='Avg Ann Death Count', group='County_y')) + geom_bar(position="dodge", stat="identity")
#cdfp2 = ggplot(completedf, aes(x='5 Year Trend Incd Rates',y='Avg Ann Incd Rates', group='County_y, col='County_y')) + facet.grid('FIPS'')
#cdfp3 = ggplot(completedf, aes(x=))