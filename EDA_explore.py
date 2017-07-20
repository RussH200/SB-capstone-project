import pandas as pd
import matplotlib.pyplot as plt
from ggplot import *

filename = "~\PycharmProjects\Capstone-project\SB-capstone-project\Data\BYAREA.TXT"
df = pd.read_table(filename,sep='|')

filename2 = "~\PycharmProjects\Capstone-project\SB-capstone-project\Data\incd.csv"
filename3 = "~\PycharmProjects\Capstone-project\SB-capstone-project\Data\death.csv"

df2= pd.read_csv(filename2,skiprows=8,nrows=3141,encoding = "ISO-8859-1")
df3= pd.read_csv(filename3,skiprows=8,nrows=3141,encoding = "ISO-8859-1")

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

df2.plot(x='County',y='Average Annual Count')
# US is the first row which has a very large number (i.e outlier) plotting w/o first row
df2[1:].plot(x='County',y='Average Annual Count')
