## 📈 Data-Driven Customer Strategy & Retention Analysis Roadmap Project (RFM, Cohort & Pareto)

An end-to-end data analytics and business intelligence project built on a retail transactional dataset containing exactly 9,994 rows and 21 columns. This study implements an RFM (Recency, Frequency, Monetary) behavioral segmentation framework and synthesizes it with Time-Based Cohort Retention analysis, Pareto Revenue Concentration analysis, Order Gap timelines, and Calibrated Discount Sensitivity metrics to detect net profit margin leakage and construct data-driven growth marketing strategies.

## 🚀 Key Business Findings (Executive Summary)
The Whale Paradox: Out of the 73 ultra-high-spending accounts (Whales) isolated based on high monetary value, 0% belong to the 'Champions' segment. High-value accounts like AH-10690 (Recency: 412 days) and AJ-10795 (Recency: 168 days) have slipped into dormant (Hibernating) or At Risk segments due to a lack of systematic, personalized re-engagement workflows.

Month 2 Retention Cliff: Cohort analysis tracking the historical longevity of the user base highlights that the most severe drop-off occurs in Month 2, showing a catastrophic 93.9% customer churn rate. Looking at the entire retention matrix, the April 2014 cohort stands out as the highest quality kpi (14.36% retention), whereas long-term retention quality systematically erodes in late 2017 cohorts (September through November), locking below 2.08%.

Systemic Discount Dependency: Across the entire customer database, average discount dependency remains critically high. When calibrating the mathematical markdown threshold filter to 0.7 (70% or higher discount rate), exactly 371 unique accounts operate as High-Discount Hunters, purchasing exclusively during promotional clearouts. Even the critical Loyal Customers segment holds a steep discount dependency rating of 54.3%.

Revenue Concentration (Pareto Principle): Data sorting and cumulative total metrics show that only 445 unique customers drive exactly 80% of total company revenue. Within this 445-account core engine, revenue stability is highly volatile: 65 vital accounts sit in the At Risk segment, and 29 accounts are trapped in Can't Lose Them.

## 🛠️ Data Cleaning, Validation & Preprocessing
# 1. Programmatic Type Conversion
Date Parsing: Columns containing the string "Date" were programmatically converted into true datetime objects.

Categorical Constraints: Object columns including Segment, Region, and Category were cast to the category type for runtime execution and memory optimization.

Relational Formatting: Structural components like Postal Code were cast as strings to prevent data corruption during downstream numerical transformations.

# 2. Logical Data Assertions & Order Gap Analysis
Chronological Verification: Validated that Ship Date >= Order Date for 100% of the dataset; zero structural discrepancies or data anomalies were found.

Volume & Revenue Screening: Scanned for and eliminated corrupted transactional rows where Quantity <= 0 or Sales <= 0.

Margin Friction Analysis: Identified 1,871 loss-making records where Profit < 0. These were deliberately retained to preserve the historical footprint of net margin strain caused by deep discounting.

Order Gap Operational Pattern: Consecutive purchasing timelines were calculated at the user level using the shift(-1) date method. The analysis revealed an average order gap of 86.16 days, while the median order gap sat at exactly 0.00 days. A median of 0 mathematically proved a heavy concentration of same-day consecutive transactions (order-line row item structures or immediate multi-checkout behaviors). This insight forced the use of Order ID.nunique() instead of raw row counting in the RFM Frequency calculation, preventing artificial profile inflation.

# 3. Outlier Management (Winsorization)
Standard 1.5 * IQR thresholding proved too aggressive for this business model, stripping away legitimate enterprise-level high-value bulk transactions. A Factor 3 IQR threshold was utilized to compute logical data boundaries, followed by a two-sided Winsorization to stabilize variance without breaking the distribution curve:

Before Preprocessing: Sales Mean: 229.85, Max: 22638.48 | Profit Mean: 28.65
After Winsorization: Sales Mean: 165.74, Max: 787.92 | Profit Mean: 18.24 (Min: -81.17, Max: 112.26)

# 📊 Customer Segmentation Matrix (RFM)

Customers were ranked based on Recency and Frequency percentiles using pd.qcut and .rank functions to assign scores from 1 to 5. Scores were combined as strings to prevent overlapping data traps, and segments were structured using the following mathematical breakdown:

Segment  -  Mean - Recency (Days)  -  Mean  - Frequency (Orders)  -  Mean Monetary (AOV)  -  Customer Count  -  Customer Share %  -  Revenue Share %  -  Top Category

🏆 Champions - 15.26 - 9.05 - 3000.49 - 88  -  11.10%  -  15.94% - Office Supplies
💎 Loyal Customers  57.49  - 8.73  -  2927.91  - 148  -  18.66%  -  26.16% - Office Supplies
⭐ Potential Loyalists  28.08  -  5.63  -  1921.98  -  111  -  14.00%  -  12.88% - Office Supplies
🚨 At Risk  224.27  -  6.57  -  2264.71  -  107  - 13.49% - 14.63% - Office Supplies
💔 Can't Lose Them  212.87  -  9.97  -  2985.43  -  39  -  4.92%  -  7.03%  - Office Supplies
⚠️ Need Attention  81.00  -  6.40  -  1976.78  -  32  -  4.04%  -  3.82% - Office Supplies
💤 About to Sleep  75.08  -  4.01  -  1371.39  -  58  -  7.31%  -  4.80% - Office Supplies
🌱 New Customers  15.28  -  3.28 - 952.51 -  21  - 2.65%  -  1.21% - Office Supplies
⚡ Promising  40.66  -  3.27  -  965.22  -  18  -  2.27%  -  1.05% - Office Supplies
🥶 Hibernating  378.54  -  3.71  -  1209.27 - 171  - 	21.56%	- 12.48%	-  Office Supplies


## 🏁 Segment-Based Strategic Action Plan

# 🚨 Priority 1: Crisis Intervention & Churn Mitigation

Non-Champion Whale Accounts (73 Customers): Halt all automated, generic lifecycle communications immediately. Account managers must execute manual outbound calls to negotiate bespoke enterprise-level contract pricing or distribute high-value, personalized VIP return packages.

Can't Lose Them (39 Customers): This segment leads the entire database in transaction frequency (9.97 average) but has drifted into a 212-day dormant state. Lock in these accounts by offering dedicated account handling, priority free shipping, return level guarantees, or bulk-pricing agreements focused on their historically preferred categories (Office Supplies and Furniture).

At Risk (107 Customers): Holding 65 vital revenue-driving Pareto accounts, this group requires immediate 48-hour time-bound "Last Chance" sepet vouchers distributed via custom dynamic remarketing streams matching their last active categories.

New Customers & Month 2 Retention Cliff: To repair the 93.9% systemic customer drop-out, deploy a structured post-purchase onboarding flow: dispatch an automated experience evaluation survey on Day 7, apply a strict frequency capping filter on notifications due to the 0.00-day median order gap anomaly (preventing spam), and trigger a time-restricted conditional secondary purchase incentive on Day 25.

# 💰 Priority 2: Margin Preservation & Tier Optimization

Core Revenue Pool (445 Pareto Customers): To defend the 445 accounts sustaining 80% of total company revenue, ring-fence and allocate 70% of the retention/marketing resources specifically to support and recover accounts within this core layer. Dynamically trigger Corporate accounts during their historical budget renewal cycles on cohort months 8 and 31, while stimulating Consumer accounts with loyalty milestones on cohort months 16 and 26.

Loyal Customers (148 Customers): Driving a massive 26.16% share of revenue, this segment holds an alarmingly high discount dependency of 54.3%. Cease direct, raw price-slashing maneuvers immediately. Transition them to an earned points-accumulation gamified tier system, and cross-sell Office Supplies attachments directly paired with their Furniture orders to expand basket variety.

Champions (88 Customers): Boasting the highest Average Order Value (AOV: 3,000) and an active recency of 15 days, these advocates require zero promotional price reductions. Target them exclusively with experiential loyalty hooks, including priority early access to premium Technology lines and elite customer community perks.

Potential Loyalists (111 Customers): Active within 28 days with lower overall discount vulnerability (51.8%). Shorten their purchasing cycle by launching automated category expansion offers (e.g., "Buy 3, Pay for 2" on adjacent product categories) exactly 15 days post-purchase.

Need Attention (32 Customers): Dormant for 81 days and sitting on a dangerous precipice right above the At Risk threshold. Send a lightweight, high-empathy "How can we improve?" perception survey, rewarding completion with a fixed-value store credit to instantly reactivate their purchasing journey.

# 🥶 Priority 3: Low-Cost Automation & Cost Mitigation

Discount Hunters (371 Customers): Isolated via the 0.7 markdown filter, these 371 unique accounts exhibit extreme price dependency, never buying at standard retail rates. Exclude them entirely from marketing campaigns targeting high-margin inventory to protect net margins. Treat this list exclusively as an optimization lever to liquidate warehouse dead stock or clear seasonal inventory using zero-cost automated email automation.

About to Sleep (58 Customers): Inactive for 75 days with low historical baseline engagement. Limit outreach exclusively to zero-cost, low-priority automated bulk newsletters featuring clearance stock or mass markdown seasonal events.

Promising (18 Customers): Highly vulnerable to the Month 2 retention cliff. Warm them up using content-rich educational emails explaining product use cases, anchored with low-tier conditional promotional incentives to lock in their second transaction.

Hibernating (171 Customers): Absent for over a year with negligible past revenue contributions. Suppress them entirely from paid marketing audiences (Meta/Google Ads) to save marketing capital. Restrict interactions to zero-cost, automated quarterly email touchpoints.
