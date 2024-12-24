import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
import warnings
warnings.filterwarnings('ignore')
#import excel file
ecommerce_retail = pd.read_excel(
    r'C:\\Users\\Admin\\Desktop\\DA books\\DA lesson\\Python\\Final_project_RFM\\ecommerce retail.xlsx'
)

#check missing values, data type
print(ecommerce_retail.info())  

#Count number of missing values
print("Number of missing values in: ")

print(ecommerce_retail.isna().sum())

#Remove null valuese in Customer ID
ecommerce_retail= ecommerce_retail.drop(
    ecommerce_retail[ecommerce_retail['CustomerID'].isna()].index, axis = 0
)

#Recheck missing values
print("Number of missing values in: ")

print(ecommerce_retail.isna().sum())

#change data type
column_list = ['InvoiceNo','StockCode','Description','Country']
for c in column_list:
     ecommerce_retail[c] = ecommerce_retail[c].astype('string')
ecommerce_retail['CustomerID'] = ecommerce_retail['CustomerID'].astype(int) 

#Recheck data type
print(ecommerce_retail.info())

#check incorrect values, abnormal data, outliers
pd.set_option('display.max_columns', None)  
pd.set_option('display.width', 1000)

print(ecommerce_retail.describe())

#check negative values
pd.set_option('display.max_columns', None)  
pd.set_option('display.width', 1000)

print(ecommerce_retail[ecommerce_retail['UnitPrice'] < 0])

print(ecommerce_retail[ecommerce_retail['Quantity'] < 0])

#Count negative values in UnitPrice and Quantity
print((ecommerce_retail['UnitPrice'] < 0).sum())

print((ecommerce_retail['Quantity'] < 0).sum())

#Drop negative values in UnitPrice and Quantity
ecommerce_retail= ecommerce_retail.drop(
    ecommerce_retail[ecommerce_retail['UnitPrice']< 0].index, axis = 0
)

ecommerce_retail= ecommerce_retail.drop(
    ecommerce_retail[ecommerce_retail['Quantity']< 0].index, axis = 0
)

#Recheck negative values
print((ecommerce_retail['UnitPrice'] < 0).sum())

print((ecommerce_retail['Quantity'] < 0).sum())

#Recheck incorrect values, abnormal data, outliers
pd.set_option('display.max_columns', None)  
pd.set_option('display.width', 1000)

print(ecommerce_retail.describe())

#Recheck negative values in UnitPrice and Quantity
print((ecommerce_retail['UnitPrice'] < 0).sum())
print((ecommerce_retail['Quantity'] < 0).sum())

#Count number of duplicates
print("Number of duplicates is: " + str(ecommerce_retail.duplicated().sum()))

#remove duplicates, check duplicates again
ecommerce_retail_removedup = ecommerce_retail.drop_duplicates(
    ["InvoiceNo", "StockCode","InvoiceDate","CustomerID"], keep = 'first'
)

print("Number of duplicates is: " + str(ecommerce_retail_removedup.duplicated().sum()))

pd.set_option('display.max_columns', None)  
pd.set_option('display.width', 1000)

print(ecommerce_retail_removedup)

#Check number of cancelled Invoice
print("Number of cancel Invoice is: " + str((ecommerce_retail_removedup['InvoiceNo'].str.contains("^C")).sum()))

print(ecommerce_retail_removedup.info())

#date for Recency at 31-12-2011
date_R = dt.datetime(2011,12,31)

#Calculate Revenue
ecommerce_retail_removedup['Total_revenue'] = ecommerce_retail_removedup['Quantity'] * ecommerce_retail_removedup['UnitPrice']

#RFM model
RFM_model = ecommerce_retail_removedup.groupby('CustomerID').agg(
    Recency = ('InvoiceDate', lambda x: (date_R - x.max()).days),
    Frequency = ('InvoiceNo', lambda x: x.count()),
    Monetary = ('Total_revenue', lambda x: x.sum())
).reset_index()

print(RFM_model)
print(RFM_model.info())

# rank RFM marks
# RFM_model= RFM_model.sort_values(['Recency', 'Frequency', 'Monetary'], ascending=(True, False, False))
RFM_model['Recency_Score'] = pd.qcut(RFM_model['Recency'], q = 5, labels=[5,4,3,2,1])
RFM_model['Frequency_Score'] = pd.qcut(RFM_model['Frequency'], q = 5, labels=[1,2,3,4,5])
RFM_model['Monetary_Score'] = pd.qcut(RFM_model['Monetary'], q = 5, labels=[1,2,3,4,5])

#Calculate RFM Score
RFM_model['RFM_Score'] = (
    RFM_model['Recency_Score'].astype(str) + RFM_model['Frequency_Score'].astype(str) + RFM_model['Monetary_Score'].astype(str)
)
RFM_model['RFM_Score'] = RFM_model['RFM_Score'].astype(int)

pd.set_option('display.max_columns', None)  
pd.set_option('display.width', 1000)
print(RFM_model)
print(RFM_model.info())

#Check outliers in Recency
sns.boxplot(RFM_model, x = 'Recency')

#Check outliers in Frequency
sns.boxplot(RFM_model, x = 'Frequency')

#Check outliers in Monetary
sns.boxplot(RFM_model, x = 'Monetary')

#Setup IQR, upper, lower point for Recency
Seventy_fifth_R = RFM_model['Recency'].quantile(0.75)
Twenty_fifth_R = RFM_model['Recency'].quantile(0.25)
Recency_iqr = Seventy_fifth_R - Twenty_fifth_R
Recency_upper = Seventy_fifth_R + (1.5 * Recency_iqr)
Recency_lower = Twenty_fifth_R - (1.5 * Recency_iqr)

#Setup IQR, upper, lower point for Frequency
Seventy_fifth_F = RFM_model['Frequency'].quantile(0.75)
Twenty_fifth_F = RFM_model['Frequency'].quantile(0.25)
Frequency_iqr = Seventy_fifth_F - Twenty_fifth_F
Frequency_upper = Seventy_fifth_F + (1.5 * Frequency_iqr)
Frequency_lower = Twenty_fifth_F - (1.5 * Frequency_iqr)

#Setup IQR, upper, lower point for Monetary
Seventy_fifth_M = RFM_model['Monetary'].quantile(0.75)
Twenty_fifth_M = RFM_model['Monetary'].quantile(0.25)
Monetary_iqr = Seventy_fifth_M - Twenty_fifth_M
Monetary_upper = Seventy_fifth_M + (1.5 * Monetary_iqr)
Monetary_lower = Twenty_fifth_M - (1.5 * Monetary_iqr)

#Remove Outliers
RFM_model_remove_outliners = RFM_model[
    (RFM_model['Recency'] > Recency_lower) 
          & (RFM_model['Recency'] < Recency_upper)
     & (RFM_model['Frequency'] > Frequency_lower) 
          & (RFM_model['Frequency'] < Frequency_upper)
     & (RFM_model['Monetary'] > Monetary_lower) 
          & (RFM_model['Monetary'] < Monetary_upper)
]

#Recheck outliers in Recency
sns.boxplot(RFM_model_remove_outliners, x = 'Recency')

#Recheck outliers in Frequency
sns.boxplot(RFM_model_remove_outliners, x = 'Frequency')

#Recheck outliers in Monetary
sns.boxplot(RFM_model_remove_outliners, x = 'Monetary')

#import excel file, sheet 2
Segmentation = pd.read_excel(
    r'C:\\Users\\Admin\\Desktop\\DA books\\DA lesson\\Python\\Final_project_RFM\\ecommerce retail.xlsx', sheet_name = 'Segmentation'
)
print(Segmentation)

# Split values
Segmentation['RFM Score'] = Segmentation['RFM Score'].str.split(',')

Segmentation_sepe = Segmentation.explode('RFM Score').reset_index(drop = True)
Segmentation_sepe.rename(columns= {'RFM Score': 'RFM_Score'}, inplace= True)

Segmentation_sepe['RFM_Score'] = Segmentation_sepe['RFM_Score'].astype(int)

print(Segmentation_sepe)

RFM_Seg = pd.merge(
    RFM_model_remove_outliners, Segmentation_sepe, on= 'RFM_Score', how = 'inner'
)

pd.set_option('display.max_columns', None)  
pd.set_option('display.width', 1000)

print(RFM_Seg)

Cus_Seg = RFM_Seg.merge(
    ecommerce_retail_removedup[['CustomerID','Country']], on ='CustomerID', how = 'inner'
)
Cus_Seg = Cus_Seg.drop_duplicates()
pd.set_option('display.max_columns', None)  
pd.set_option('display.width', 1000)

print(Cus_Seg)

#Customer Segmentations
Customer_Segment = Cus_Seg['Segment'].value_counts().reset_index(name= 'Number_of_Cus')
total_customers = Customer_Segment['Number_of_Cus'].sum()
Customer_Segment['Percentage'] = (Customer_Segment['Number_of_Cus'] / total_customers) * 100.0
Customer_Segment['Percentage'] = Customer_Segment['Percentage'].round(2)

print(Customer_Segment)

#Customer Segmentation treemap  
import plotly.express as px

fig = px.treemap(
    Customer_Segment, 
    path = ['Segment'], values = 'Percentage',
    title = '% Distribution of Customer by Segmentation'
)

fig.update_traces(textinfo='label+value')
fig.update_layout(margin = dict(t = 50,l = 25, r = 30, b = 20))
fig.update_traces(texttemplate='%{label}<br>%{value}%')

fig.show()

category = RFM_Seg[["Segment","Recency","Frequency", "Monetary"]].groupby('Segment').agg(["mean", "min", "max"])

pd.set_option('display.max_columns', None)  
pd.set_option('display.width', 1000)

print(category)

