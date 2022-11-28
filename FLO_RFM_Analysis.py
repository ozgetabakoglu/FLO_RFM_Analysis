
###############################################################
# Customer Segmentation with RFM
###############################################################

###############################################################
# Business Problem
###############################################################
# FLO wants to divide its customers into segments and determine marketing strategies according to these segments.
# For this purpose, the behaviors of the customers will be defined and groups will be formed according to these behavior clusters.

################################################ ###############
# Dataset Story
################################################ ###############

# The dataset consists of information obtained from the past shopping behaviors of
# customers who made their last purchases as OmniChannel (both online and offline shopper) in 2020 - 2021.

# master_id: Unique client number
# order_channel : Which channel of the shopping platform is used (Android, ios, Desktop, Mobile, Offline)
# last_order_channel : The channel where the last purchase was made
# first_order_date : The date of the customer's first purchase
# last_order_date : The date of the last purchase made by the customer
# last_order_date_online : The date of the last purchase made by the customer on the online platform
# last_order_date_offline : The date of the last purchase made by the customer on the offline platform
# order_num_total_ever_online : The total number of purchases made by the customer on the online platform
# order_num_total_ever_offline : Total number of purchases made by the customer offline
# customer_value_total_ever_offline : The total price paid by the customer for offline purchases
# customer_value_total_ever_online : The total price paid by the customer for their online shopping
# interested_in_categories_12 : List of categories the customer has purchased from in the last 12 months

################################################ ###############
# TASKS
################################################ ###############

# TASK 1: Data Understanding and Preparation
           # 1. Read the flo_data_20K.csv data.
           #2. In the dataset
                     # a. top 10 observations,
                     # b. variable names,
                     # c. descriptive statistics,
                     # D. null value,
                     # e. Variable types, review.
           # 3. Omnichannel means that customers shop from both online and offline platforms. Total for each customer
           # create new variables for number of purchases and spend.
           # 4. Examine the variable types. Change the type of variables that express date to date.
           # 5. Look at the breakdown of the number of customers, average number of products purchased, and average spend in shopping channels.
           # 6. Rank the top 10 customers with the most revenue.
           # 7. Rank the top 10 customers with the most orders.
           # 8. Functionalize the data provisioning process.

# TASK 2: Calculating RFM Metrics

# TASK 3: Calculating RF and RFM Scores

# TASK 4: Defining RF Scores as Segments

# TASK 5: Time for action!
# 1. Examine the recency, frequency and monetary averages of the segments.
# 2. With the help of RFM analysis, find the customers in the relevant
# profile for 2 cases and save the customer IDs to the csv.
 # a. FLO includes a new women's shoe brand. The product prices of the brand it includes are
 # above the general customer preferences. For this reason, customers in the profile who will be interested in the promotion
 # of the brand and product sales are requested to be contacted privately. Those who shop from their loyal customers (champions, loyal_customers),
 # on average over 250 TL and from the women category, are the customers to contact privately. Save the id numbers of these
 # customers in the csv file as new_brand_target_customer_id.cvs.
 # b. Up to 40% discount is planned for Men's and Children's products. It is aimed to specifically target customers
 # who are good customers in the past, but who have not shopped for a long time, who are interested in the categories
 # related to this discount, who should not be lost, who are asleep and new customers. Save the ids of the customers
 # in the appropriate profile to the csv file as discount_target_customer_ids.csv.


# TASK 6: Functionalize the whole process.

################################################ ###############
# TASK 1: Data Understanding
################################################ ###############

import pandas as pd
import datetime as dt
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.set_option('display.width',1000)



# 1. Read the data flo_data_20K.csv. Make a copy of the dataframe.
df_ = pd.read_csv("Module_2_CRM_Analitigi/Dataset/flo_data_20K.csv")
df = df_.copy()
df.head()


#2. In the dataset
         # a. top 10 observations,
         # b. variable names,
         # c. Dimension,
         # D. descriptive statistics,
         # e. null value,
         # f. Variable types, review.

df.head(10)
df.columns
df.shape
df.describe().T
df.isnull().sum()
df.info()


# 3. Omnichannel means that customers shop from both online and offline platforms.
# Create new variables for each customer's total number of purchases and spending.
df["order_num_total"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["customer_value_total"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]

# 4. Examine the variable types. Change the type of variables that express date to date.
date_columns = df.columns[df.columns.str.contains("date")]
df[date_columns] = df[date_columns].apply(pd.to_datetime)
df.info()

# 5. Look at the distribution of the number of customers in the shopping channels, the total number of products purchased and total expenditures.
df.groupby("order_channel").agg({"master_id":"count",
                                  "order_num_total":"sum",
                                  "customer_value_total":"sum"})

# 6. Rank the top 10 customers with the most revenue.
df.sort_values("customer_value_total", ascending=False)[:10]

# 7. Rank the top 10 customers with the most orders.
df.sort_values("order_num_total", ascending=False)[:10]

# 8. Functionalize the data provisioning process.
def data_prep(dataframe):
    dataframe["order_num_total"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["customer_value_total"] = dataframe["customer_value_total_ever_offline"] + dataframe["customer_value_total_ever_online"]
    date_columns = dataframe.columns[dataframe.columns.str.contains("date")]
    dataframe[date_columns] = dataframe[date_columns].apply(pd.to_datetime)
    return df

################################################ ###############
# TASK 2: Calculating RFM Metrics
################################################ ###############

# Analysis date 2 days after the last shopping date in the data set
df["last_order_date"].max() # 2021-05-30
analysis_date = dt.datetime(2021,6,1)


# A new rfm dataframe with customer_id, recency, frequnecy and monetary values
rfm = pd.DataFrame()
rfm["customer_id"] = df["master_id"]
rfm["recency"] = (analysis_date - df["last_order_date"]).astype('timedelta64[D]')
rfm["frequency"] = df["order_num_total"]
rfm["monetary"] = df["customer_value_total"]

rfm.head()

################################################ ###############
# TASK 3: Calculating RF and RFM Scores
################################################ ###############

# Converting Recency, Frequency and Monetary metrics to scores between 1-5
# with the help of qcut and saving these scores as recency_score, frequency_score and monetary_score
rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm.head()


# Express recency_score and frequency_score as a single variable and save it as RF_SCORE
rfm["RF_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str))


# 3. Expressing recency_score and frequency_score and monetary_score as a single variable and saving it as RFM_SCORE
rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str) + rfm['monetary_score'].astype(str))

rfm.head()

################################################ ###############
# TASK 4: Defining RF Scores as Segments
################################################ ###############

# Segment definition and conversion of RF_SCORE to segments with the help of defined seg_map so that the generated RFM scores can be explained more clearly.
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm['segment'] = rfm['RF_SCORE'].replace(seg_map, regex=True)
rfm['segment']
rfm.head()

###############################################################
# TASK 5: Time for action!
################################################ ###############

# 1. Examine the recency, frequency and monetary averages of the segments.
rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

#                          recency       frequency       monetary
#                        mean count      mean count     mean count
# segment
# about_to_sleep       113.79  1629      2.40  1629   359.01  1629
# at_Risk              241.61  3131      4.47  3131   646.61  3131
# cant_loose           235.44  1200     10.70  1200  1474.47  1200
# champions             17.11  1932      8.93  1932  1406.63  1932
# hibernating          247.95  3604      2.39  3604   366.27  3604
# loyal_customers       82.59  3361      8.37  3361  1216.82  3361
# need_attention       113.83   823      3.73   823   562.14   823
# new_customers         17.92   680      2.00   680   339.96   680
# potential_loyalists   37.16  2938      3.30  2938   533.18  2938
# promising             58.92   647      2.00   647   335.67   647


#How many segments are there and how many %.
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Qt5Agg')

segments_counts = rfm['segment'].value_counts().sort_values(ascending=True)

fig, ax = plt.subplots()

bars = ax.barh(range(len(segments_counts)),
              segments_counts,
              color='silver')
ax.set_frame_on(False)
ax.tick_params(left=False,
               bottom=False,
               labelbottom=False)
ax.set_yticks(range(len(segments_counts)))
ax.set_yticklabels(segments_counts.index)

for i, bar in enumerate(bars):
        value = bar.get_width()
        if segments_counts.index[i] in ['Can\'t loose']:
            bar.set_color('firebrick')
        ax.text(value,
                bar.get_y() + bar.get_height()/2,
                '{:,} ({:}%)'.format(int(value),
                                   int(value*100/segments_counts.sum())),
                va='center',
                ha='left'
               )

plt.show()


# 2. With the help of RFM analysis, find the customers in the relevant profile for 2 cases and save the customer IDs to the csv.

# a. FLO includes a new women's shoe brand. The product prices of the brand it includes are above the general customer preferences.
# For this reason, customers in the profile who will be interested in the promotion of the brand and product sales are
# requested to be contacted privately. These customers were planned to be loyal and female shoppers.
# Save the id numbers of the customers to the csv file as new_brand_target_customer_id.cvs.
target_segments_customer_ids = rfm[rfm["segment"].isin(["champions","loyal_customers"])]["customer_id"]
cust_ids = df[(df["master_id"].isin(target_segments_customer_ids)) &(df["interested_in_categories_12"].str.contains("KADIN"))]["master_id"]
cust_ids.to_csv("yeni_marka_hedef_müşteri_id.csv", index=False)
cust_ids.shape

rfm.head()


# b. Up to 40% discount is planned for Men's and Children's products.
# We want to specifically target customers who are good customers in the past who are interested in categories
# related to this discount, but have not shopped for a long time and new customers.
# Save the ids of the customers in the appropriate profile to the csv file as discount_target_customer_ids.csv.
target_segments_customer_ids = rfm[rfm["segment"].isin(["cant_loose","hibernating","new_customers"])]["customer_id"]
cust_ids = df[(df["master_id"].isin(target_segments_customer_ids)) & ((df["interested_in_categories_12"].str.contains("ERKEK"))|(df["interested_in_categories_12"].str.contains("COCUK")))]["master_id"]
cust_ids.to_csv("indirim_hedef_müşteri_ids.csv", index=False)


###############################################################
# BONUS
###############################################################

def create_rfm(dataframe):
    # Preparing Data
    dataframe["order_num_total"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["customer_value_total"] = dataframe["customer_value_total_ever_offline"] + dataframe["customer_value_total_ever_online"]
    date_columns = dataframe.columns[dataframe.columns.str.contains("date")]
    dataframe[date_columns] = dataframe[date_columns].apply(pd.to_datetime)


    # CALCULATION OF RFM metrics
    dataframe["last_order_date"].max()  # 2021-05-30
    analysis_date = dt.datetime(2021, 6, 1)
    rfm = pd.DataFrame()
    rfm["customer_id"] = dataframe["master_id"]
    rfm["recency"] = (analysis_date - dataframe["last_order_date"]).astype('timedelta64[D]')
    rfm["frequency"] = dataframe["order_num_total"]
    rfm["monetary"] = dataframe["customer_value_total"]

    # CALCULATION OF RF and RFM SCORES
    rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])
    rfm["RF_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str))
    rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str) + rfm['monetary_score'].astype(str))


    # NAMING OF SEGMENTS
    seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_Risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }
    rfm['segment'] = rfm['RF_SCORE'].replace(seg_map, regex=True)

    return rfm[["customer_id", "recency","frequency","monetary","RF_SCORE","RFM_SCORE","segment"]]

rfm_df = create_rfm(df)



