"""
Data Visualisation for the dataset "video game sales". This programme creates a PDF with different charts.

Data set taken from Kaggle: https://www.kaggle.com/gregorut/videogamesales

"""
# import all necessary modules
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np
from PyPDF2 import PdfFileMerger, PdfFileReader
import os 

data = pd.read_csv('vgsales.csv')

## clean up the data. 
# remove NaN values.
data = data.dropna(how = 'all')
data = data.fillna(0)
data = data.convert_dtypes()
data['Year'].astype('int64')

# convert year values to integers from floats.
data.drop(data[data.Year == 0].index, inplace=True)
data.head()

'''A bar plot showing the value of global video games sales for each year'''
# set figure size
fig = plt.figure(figsize=(15,10))
# plot the data
total_sales_year = data.groupby('Year').sum()['Global_Sales']
years = list(range(1980, 2018))+[2020]
plt.bar(years, total_sales_year)
# add title and labels
plt.title('Global Video Game Sales', fontweight='bold', color='g', size=20)
plt.xlabel('Year', size=18)
plt.ylabel('Global Sales in mln USD', size=18)
# save chart as pdf
fig.savefig('chart1.pdf')

'''4 charts representing sales in each region for each year'''
# create variables to represent needed columns of data 
na_sales_year = data.groupby('Year').sum()['NA_Sales']
eu_sales_year = data.groupby('Year').sum()['EU_Sales']
jp_sales_year = data.groupby('Year').sum()['JP_Sales']
ot_sales_year = data.groupby('Year').sum()['Other_Sales']

# create charts 
fig, axs = plt.subplots(2, 2, figsize=(15,10))
axs[0, 0].plot(years, na_sales_year)
axs[0, 0].set_title('NA Sales', fontweight='bold')
axs[0, 1].plot(years, eu_sales_year, 'tab:orange')
axs[0, 1].set_title('EU Sales', fontweight='bold')
axs[1, 0].plot(years, jp_sales_year, 'tab:green')
axs[1, 0].set_title('JP Sales', fontweight='bold')
axs[1, 1].plot(years, ot_sales_year, 'tab:red')
axs[1, 1].set_title('Other Sales', fontweight='bold')

# set labels and right distance between charts
for ax in axs.flat:
    if ax == axs.flat[0]:
        ax.set(xlabel=None, ylabel='Total Sales')
    if ax == axs.flat[2]:
        ax.set(xlabel='Year', ylabel='Total Sales')
    if ax == axs.flat[3]:
        ax.set(xlabel='Year', ylabel=None)
fig.tight_layout(pad=1.0)
# save chart
fig.savefig('chart2.pdf')

'''Grouped bar chart demonstrating 10 best-selling video games (global sales) of all years'''
# sort data
vg_names = list(data['Name'].unique())
top_10_names = vg_names[:10]
vg_sales = data.groupby(['Name']).sum().sort_values('Global_Sales', ascending=False)
# create variables that represent a list of values of global sales for top 10 games in each region
top_10_values_na = vg_sales['NA_Sales'].head(10)
top_10_values_eu = vg_sales['EU_Sales'].head(10)
top_10_values_jp = vg_sales['JP_Sales'].head(10)
top_10_values_other = vg_sales['Other_Sales'].head(10)

#  set figure size 
fig = plt.figure(figsize=(15,10))
# plot the data
w = 0.2
b1 = np.arange(len(top_10_names))
b2 = [x + w for x in b1]
b3 = [x + w for x in b2]
b4 = [x + w for x in b3]

plt.bar(b1, top_10_values_na, color='#0097E0', width=w, edgecolor='white', label='NA Sales')
plt.bar(b2, top_10_values_eu, color='#FFA200', width=w, edgecolor='white', label='EU Sales')
plt.bar(b3, top_10_values_jp, color='#2DCF00', width=w, edgecolor='white', label='JP Sales')
plt.bar(b4, top_10_values_other, color='#CF0000', width=w, edgecolor='white', label='Other Sales')
 
# add title and lables
plt.title('Top 10 Games', fontweight='bold', color='g', size=20)
plt.ylabel('Sales in mln USD', size=18)
plt.xticks([r + w for r in range(len(top_10_names))], list(top_10_names), rotation=35, size=8, fontweight='bold', ha='right')

# create legend
plt.legend() 
# save the chart
fig.savefig('chart3.pdf')

'''Horizontal bar chart showing what platforms have the most games'''
# remove columns we don't need 
platform_data = data.drop(columns=['Rank', 'Year', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Genre', 'Publisher'])

# group by platform and sort data
platform_data = platform_data.groupby('Platform').sum().sort_values('Global_Sales', ascending=False)

# convert dataframe into a dictionary like {index -> {column -> value}}
data_dict = platform_data.to_dict(orient='index')
top_10_platforms = list(data_dict.keys())[:10]

top_10_platforms_sales_prep = list(data_dict.values())
top_10_platforms_sales = []
for i in top_10_platforms_sales_prep:
    top_10_platforms_sales.append(list(i.values())[0])
top_10_platforms_sales = top_10_platforms_sales[:10]

# create a horizontal bar chart
fig = plt.figure(figsize=(15,10))
plt.barh(top_10_platforms, top_10_platforms_sales)
plt.title('Top 10 Platforms', fontweight='bold', color='g', size=20)
plt.ylabel('Platform', size=18)
plt.xlabel('Sales in mln USD', size=18)
fig.savefig('chart4.pdf')

##create a pdf
# call a file merger
merged = PdfFileMerger()
 
# loop through all charts and append them to the merged pdf file
for n in range(1, 5):
    merged.append(PdfFileReader('chart' + str(n)+ '.pdf', 'rb'))
 
# write all the files into a file named as shown below
merged.write("Video Game Sales Report.pdf")

# delete charts 1 to 4
for ch in ['chart1.pdf', 'chart2.pdf', 'chart3.pdf', 'chart4.pdf']:
    os.remove(ch)