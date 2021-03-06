# Import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
# import ggplot

# Show download of BYAREA.TXT for reproducibility
# go to https://www.cdc.gov/cancer/npcr/uscs/download_data.htm
# download https://www.cdc.gov/cancer/npcr/uscs/USCS_1999_2013_ASCII.zip
# Unzip file 'BYAREA.TXT'

# Assign filename to BYAREA text file
filename = "~\PycharmProjects\Capstone-project\Data\BYAREA.TXT"
#filename2 = "~\PycharmProjects\Capstone-project\Data\incd.csv"
#filename3 = "~\PycharmProjects\Capstone-project\Data\death.csv"

# Read in CDC Wonder text file BYAREA and put in a dataframe df
#df = pd.read_table(filename,sep='|')

df = pd.read_table(filename,sep='|')

# Write out Dataframe as a CSV file byarea.csv
# df.to_csv("byarea.csv")
# df.to_csv('byarea_10k.csv')

# print out the columns names to check to see what we may need to cleanup and remove
df.columns

# print out the shape of dataframe rows by columns
df.shape

# print out the data types for the columns can also use df.dtypes
df.info

# Print out numeric data which is only the first(index[0] - unamed) column and the population column at this point
df.describe()
# Check for frequency counts in categorical data in event_type column of incidence and mortality also checking for
# NA's by dropna=FALSE
print(df['EVENT_TYPE'].value_counts(dropna=False))
print(df.EVENT_TYPE.all)

# Convert 'YEAR','COUNT','POPULATION' to a numeric dtypes
df.YEAR = pd.to_numeric(df.YEAR, errors='coerce')
df.COUNT = pd.to_numeric(df['COUNT'], errors='coerce')
df.POPULATION = pd.to_numeric(df['POPULATION'], errors='coerce')

# convert null datatypes to category to save memory usage
df.AREA = df.AREA.astype('category')
df.RACE = df.RACE.astype('category')
df.SEX = df.SEX.astype('category')
df.AGE_ADJUSTED_RATE = df.AGE_ADJUSTED_RATE.astype('category')
df.SITE = df.SITE.astype('category')
df.EVENT_TYPE = df.EVENT_TYPE.astype('category')

# Remove columns not wanted to use in further analysis
# First create a list of columns in case you decide to go back and change list later
col_drop = ['CRUDE_RATE','CRUDE_CI_LOWER','CRUDE_CI_UPPER','AGE_ADJUSTED_CI_LOWER','AGE_ADJUSTED_CI_UPPER']
df.drop(col_drop,inplace=True,axis=1)

# write out a new CSV file to save on disk space
# df.to_csv("byarea_new.csv")

# Bring in new dataset from cancer.org on Incidence for evaluation and cleanup
# Let's see if this new dataset maybe better based on variables that can be better correlated to
# other datasets - The goal is to make sure you can do our analysis based upon county in US
# When we first try to read in this csv file we get an error and decide to look at it in excel
# The first 8 rows happen to be header notes that we can ignore so we add skiprows=8.
# The next issue is an read_csv encoding error due to a non ASCII character we see if the Header Row #9.
# after trying many encoding options, we find ISO-8859-1 is the proper encoding to use.
# We then see that the first column has extra rows based upon trailing lines in the footer of the file which are more
# notes. We add nrows=3141 which matches all the other columns and allows us to read this in without changing
# the original file. One other check if I change nrows=3142 the last rows are Nan's using df.tail()

df2= pd.read_csv(filename2,skiprows=8,nrows=3141,encoding = "ISO-8859-1")

# check for relevant columns (variables) for our analysis
df2.columns

#check the dataframe
df2.info()

# We see that the FIPS column has a empty space so we rename it. This column is very important for our analysis as
# FIPS can be used to correlate to other Datasets and their variables
df2 = df2.rename(columns={' FIPS': 'FIPS'})
df2 = df2.rename(columns={'Recent 5-Year Trend () in Incidence Rates': '5 Year Trend Incd Rates'})

# Remove columns not wanted to use in further analysis
# First create a list of columns in case you decide to go back and change list later
col_drop2 = ['Met Healthy People Objective of ***?','Age-Adjusted Incidence Rate() - cases per 100,000',\
            'Lower 95% Confidence Interval','Upper 95% Confidence Interval','Recent Trend',\
            'Lower 95% Confidence Interval.1','Upper 95% Confidence Interval.1']
df2.drop(col_drop2,inplace=True,axis=1)

# Convert Average Annual Count and Incidence Rates columns to numeric
df2['Average Annual Count'] = pd.to_numeric(df2['Average Annual Count'], errors='coerce')
df2['5 Year Trend Incd Rates'] = pd.to_numeric(df2['5 Year Trend Incd Rates'], errors='coerce')

# That dataset seems ready to go now.

# Now let's do the mortality dataset - Had same issues as the incidence in reading in..
df3= pd.read_csv(filename3,skiprows=8,nrows=3141,encoding = "ISO-8859-1")

# check for relevant columns (variables) for our analysis
df3.columns

#check the dataframe
df3.info()

# We see that the FIPS column has a empty space so we rename it. This column is very important for our analysis as
# FIPS can be used to correlate to other Datasets and their variables
df3 = df3.rename(columns={' FIPS': 'FIPS'})
df3 = df3.rename(columns={'Recent 5-Year Trend () in Death Rates': '5 Year Trend Death Rates'})

# Remove columns not wanted to use in further analysis
# First create a list of columns in case you decide to go back and change list later
col_drop3 = ['Met Healthy People Objective of 161.4?','Age-Adjusted Death Rate() - deaths per 100,000',\
            'Lower 95% Confidence Interval','Upper 95% Confidence Interval','Recent Trend',\
            'Lower 95% Confidence Interval.1','Upper 95% Confidence Interval.1']
df3.drop(col_drop3,inplace=True,axis=1)

# Convert Average Annual Count and Incidence Rates columns to numeric
df3['Average Annual Count'] = pd.to_numeric(df3['Average Annual Count'], errors='coerce')
df3['5 Year Trend Death Rates'] = pd.to_numeric(df3['5 Year Trend Death Rates'], errors='coerce')


# Notice that Incidence and Mortality are in the same column EVENT_TYPE. These need to be in separate
# columns. Using Pivot table create 2 new variables, (Incidence, Mortality). Keeping Area, year, race and sex fixed.
# Use popolation as values argument as this will be the data that is in the incidence and mortality columns now
df_pivot_1 = df.pivot_table(index=['SEX'], columns='EVENT_TYPE', values='POPULATION')
df_pivot_2 = df.pivot_table(index=['AREA'],columns='EVENT_TYPE', values='POPULATION')
df_pivot_3 = df.pivot_table(index=['AGE_ADJUSTED_RATE'],columns='EVENT_TYPE',values="POPULATION")
df_pivot_4 = df.pivot_table(index=['COUNT'],columns='EVENT_TYPE',values='POPULATION')

#print out df_pivot to check on reporting format
df_pivot_1

# Plot some views of Incidence and Mortality based upon Population, AREA
# Plotting as a bar chart
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

# Filter EVENT_TYPE to create slices of Incidence and Mortality as their own dataframe
#df_incidence = df[df.EVENT_TYPE == "Incidence"]
#df_mortality = df[df.EVENT_TYPE == "Mortality"]

#df.incidence = df_incidence.rename(columns={'EVENT_TYPE': 'Incidence'})
#df.mortality = df_mortality.rename(columns={'EVENT_TYPE': 'Mortality'})

#df_incidence = df_incidence.reset_index
#df_mortality = df_mortality.reset_index
# merge the dataframes back together by merging them horizontally
#df_merge = pd.merge(df_incidence,df_mortality,left_on=['AREA','YEAR','RACE','SEX'],right_on=['POPULATION'])
# creates columns incidence and mortality
#df_merge = pd.merge(df_incidence,df_mortality,left_on="AREA",right_on='CRUDE_RATE')



