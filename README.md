# 📈 Customer Analytics Project (RFM, Cohort & Pareto)

An end-to-end data analytics project built on a retail transactional dataset containing exactly **9,994 rows and 21 columns**. This study implements an RFM (Recency, Frequency, Monetary) behavioral segmentation framework and synthesizes it with Cohort Retention analysis, Revenue Concentration analysis, Order Gap timelines, and Calibrated Discount Sensitivity metrics to detect margin leakage and optimize customer management strategies.

---

## 🚀 Key Business Findings (Executive Summary)

* **🐋 The Whale Paradox:** Out of the 73 ultra-high-spending accounts (Whales) isolated based on high monetary value, **0% belong to the 'Champions' segment**. High-value accounts like `AH-10690` (Recency: 412 days) and `AJ-10795` (Recency: 168 days) have slipped into dormant or at-risk segments due to a lack of systematic re-engagement.
* **📉 Month 2 Retention Cliff:** Cohort analysis tracks the historical longevity of customers and highlights that the most severe drop-off occurs in Month 2, showing a **93.9% customer churn rate**. Particularly, late 2017 cohorts (September through November) exhibit long-term retention locked below 2%.
* **🏷️ Systemic Discount Dependency:** Across the entire customer database, average discount dependency remains critically high. Notably, following a calibration of the markdown threshold to **0.7 (70% or higher discount rate)**, exactly **371 unique accounts operate as High-Discount Hunters**, while the critical `Loyal Customers` segment holds a steep dependency rating of **54.3%**.
* **⚡ Transaction-Level Markdown Risk:** Setting the strict mathematical threshold at **0.7** isolated more than 300 aggressive markdown transactions. These transactions are heavily concentrated in low-margin product lines, representing a significant source of structural profit friction.
* **🎯 Revenue Concentration:** Data sorting shows that **445 unique customers drive exactly 80% of total company revenue**. Within this 445-account core group, a high concentration of high-value revenue is highly volatile, including **65 accounts sitting in `At Risk` and 29 accounts sitting in `Can't Lose Them`**.

---

## 🛠️ Data Cleaning, Validation & Preprocessing

The dataset consists of **9,994 rows and 21 columns**.

### 1. Programmatic Type Conversion
* **Date Parsing:** Columns containing the string "Date" were programmatically converted into true `datetime` objects.
* **Categorical Constraints:** Object columns including `Segment`, `Region`, and `Category` were cast to the `category` type for runtime and memory optimization.
* **Relational Formatting:** Elements like `Postal Code` were cast as strings to prevent structural data corruption.

### 2. Logical Data Assertions & Gap Analysis
* **Chronological Check:** Verified that `Ship Date` >= `Order Date` for 100% of the dataset; zero structural discrepancies were found.
* **Quantity & Revenue Screening:** Scanned for anomalies where $Quantity \le 0$ or $Sales \le 0$ to eliminate corrupt transactional logic.
* **Margin Friction Analysis:** Identified 1,871 loss-making records where $Profit < 0$. These were deliberately retained to preserve the historical footprint of margin strain caused by deep discounting.
* **Order Gap Metric:** To baseline the true purchasing rhythm of the user base, consecutive order timelines were calculated by shifting transaction dates via `shift(-1)`. Calculating both the mean and median order gaps served as the mathematical threshold for our re-engagement and onboarding timelines.

### 3. Outlier Management (Winsorization)
Standard $1.5 \times IQR$ thresholding proved too aggressive, stripping away legitimate enterprise-level high-value transactions. A **Factor 3 IQR threshold** was utilized to compute bounds, followed by a two-sided **Winsorization** to stabilize variance without breaking the distribution shape:
* **Before Cleaning:** Sales Mean: 229.85, Max: 22638.48 | Profit Mean: 28.65
* **After Winsorization:** Sales Mean: 165.74, Max: 787.92 | Profit Mean: 18.24, Min: -81.17, Max: 112.26

---

## 📊 Customer Segmentation Matrix (RFM)

Customers were ranked based on Recency and Frequency percentiles using `pd.qcut` and `.rank` to assign behavioral scores from 1 to 5. Scores were combined as strings ($Recency\_Score \times 10 + Frequency\_Score$) to prevent overlapping scoring traps.

| Segment | Recency (Mean Days) | Frequency (Mean Orders) | Monetary (Mean AOV) | Customer Count | Customer Share % | Revenue Share % | Top Category |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| 🏆 **Champions** | 15.26 | 9.05 | 3000.49 | 88 | 11.10% | 15.94% | Office Supplies |
| 💎 **Loyal Customers** | 57.49 | 8.73 | 2927.91 | 148 | 18.66% | 26.16% | Office Supplies |
| ⭐ **Potential Loyalists**| 28.08 | 5.63 | 1921.98 | 111 | 14.00% | 12.88% | Office Supplies |
| 🚨 **At Risk** | 224.27 | 6.57 | 2264.71 | 107 | 13.49% | 14.63% | Office Supplies |
| 💔 **Can't Lose Them** | 212.87 | 9.97 | 2985.43 | 39 | 4.92% | 7.03% | Office Supplies |
| ⚠️ **Need Attention** | 81.00 | 6.40 | 1976.78 | 32 | 4.04% | 3.82% | Office Supplies |
| 💤 **About to Sleep** | 75.08 | 4.01 | 1371.39 | 58 | 7.31% | 4.80% | Office Supplies |
| 🌱 **New Customers** | 15.28 | 3.28 | 952.51 | 21 | 2.65% | 1.21% | Office Supplies |
| ⚡ **Promising** | 40.66 | 3.27 | 965.22 | 18 | 2.27% | 1.05% | Office Supplies |
| 🥶 **Hibernating** | 378.54 | 3.71 | 1209.27 | 171 | 21.56% | 12.48% | Office Supplies |

---

## 🏁 Segment-Based Growth Marketing Strategies

### 🚨 Priority 1: Crisis Intervention & Churn Mitigation
* **Non-Champion Whale Accounts (73 Accounts):** Halt automated, generic communications. Account managers must execute manual outbound calls to negotiate custom enterprise-level pricing or distribute high-value, bespoke return packages.
* **Can't Lose Them (39 Customers):** This segment leads the entire dataset in transaction frequency (9.97 average) but has been dormant for 212 days. Secure them by offering account-specific priority free shipping, return guarantees, or long-term high-volume pricing agreements on their historically preferred categories (Office Supplies/Furniture).
* **At Risk (107 Customers):** Holding 65 vital revenue-driving customers, this group requires immediate 48-hour time-bound "Last Chance" product vouchers distributed via custom dynamic retargeting streams based on their last active categories.
* **New Customers (Month 2 Retention Cliff):** To repair the 93.9% systemic customer drop-out, construct a post-purchase onboarding sequence: dispatch an automated experience evaluation survey on Day 7, followed by a time-restricted conditional secondary purchase incentive on Day 25.

### 💰 Priority 2: Margin Preservation & Tier Optimization
* **Core Revenue Pool (445 Customers):** To defend the 445 accounts sustaining 80% of total company revenue, isolate and allocate 70% of the retention/marketing resources specifically to support and recover accounts within this group (especially the 94 dormant accounts from At Risk and Can't Lose Them).
* **Loyal Customers (148 Customers):** Driving a massive share of revenue but holding a 54.3% discount dependency ratio. Cease raw price-slashing maneuvers immediately. Transition them to a points-accumulation loyalty mechanism while serving cross-category cross-sell attachments (e.g., Office Supplies add-ons paired with Furniture orders).
* **Champions (88 Customers):** Boasting the highest average order value (AOV: 3000), these advocates require zero price reductions. Target them exclusively with experiential loyalty hooks, including priority early access to premium Technology lines and elite community perks.
* **Potential Loyalists (111 Customers):** Visited within 28 days with lower overall discount vulnerability (51.8%). Shorten their purchasing cycle by serving automated category expansion offers (e.g., "Buy 3 Pay for 2" on adjacent product categories) exactly 15 days post-purchase.
* **Need Attention (32 Customers):** Dormant for 81 days. Distribute a short feedback and brand perception questionnaire offering a fixed-value store credit upon completion to disrupt their transition down into the "At Risk" category.

### 🥶 Priority 3: Low-Cost Automation & Cost Mitigation
* **Discount Hunters (371 Customers):** This expanded group of 371 accounts exhibits severe price-dependency, triggered almost exclusively by aggressive markdowns under the calibrated 0.7 filter. Exclude them entirely from marketing campaigns targeting high-margin inventory to protect net margins. Treat this group exclusively as an optimization lever to clear out warehouse dead stock and liquidate inventory via zero-cost automated channels.
* **About to Sleep (58 Customers):** Inactive for 75 days with faint historical engagement metrics. Limit outreach to zero-cost, low-priority automated bulk clearance newsletters to test for baseline price responses.
* **Promising (18 Customers):** Highly vulnerable to the Month 2 retention cliff. Warm them up using content-driven educational emails explaining product use cases, anchored with low-tier promotional incentives to lock in their second transaction.
* **Hibernating (171 Customers):** Absent for over a year with minimal past revenue footprints. Suppress them entirely from paid marketing audiences to save capital. Restrict interactions to zero-cost, quarterly automated mail touchpoints.
