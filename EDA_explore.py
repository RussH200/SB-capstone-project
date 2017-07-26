import pandas as pd
import matplotlib.pyplot as plt
from ggplot import *

filename = "~\PycharmProjects\Capstone-project\SB-capstone-project\Data\BYAREA.TXT"
df = pd.read_table(filename,sep='|')

filename2 = "~\PycharmProjects\Capstone-project\SB-capstone-project\Data\incd.csv"
filename3 = "~\PycharmProjects\Capstone-project\SB-capstone-project\Data\death.csv"

df.YEAR = pd.to_numeric(df.YEAR, downcast='integer',errors='coerce')
df.COUNT = pd.to_numeric(df['COUNT'], errors='coerce')
df.POPULATION = pd.to_numeric(df['POPULATION'], errors='coerce')

df_pivot_1 = df.pivot_table(index=['SEX'], columns='EVENT_TYPE', values='POPULATION')
df_pivot_2 = df.pivot_table(index=['AREA'],columns='EVENT_TYPE', values='POPULATION')
df_pivot_3 = df.pivot_table(index=['AGE_ADJUSTED_RATE'],columns='EVENT_TYPE',values="POPULATION")
df_pivot_4 = df.pivot_table(index=['COUNT'],columns='EVENT_TYPE',values='POPULATION')

plot1 = df_pivot_1.plot(kind='bar')
plot1.legend(loc='upper right',title='Incidence and Mortality by SEX')
# plot1.set_ylabel('Incidence')
# plot1.set_xlabel('Mortality')
plt.show()

plot2 = df_pivot_2.plot(kind='bar')
plot2.legend(loc='upper right',title='Incidence and Mortality by AREA')
plt.show()

plot3 = df_pivot_3.plot(kind='bar')
plot3.legend(loc='upper right',title='Incidence and mortality by AGE')
plt.show()

plot4 = df_pivot_4.plot(kind='bar')
plot4.legend(loc='upper right',title='Incidence and mortality by COUNT')
plt.show()

# now using ggplot
ggp = ggplot(df, aes(x='EVENT_TYPE',group='SEX', y='POPULATION' )) + geom_bar(position="dodge", stat="identity")

df2 = df2.rename(columns={' FIPS': 'FIPS'})
df2 = df2.rename(columns={'Recent 5-Year Trend () in Incidence Rates': '5 Year Trend Incd Rates'})
df2 = df2.rename(columns={'Average Annual Count': 'Avg Ann Incd Count'})

# Remove columns not wanted to use in further analysis
# First create a list of columns in case you decide to go back and change list later
col_drop2 = ['Met Healthy People Objective of ***?','Age-Adjusted Incidence Rate() - cases per 100,000',\
            'Lower 95% Confidence Interval','Upper 95% Confidence Interval','Recent Trend',\
            'Lower 95% Confidence Interval.1','Upper 95% Confidence Interval.1']
df2.drop(col_drop2,inplace=True,axis=1)

df2.plot(x='County',y='Average Annual Count')
# US is the first row which has a very large number (i.e outlier) plotting w/o first row
df2[1:].plot(x='County',y='Average Annual Count')

# Now let's do the mortality dataset - Had same issues as the incidence in reading in..
df3= pd.read_csv(filename3,skiprows=8,nrows=3141,encoding = "ISO-8859-1")

# We see that the FIPS column has a empty space so we rename it. This column is very important for our analysis as
# FIPS can be used to correlate to other Datasets and their variables
df3 = df3.rename(columns={' FIPS': 'FIPS'})
df3 = df3.rename(columns={'Recent 5-Year Trend () in Death Rates': '5 Year Trend Death Rates'})
df3 = df3.rename(columns={'Average Annual Count': 'Avg Ann Death Count'})

# Remove columns not wanted to use in further analysis
# First create a list of columns in case you decide to go back and change list later
col_drop3 = ['Met Healthy People Objective of 161.4?','Age-Adjusted Death Rate() - deaths per 100,000',\
            'Lower 95% Confidence Interval','Upper 95% Confidence Interval','Recent Trend',\
            'Lower 95% Confidence Interval.1','Upper 95% Confidence Interval.1']
df3.drop(col_drop3,inplace=True,axis=1)

# Convert Average Annual Count and Incidence Rates columns to numeric
df3['Avg Ann Death Count'] = pd.to_numeric(df3['Avg Ann Death Count'], errors='coerce')
df3['5 Year Trend Death Rates'] = pd.to_numeric(df3['5 Year Trend Death Rates'], errors='coerce')

# Check that the FIPS coulumn has the same unique values. df3.FIPS

# assign file name for Medically Underserved Area (MUA)
filename4 = '~\PycharmProjects\Capstone-project\SB-capstone-project\Data\MUA_DET.csv'
# Read in CSV file as a panda dataframe: df4
df4 = pd.read_csv(filename4)

# rename column to match Incd FIPS column
df4 = df4.rename(columns={'Common State County FIPS Code': 'FIPS'})

# Merge df2 Incd Rate with df4 into fulldf
fulldf = df4.merge(df2[['FIPS', 'County','Avg Ann Incd Count','5 Year Trend Incd Rates']], on='FIPS', how='inner')
# Merge df3 Death Rate with df4 into fulldf
completedf = fulldf.merge(df3[['FIPS', 'County','Avg Ann Death Count','5 Year Trend Death Rates']], on='FIPS', how='inner')

# Need to verify the same amount of FIPS codes are in each dataset

# Continue EDA using ggplot on merged Datasets - working on finalizing these
cdfp1 = ggplot(completedf, aes(x='5 Year Trend Death Rates',y='Avg Ann Death Count', group='County_y')) + geom_bar(position="dodge", stat="identity")
cdfp2 = ggplot(completedf, aes(x='5 Year Trend Incd Rates',y='Avg Ann Incd Rates', group='County_y, col='County_y')) + facet.grid('FIPS'')
cdfp3 = ggplot(completedf, aes(x=))
