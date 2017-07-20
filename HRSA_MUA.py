# HRSA_evaluate file our 4th Dataset which includes FIPS columns for state and county as well as Medically underserved
# areas and the population in those areas.

# import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt

# assign file name for Medically Underserved Area (MUA)
filename4 = '~\PycharmProjects\Capstone-project\Data\MUA_DET.csv'

# Read in CSV file as a panda dataframe: df4
df4 = pd.read_csv(filename4)

# print out info on Dataframe: df4
df4.info

# check out column names - These were filter by website data output - can be changed or filtered in DF
df4.columns

# print out numeric data
df4.describe()




