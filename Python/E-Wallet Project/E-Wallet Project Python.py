#import library and data
import pandas as pd
import numpy as np

product_data = pd.read_csv(
    "C:\\Users\\Admin\\Desktop\\DA books\\DA lesson\\Python\\product.csv"
)
transactions_data = pd.read_csv(
    "C:\\Users\\Admin\\Desktop\\DA books\\DA lesson\\Python\\transactions.csv"
)
payment_data = pd.read_csv(
    "C:\\Users\\Admin\\Desktop\\DA books\\DA lesson\\Python\\payment_report.csv"
)

#Check product data
print(product_data.info())

#check payment_report data
print(payment_data.info())

#check transactions data
print(transactions_data.info())

#Join product.csv and payment_report.csv, explore data  
payment_enriched = pd.merge(payment_data, product_data, on = "product_id")
payment_enriched["report_month"] = pd.to_datetime(
    payment_enriched["report_month"]
)

#Payment enriched data
#check missing values, datatype
print(payment_enriched.info())

#check incorrect values
print(payment_enriched.describe())

#change data type
payment_enriched["payment_group"] = payment_enriched["payment_group"].astype('string')
payment_enriched["category"] = payment_enriched["category"].astype('string')
payment_enriched["team_own"] = payment_enriched["team_own"].astype('string')

#Recheck duplicate
print("Duplicate data is: " + str(payment_enriched.duplicated().sum()))

#Recheck missing values
print("Null data in:")
print(payment_enriched.isna().sum())

#Recheck datatype

pd.set_option('display.max_columns', None)  
pd.set_option('display.width', 1000)

print(payment_enriched.info())

#Recheck incorrect values
print(payment_enriched.describe())

#Transactions data
#check missing values, datatype
print(transactions_data.info())

#Check incorrect values, 
print(transactions_data.describe())

#find duplicates data
print(transactions_data.isna().sum())

print("Num of Duplicated data is: " + str(transactions_data.duplicated().sum()))

#change data type, fill null, convert incorrect values(negative to positive)
transactions_data["receiver_id"] = transactions_data["receiver_id"].abs()
transactions_data["transStatus"] = transactions_data["transStatus"].abs()
transactions_data["sender_id"] = transactions_data["sender_id"].fillna(0).astype(int)
transactions_data["receiver_id"] = transactions_data["receiver_id"].fillna(0).astype(int)

#remove dup
transaction_remove_dup = transactions_data.drop_duplicates(subset= "transaction_id")

#Recheck duplicates

pd.set_option('display.max_columns', None)  
pd.set_option('display.width', 1000)

print("Num of Removed duplicated data is :" + str(transaction_remove_dup.duplicated().sum()))

#Recheck missing values , datatype
print("Null data in:")
print(transaction_remove_dup.info())

print(transaction_remove_dup.isna().sum())

#Recheck incorrect values
print(transaction_remove_dup.describe())

#sum volume and get top 3 products
total_volume = pd.DataFrame(payment_data.groupby("product_id")["volume"].sum())
top_3_productids = total_volume.sort_values("volume", ascending= False).head(3)

print(top_3_productids)

#total unique data, product owned by 1 team
total_unique = payment_enriched.groupby(
    "product_id", as_index = False)["team_own"].nunique()
team_normal = total_unique[total_unique["team_own"] == 1]
team_abnormal = total_unique[total_unique["team_own"] != 1]

pd.set_option('display.max_columns', None)  
pd.set_option('display.width', 1000)

print(total_unique)
print(team_normal)
print(team_abnormal)

#total volume by team since 2023-04
total = pd.DataFrame(
    payment_enriched[payment_enriched["report_month"].dt.quarter >= 2]
    .groupby("team_own")["volume"]
    .sum()
)
total["rank"] = total.sort_values("volume").rank()
print(total[total["rank"]== 1])

#find category have lowest contribution to that team (APS)
total1 = pd.DataFrame(
    payment_enriched[
        (payment_enriched["report_month"].dt.quarter >= 2) 
        & (payment_enriched["team_own"] == "APS")
    ]
    .groupby("category")["volume"]
    .sum()
)
total1["rank1"] = total1.sort_values("volume").rank()
print(total1[total1["rank1"]== 1])

contribution = pd.DataFrame(
    payment_data[payment_data["payment_group"] == "refund"]
    .groupby("source_id")["volume"]
    .sum()
)
contribution["rank_cont"] = contribution.sort_values("volume", ascending = False).rank(ascending= False)
print(contribution[contribution["rank_cont"] == 1])

#list of categories
transactions_data["sender_id"] = transactions_data["sender_id"].fillna(0).astype(int)
transactions_data["receiver_id"] = transactions_data["receiver_id"].fillna(0).astype(int)
transaction_remove_dup = transactions_data.drop_duplicates(subset= "transaction_id")
transaction_categories = [
    "Bank Transfer Transaction", 
    "Withdraw Money Transaction", 
    "Top Up Money Transaction",
    "Payment Transaction",
    "Transfer Money Transaction", 
    "Split Bill Transaction"
]
#list of conditions, through by each position in list
conditions = [
    (transaction_remove_dup["transType"] == 2) 
    & (transaction_remove_dup["merchant_id"] == 1205),
    (transaction_remove_dup["transType"] == 2) 
    & (transaction_remove_dup["merchant_id"] == 2260),
    (transaction_remove_dup["transType"] == 2) 
    & (transaction_remove_dup["merchant_id"] == 2270),
    (transaction_remove_dup["transType"] == 2) 
    & (~transaction_remove_dup["merchant_id"].isin([1205, 2260, 2270])),
    (transaction_remove_dup["transType"] == 8) 
    & (transaction_remove_dup["merchant_id"] == 2250),
    (transaction_remove_dup["transType"] == 8) 
    & (~transaction_remove_dup["merchant_id"].isin([2250]))]
transaction_remove_dup["transaction_type"]= np.select(
    conditions, transaction_categories, default = "Invalid Transactions"
)

pd.set_option('display.max_columns', None)  
pd.set_option('display.width', 1000)

print(transaction_remove_dup)

#num of transactions, volume, senders, receivers unique.
summarize_transaction = (
    transaction_remove_dup[
        transaction_remove_dup["transaction_type"] != "Invalid Transactions"
    ]
    .groupby("transaction_type")
    .agg(
        num_transactions = ("transaction_id", "nunique"),
        total_volume = ("volume", "sum"),
        num_senders = ("sender_id", "nunique"),
        num_receivers = ("receiver_id", "nunique")
    )
)

pd.set_option('display.max_columns', None)  
pd.set_option('display.width', 1000)

print(summarize_transaction)

