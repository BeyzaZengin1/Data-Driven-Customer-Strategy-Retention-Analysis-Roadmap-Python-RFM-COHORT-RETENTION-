
## DATA LOADING

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt



## DISPLAY SETTINGS

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 1000)
df = pd.read_csv(r'C:\Users\Hp\Sample - Superstore (1).csv', encoding='latin-1')


## EDA

print(df.head())
print(df.shape)
print(df.columns)
print(df.isnull().sum())  # No null values
print(df.info())  # Inconsistent data types
print(df.describe().T)
print(df.duplicated().sum())  # 0


## ADVANCED EDA

# Identified all categorical variables
cat_cols = [col for col in df.columns if str(df[col].dtypes) in ["category", "object", "bool"]]
# Numerical but categorical
num_but_cat = [col for col in df.columns if df[col].nunique() < 15 and df[col].dtypes in ['int64','float64']]
# Categorical but cardinal
cat_but_car = [col for col in df.columns if df[col].nunique() > 20 and df[col].dtype.name in ["category", "object"]]
# Categorical columns
cat_cols = cat_cols + num_but_cat
cat_cols = [col for col in cat_cols if col not in cat_but_car]
# Numericals
num_cols = [col for col in df.columns if df[col].dtypes in ["int64", "float64"]]
num_cols = [col for col in num_cols if col not in num_but_cat]


# Fixed all data types using a function

def set_column_types(df, cat_cols, num_cols, cat_but_car, num_but_cat):
    # Automatic Date Detection
    date_cols = [col for col in df.columns if "Date" in col]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    # Convert numerical but categorical variables to category type
    for col in num_but_cat:
        df[col] = df[col].astype("category")

    # Cast object columns to category
    for col in cat_cols:
        if col not in cat_but_car:
            df[col] = df[col].astype("category")

    # Cast true numerical columns to float/int
    for col in num_cols:
        if col not in num_but_cat:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Exception
    if "Postal Code" in df.columns:
        df["Postal Code"] = df["Postal Code"].astype(str)

    return df


df = set_column_types(df, cat_cols, num_cols, cat_but_car, num_but_cat)


df.info()


## DATA VALIDATION

# Date Consistency
print(df[df['Ship Date'] < df['Order Date']])
# Inconsistent values
# Show rows where Quantity is 0 or negative; 0 is problematic
df['Quantity'].value_counts()
print(df[df['Sales'] <= 0])  # 0
print(df[df['Profit'] < 0])  # 1871 rows
# Check for abnormal discounts (out of range 0-1)
print(df["Discount"].value_counts())
# Are there multiple names for the same ID?
df.groupby('Customer ID')['Customer Name'].nunique().sort_values(ascending=False)
# Quantity > 0 but Sales = 0
qty_zero_sales = df[(df['Quantity'].astype(int) > 0) & (df['Sales'] == 0)]
# Discount > 0 but Sales is illogically high
# Hypothetical: Sales < Discount * Sales might be illogical
# Checking for Discount > 1 or scenarios where Discount > 0 but Sales is 0
discount_issue = df[(df['Discount'].astype(float) > 0) & (df['Sales'] <= 0)]


print(df[['Sales', 'Profit']].describe().T)


## IQR CALCULATION
# Detecting outliers with visualization methods

num_cols = df.select_dtypes(include=[np.number]).columns
for i, col in enumerate(num_cols):
    plt.figure(figsize=(6, 2))
    sns.boxplot(x=df[col])
    plt.title(f"{col} Outlier Analysis")
    plt.show()


# Defined outlier thresholds using this function

def outlier_thresholds(dataframe, col_name, q1=0.25, q3=0.75, factor=1.5):
    quartile1 = dataframe[col_name].quantile(q1)
    quartile3 = dataframe[col_name].quantile(q3)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + factor * interquantile_range
    low_limit = quartile1 - factor * interquantile_range
    return low_limit, up_limit



# WINSORIZATION FUNCTION

def replace_with_thresholds(dataframe, variable, low_limit, up_limit):
    dataframe.loc[dataframe[variable] < low_limit, variable] = low_limit
    dataframe.loc[dataframe[variable] > up_limit, variable] = up_limit
    return dataframe




# SALES CLEANING

#I used winsorization for Sales outlier cleaning because high-value sales carry significant business value
low_s, up_s = outlier_thresholds(df, "Sales", factor=3)  # I only trimmed the extreme edges. Using a $1.5 \times IQR$ threshold would have been too aggressive, removing too much data and discarding valuable customers.
# I prioritized preserving the data distribution.
low_s = max(low_s, 0) # Sales cannot be negative. In RFM, we measure the total value a customer has generated, so zero or negative values are irrelevant and must be corrected.


# WINSORIZE

df = replace_with_thresholds(df, "Sales", low_s, up_s)



# IQR

low_p, up_p = outlier_thresholds(df, "Profit", factor=3)



# WINSORIZE

df = replace_with_thresholds(df, "Profit", low_p, up_p)



# CONTROLLING

print(df[["Sales", "Profit"]].describe().T)



## RFM

# Calculating rfm metrics
today_date = df['Order Date'].max() + dt.timedelta(days=2) #If we had used today's date, the Recency would be wrong

rfm = df.groupby('Customer ID').agg({
    'Order Date': lambda x: (today_date - x.max()).days,
    'Order ID': lambda x: x.nunique(),
    'Sales': lambda x: x.sum()})



# Adding column names

rfm.columns = ['recency', 'frequency', 'monetary']



# SCORING

rfm["recency_score"] = pd.qcut(rfm['recency'].rank(method="first"), 5, labels=[5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["monetary_score"] = pd.qcut(rfm['monetary'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])



# CALCULATING RF_SCORE 

rfm["RF_SCORE"] = rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str)

# SEGMENT MAP

seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_risk',
    r'[1-2]5': 'cant_lose_them',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}



rfm['segment'] = rfm['RF_SCORE'].replace(seg_map, regex=True)



# Data type casting for calculations

rfm['recency'] = rfm['recency'].astype(int)
rfm['frequency'] = rfm['frequency'].astype(int)
rfm['monetary'] = rfm['monetary'].astype(float)



print(rfm['segment'].value_counts())


# STATISTICAL SUMMARY BY SEGMENT

rfm_stats = rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count", "sum"])



# Redefined columns with clear and descriptive names

rfm_stats.columns = ['_'.join(col).strip() for col in rfm_stats.columns.values]
rfm_stats = rfm_stats.reset_index()
rfm_stats = rfm_stats.sort_values(by="monetary_sum", ascending=False)
#rfm['monetary'] = pd.to_numeric(rfm['monetary'], errors='coerce')


print(rfm_stats)



# Customer count and total revenue share by segment: Which segment generates the most revenue?

segment_analysis = rfm.groupby("segment").agg({"monetary": ["count", "sum"]})
segment_analysis.columns = ["customer_count", "total_monetary"]
print(segment_analysis)



# Calculating percentage distributions

total_customers = segment_analysis["customer_count"].sum()
total_revenue = segment_analysis["total_monetary"].sum()



segment_analysis["customer_share_%"] = (segment_analysis["customer_count"] / total_customers) * 100
segment_analysis["revenue_share_%"] = (segment_analysis["total_monetary"] / total_revenue) * 100

print(segment_analysis.sort_values(by="revenue_share_%", ascending=False))
print(segment_analysis.sort_values(by="customer_share_%", ascending=False))



# High monetary value but low frequency (Big Spenders)

big_spenders = rfm[(rfm["monetary_score"] == 5) & (rfm["recency_score"] >= 3)]

print(f"Total of {len(big_spenders)} 'Whale' customers identified, but they are not Champions!")
print(big_spenders[["recency", "frequency", "monetary", "segment"]].head())



df['Discount'] = df['Discount'].astype(float)



# Calculate customer-based discount metrics

discount_analysis = df.groupby('Customer ID').agg({
    'Discount': ['mean', 'count', lambda x: (x > 0).sum()], # Average discount, total transactions, discounted transactions count
    'Sales': 'sum'
}).reset_index()

# Clean up column names
discount_analysis.columns = ['Customer ID', 'avg_discount_rate', 'total_transactions', 'discounted_transactions_count', 'total_spend']

# Calculate Discounted Transaction Ratio (%)
# (What percentage of transactions included a discount?)
discount_analysis['discount_dependency_ratio'] = (discount_analysis['discounted_transactions_count'] / discount_analysis['total_transactions']) * 100

# Defined "Discount Hunters" 
# Criteria: Customers with more than 70% of transactions discounted and an average discount rate above the company average.
threshold_ratio = 0.7
avg_market_discount = discount_analysis['avg_discount_rate'].mean()

discount_hunters = discount_analysis[(discount_analysis['discount_dependency_ratio'] >= threshold_ratio) & 
    (discount_analysis['avg_discount_rate'] > avg_market_discount)].sort_values(by='discount_dependency_ratio', ascending=False)

# Merge with RFM Segments (How many discount hunters are in each segment?)
# Merge with your rfm table (where the segments are stored)
final_discount_report = rfm.merge(discount_analysis[['Customer ID', 'discount_dependency_ratio', 'avg_discount_rate']], on='Customer ID')

print(f"Total of {len(discount_hunters)} 'Discount Hunters' identified.")
print("-" * 30)
print(discount_hunters.head(10))

# Segment-based Discount Sensitivity Summary
segment_discount_summary = final_discount_report.groupby('segment').agg({
    'discount_dependency_ratio': 'mean',
    'avg_discount_rate': 'mean',
    'Customer ID': 'count'
}).sort_values(by='discount_dependency_ratio', ascending=False)

print("\n--- Segment Discount Dependency Summary ---")
print(segment_discount_summary)


# Calculate discount metrics from the dataset 
discount_metrics = df.groupby('Customer ID').agg({
    'Discount': 'mean',  # Average discount rate (%)
    'Sales': 'sum'  # Total spend
}).reset_index()



# Merge with the RFM table (the table containing segments)

rfm_discount = rfm.merge(discount_metrics, on='Customer ID', how='left')





# Analyze discount utilization by segment

segment_discount_report = rfm_discount.groupby('segment').agg({
    'Discount': 'mean',  # Average discount rate of the segment
    'Customer ID': 'count',  # Number of customers in the segment
    'monetary': 'mean'  # Average spend per customer
}).sort_values(by='Discount', ascending=False)

print("--- Segment-Based Discount Sensitivity ---")
print(segment_discount_report)



df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce').fillna(0)



# High-value customers at risk of churning

danger_zone = rfm[
    (rfm["segment"].isin(["cant_lose_them", "at_risk"])) &
    (rfm["monetary_score"].astype(int) >= 4) &
    (rfm["frequency_score"].astype(int) >= 3)].sort_values("monetary", ascending=False)



print(f"URGENT INTERVENTION REQUIRED: {len(danger_zone)} High-Value Customers Identified!")
print(danger_zone.head(10))



# Sorted customers by total spending in descending order

rfm_sorted = rfm.sort_values("monetary", ascending=False)
rfm_sorted['cum_sum'] = rfm_sorted['monetary'].cumsum()
total_revenue = rfm_sorted['monetary'].sum()
rfm_sorted['revenue_share'] = (rfm_sorted['cum_sum'] / total_revenue) * 100



# Identified the core customer group generating 80% of total revenue

pareto_limit = rfm_sorted[rfm_sorted['cum_sum'] <= total_revenue * 0.8]
pareto_percentage = (len(pareto_limit) / len(rfm)) * 100

print(f"Insight: {pareto_percentage:.1f}% of customers generate 80% of total revenue.")




# List of customers in the Pareto group
pareto_customers = pareto_limit.copy()

# Analyze the distribution of these customers across segments
pareto_segment_dist = pareto_customers['segment'].value_counts()

print(f"A total of {len(pareto_customers)} customers generate 80% of the total revenue.")
print("\n--- Segment Distribution of Pareto Group Customers ---")
print(pareto_segment_dist)

# Display the top 20 rows of this list
print("\n--- Top 20 Customers Driving 80% of Revenue ---")
print(pareto_customers[['recency', 'frequency', 'monetary', 'segment', 'cum_sum']].head(20))



# Map segment information back to the main dataframe (df)

df_with_segments = df.merge(rfm[['segment']], on='Customer ID', how='left')



# Identified the top 3 most preferred categories per segment

top_products_by_segment = df_with_segments.groupby(['segment', 'Category'], observed=False)['Order ID'].nunique().reset_index()
top_products_by_segment = top_products_by_segment.sort_values(['segment', 'Order ID'], ascending=[True, False])

print("MOST POPULAR CATEGORIES BY SEGMENT:")
print(top_products_by_segment.groupby('segment').head(2))


# Reset index to clean up the table and make segment names visible
# If the segment column is set as index, reset_index() brings it back as a column
rfm_stats_clean = rfm_stats.reset_index()

rfm_stats_clean['AOV'] = rfm_stats_clean['monetary_sum'] / rfm_stats_clean['monetary_count']

# Display sorted Average Order Value (AOV) results by segment
print("AVERAGE ORDER VALUE (AOV) BY SEGMENT:")
aov_report = rfm_stats_clean[['segment', 'AOV']].sort_values(by='AOV', ascending=False)
print(aov_report)


# COHORT ANALYSIS


#  DATA PREPARATION


df['Order Date'] = pd.to_datetime(df['Order Date'])

# Monthly breakdown
df['Order Month'] = df['Order Date'].dt.to_period('M').dt.to_timestamp()

# First purchase month (Cohort Month)
df['Cohort Month'] = df.groupby('Customer ID')['Order Month'].transform('min')


# COHORT INDEX


def get_date_int(df, column):
    year = df[column].dt.year
    month = df[column].dt.month
    return year, month

order_year, order_month = get_date_int(df, 'Order Month')
cohort_year, cohort_month = get_date_int(df, 'Cohort Month')

years_diff = order_year - cohort_year
months_diff = order_month - cohort_month

df['CohortIndex'] = years_diff * 12 + months_diff + 1

# COHORT TABLE (ABSOLUTE VALUES)


cohort_group = (df.groupby(['Cohort Month', 'CohortIndex'])['Customer ID'].nunique().reset_index())

cohort_counts = cohort_group.pivot(
    index='Cohort Month',
    columns='CohortIndex',
    values='Customer ID'
).fillna(0)


# RETENTION MATRIX 

if 1 not in cohort_counts.columns:
    raise ValueError("Cohort index 1 does not exist → retention cannot be calculated")

# Replace 0 with NaN to avoid division by zero errors
cohort_sizes = cohort_counts[1].replace(0, np.nan)

# Calculate retention rates
retention = cohort_counts.divide(cohort_sizes, axis=0)

# Format index as Year-Month
retention.index = retention.index.strftime('%Y-%m')



# RETENTION DROP ANALYSIS

avg_retention = retention.mean(axis=0)
retention_diff = avg_retention.diff()

print("\n Monthly Retention Change:")
print(retention_diff)

print("\n Worst Drop Month:", retention_diff.idxmin())
print(" Max Drop Value:", retention_diff.min())


# COHORT SIZE INSIGHT


cohort_summary = pd.DataFrame({
    "cohort_size": cohort_sizes
})

print("\n Cohort Sizes:")
print(cohort_summary.head())



# TOP / BOTTOM COHORTS


print("\n Best Cohorts (avg retention):")
print(retention.mean(axis=1).sort_values(ascending=False).head())

print("\n Worst Cohorts (avg retention):")
print(retention.mean(axis=1).sort_values().head())




# SEGMENT BASED RETENTION


segments = ['Consumer', 'Corporate']

print("--- Consumer Segment Distribution Across Cohort Indexes ---")
print(df[df["Segment"] == "Consumer"]["CohortIndex"].value_counts().head(3))

print("\n--- Corporate Segment Distribution Across Cohort Indexes ---")
print(df[df["Segment"] == "Corporate"]["CohortIndex"].value_counts().head(3))



#  ORDER GAP ANALYSIS


# I sorted the dataset chronologically by customer and order date to map the timeline
df = df.sort_values(['Customer ID', 'Order Date'])

# I brought the next order date to the current row for each customer using the shift function
df['Next Order Date'] = df.groupby('Customer ID')['Order Date'].shift(-1)

# I calculated the exact number of days passing between consecutive orders
df['Days Between Orders'] = (df['Next Order Date'] - df['Order Date']).dt.days

# I dropped the NaN values (representing the customer's final order) to avoid skewing the calculations
gap_series = df['Days Between Orders'].dropna()

# I calculated both the mean and median to discover the true purchasing rhythm
avg_gap = gap_series.mean()
median_gap = gap_series.median()

# I printed the final benchmarks to evaluate the customer re-engagement timelines
print(f"Average order gap: {avg_gap:.2f} days")
print(f"Median order gap: {median_gap:.2f} days")



# I grouped the data by customer and date to calculate the number of unique Order IDs per day
same_day_distinct_orders = df.groupby(['Customer ID', 'Order Date']).agg({
    'Order ID': 'nunique'  
}).reset_index()

# I filtered the dataset to isolate only the instances where a customer had more than 1 distinct order on the same day
real_same_day_buyers = same_day_distinct_orders[same_day_distinct_orders['Order ID'] > 1]

# I printed the metrics and the top 10 rows to validate my findings
print(f"I investigated the dataset and found that the number of unique customers who truly placed multiple distinct orders on the exact same day is: {real_same_day_buyers['Customer ID'].nunique()}")
print("\n--- I isolated and listed the top 10 customers experiencing this systemic/behavioral pattern below ---")
print(real_same_day_buyers.sort_values(by='Order ID', ascending=False).head(10))



# Strategic Customer Analytics Action Plan 

# --- 🚨 SECTION 1: EMERGENCY CRISIS INTERVENTIONS (CRITICAL GROUPS) ---
emergency_interventions = {
    "WHALE_CUSTOMERS_ALARM": {
        "TARGET_AUDIENCE": "73 'Whale' Customers (Non-Champions)",
        "STRATEGY": "1-to-1 VIP Recovery / Key Account Management",
        "ACTION": "Halt all automated generic emails/SMS for dormant whales! The sales team must execute manual outbound calls to offer bespoke contract pricing or high-value personalized 'VIP Return Packages'.",
        "WHY": "These top-spending accounts are missing from the 'Champions' segment; those who are inactive have drifted into riskier segments due to lack of personalization."
    },
    "cant_lose_them": {
        "TARGET_AUDIENCE": "Can't Lose Them (39 Customers)",
        "STRATEGY": "Direct Relationship Management & Service Level Guarantees",
        "ACTION": "Focus heavily on their historically preferred categories (Office Supplies/Furniture). Provision dedicated account handling, priority shipping, and high-value custom product bundles.",
        "WHY": "They lead the entire dataset in purchase frequency (9.97 average) but have been completely inactive for over 212 days."
    },
    "at_risk": {
        "TARGET_AUDIENCE": "At Risk (107 Customers)",
        "STRATEGY": "Category-Specific Win-Back Retargeting",
        "ACTION": "Launch dynamic remarketing ads tailored to their last purchased category, paired with a strict 48-hour time-bound 'Last Chance' high-value voucher.",
        "WHY": "They contain 65 crucial revenue-driving accounts that sustain key revenue streams but have been dormant for 224 days."
    },
    "new_customers_cliff": {
        "TARGET_AUDIENCE": "New Customers (Month 2 Retention Cliff)",
        "STRATEGY": "Systemic Retention Optimization (Onboarding Flow)",
        "ACTION": "Deploy an automated onboarding sequence: an experience feedback survey on Day 7, followed by a high-incentive, time-limited secondary purchase trigger on Day 25.",
        "WHY": "Cohort analysis indicates a catastrophic 93.9% drop-out rate in Month 2. The customer acquisition funnel is a leaking bucket."
    }
}

# --- 💰 SECTION 2: GROWTH & MARGIN PRESERVATION STRATEGIES ---
growth_and_margin_tactics = {
    "REVENUE_CORE_445": {
        "TARGET_AUDIENCE": "Core Accounts (445 Customers Driving 80% Revenue)",
        "STRATEGY": "Budget & Resource Consolidation",
        "ACTION": "Ring-fence 70% of the total marketing and retention budget exclusively to engage, protect, or win back these 445 vital accounts.",
        "WHY": "While the distribution is broader than a classic Pareto curve, 445 core accounts completely sustain the business. Any attrition here triggers an immediate financial crisis."
    },
    "loyal_customers": {
        "TARGET_AUDIENCE": "Loyal Customers (148 Customers)",
        "STRATEGY": "Points-Based Loyalty (Gamification) & Up-selling",
        "ACTION": "Cease direct price discounting immediately. Transition them to an earned-points tier system and offer cross-category bundles (e.g., Office Supplies attachment to Furniture purchases).",
        "WHY": "They drive 26.1% of revenue, but their discount dependency is alarmingly high at 54.3%. Brand value must be decoupled from price cuts."
    },
    "champions": {
        "TARGET_AUDIENCE": "Champions (88 Customers)",
        "STRATEGY": "VIP Perks & Zero-Discount Advocacy",
        "ACTION": "Never send markdown discounts. Offer exclusive early access to premium Technology lines, VIP community perks, and experiential loyalty rewards.",
        "WHY": "They have the highest Average Order Value (AOV: 3000) and the freshest recency (15 days). They are highly emotionally invested in the brand."
    },
    "potential_loyalists": {
        "TARGET_AUDIENCE": "Potential Loyalists (111 Customers)",
        "STRATEGY": "Frequency Stimulation & Category Expansion",
        "ACTION": "Trigger automated cross-sell campaigns (e.g., 'Buy 3 Pay for 2' on ancillary product lines) exactly 15 days post-purchase to shorten the buying cycle.",
        "WHY": "They visited within 28 days and have low discount sensitivity (51.8%), making them prime candidates for upward segment migration."
    },
    "need_attention": {
        "TARGET_AUDIENCE": "Need Attention (32 Customers)",
        "STRATEGY": "Early-Warning Feedback & Re-engagement",
        "ACTION": "Send a lightweight, high-empathy 'How can we improve?' survey, rewarding participants with a fixed-value credit towards their next order.",
        "WHY": "Dormant for 81 days, they sit on a dangerous precipice. Without proactive touchpoints, they will rapidly decay into 'At Risk'."
    }
}

# --- 🥶 SECTION 3: COST ALLOCATION & PASSIVE OPTIMIZATION ---
passive_and_saving_tactics = {
    "DISCOUNT_HUNTERS_371": {
        "TARGET_AUDIENCE": "100% Discount Dependent (371 Customers)",
        "STRATEGY": "Dead-Stock Liquidation & Margin Defense",
        "ACTION": "Exclude them from high-margin new arrivals. Utilize this list exclusively via zero-cost channels to liquidate dead stock or clear warehouse inventory.",
        "WHY": "They have never bought a single product at full retail price. Funneling standard ad-spend towards them actively kills net margins."
    },
    "about_to_sleep": {
        "TARGET_AUDIENCE": "About to Sleep (58 Customers)",
        "STRATEGY": "Low-Cost Price-Driven Triggers",
        "ACTION": "Include them only in generic, automated bulk newsletters featuring high-velocity clearance stock or mass markdown seasonal events.",
        "WHY": "Inactive for 75 days with historically low baseline engagement. They are highly transactional and react only to heavy price slashes."
    },
    "promising": {
        "TARGET_AUDIENCE": "Promising (18 Customers)",
        "STRATEGY": "Brand Storytelling & Nurturing",
        "ACTION": "Deliver content-rich educational emails about product use-cases, backed by a micro-incentive to encourage a second transaction.",
        "WHY": "Fresh organic traffic that needs structured nurturing before falling into the Month 2 churn trap."
    },
    "hibernating": {
        "TARGET_AUDIENCE": "Hibernating (171 Customers)",
        "STRATEGY": "Zero Ad-Spend / Passive Automation",
        "ACTION": "Exclude entirely from paid remarketing audiences (Meta/Google Ads). Retain solely in low-priority, zero-cost quarterly email lists.",
        "WHY": "Absent for over a year with negligible past engagement. Re-acquisition marketing costs (CAC) will yield negative ROI."
    }
}

# --- TERMINAL PRINT ENGINE ---
def print_section(title, data, color_code="37"):
    print(f"\n\033[{color_code}m" + "="*40 + f" {title} " + "="*40 + "\033[0m")
    for key, val in data.items():
        print(f"\n📌 [\033[1m{key.upper()}\033[0m] -> {val['TARGET_AUDIENCE']}")
        print(f"   🎯 Strategy : {val['STRATEGY']}")
        print(f"   🚀 Action   : {val['ACTION']}")
        print(f"   💡 Why      : {val['WHY']}")

# Execution
print_section("🚨🚨🚨 EMERGENCY CRISIS INTERVENTIONS 🚨🚨🚨", emergency_interventions, "31") # Red
print_section("💰💰 GROWTH & MARGIN PRESERVATION 💰💰", growth_and_margin_tactics, "32")  # Green
print_section("🥶 LOW-COST / PASSIVE AUDIENCE MANAGEMENT 🥶", passive_and_saving_tactics, "34")   # Blue
print("\n" + "="*112)







