# 📈 Customer Analytics & Growth Marketing Project

This project is an end-to-end data analytics study built by programmatically combining **RFM Modeling**, **Cohort Retention**, **Pareto (%80/20) Analysis**, and **Discount Sensitivity** metrics based on a transactional e-commerce dataset containing more than 540,000 rows.

The pipeline spans from structural data cleaning to identifying pipeline leakages and high-value "Whale" accounts dropped by the system, aiming to generate a **strategic roadmap ready for C-suite presentation**.

---

## 🚀 Key Business Findings (Executive Summary)

* **🐋 The Whale Paradox:** The top 73 highest-spending accounts (Whales) were isolated. Shockingly, **0% of them belong to the 'Champions' segment**. Due to a lack of systematic engagement, they have drifted into dormant and at-risk categories.
* **📉 Month 2 Retention Cliff:** Cohort analysis reveals that the most severe drop-off occurs in Month 2, showing a **93.9% customer churn rate**. Particularly, the late 2017 cohorts (September, October, November) exhibit long-term retention locked at a low 2%.
* **🏷️ Systemic Discount Dependency:** Over **54.3% of 'Loyal Customers'—the backbone of the customer base—only buy when discounts are applied**. Across all segments, average discount dependency remains above 50%, with **171 unique accounts identified as 100% Discount Hunters** (never purchasing a single item at full retail price).
* **🎯 Pareto Concentration:** Just **56.1% of active accounts (445 clients) drive exactly 80% of total revenue**. Critically, 94 of these 445 core accounts are currently sitting in highly volatile segments: `At Risk` (65 accounts) and `Can't Lose Them` (29 accounts).

---

## 🛠️ Data Cleaning, Validation & Preprocessing

The dataset consists of **9,994 rows and 21 columns**.

### 1. Programmatic Type Conversion
* **Date Parsing:** Columns containing the word "Date" were automatically transformed into `datetime` objects.
* **Categorical Constraints:** Object columns such as `Segment`, `Region`, and `Category` were cast to the `category` type for memory optimization.
* **Relational Formatting:** Elements like `Postal Code`, which appear numerical but hold no mathematical value, were formatted as strings to prevent structural truncation.

### 2. Logical Data Assertions
* **Chronological Check:** Verified that `Ship Date` >= `Order Date` for 100% of the dataset; zero structural discrepancies were found.
* **Quantity & Revenue Screening:** Scanned for anomalies where $Quantity \le 0$ or $Sales \le 0$ to eliminate corrupt transactional logic.
* **Margin Friction Analysis:** Identified 1,871 loss-making records where $Profit < 0$. These were deliberately retained to accurately preserve the historical footprint of margin strain caused by heavy discounting.

### 3. Outlier Management (Winsorization)
Standard $1.5 \times IQR$ thresholding proved too aggressive, stripping away high-value enterprise purchasing behavior (Whales). A **Factor 3 IQR threshold** was utilized to compute bounds, followed by a two-sided **Winsorization** to stabilize variance without breaking the distribution shape:
* **Before:** Sales Mean: 229.85, Max: 22638.48 | Profit Mean: 28.65
* **After:** Sales Mean: 165.74, Max: 787.92 | Profit Mean: 18.24, Min: -81.17, Max: 112.26

---

## 📊 Customer Segmentation Matrix (RFM)

Customers were ranked based on Recency and Frequency percentiles using `pd.qcut` and `.rank` to assign behavioral scores. Scores were aggregated as strings ($Recency\_Score \times 10 + Frequency\_Score$) to avoid overlapping scoring traps.

| Segment | Recency (Mean Days) | Frequency (Mean Orders) | Monetary (Mean AOV) | Customer Share % | Revenue Share % | Top Category |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| 🏆 **Champions** | 15.26 | 9.05 | 3000.49 | 11.09% | 15.94% | Office Supplies & Technology |
| 💎 **Loyal Customers** | 57.49 | 8.73 | 2927.91 | 18.66% | 26.16% | Office Supplies & Furniture |
| ⭐ **Potential Loyalists**| 28.08 | 5.63 | 1921.98 | 13.99% | 12.88% | Office Supplies & Furniture |
| 🚨 **At Risk** | 224.27 | 6.57 | 2264.71 | 13.49% | 14.63% | Office Supplies & Furniture |
| 💔 **Can't Lose Them** | 212.87 | 9.97 | 2985.43 | 4.91% | 7.03% | Office Supplies & Furniture |
| ⚠️ **Need Attention** | 81.00 | 6.40 | 1976.78 | 4.03% | 3.82% | Office Supplies & Furniture |
| 💤 **About to Sleep** | 75.08 | 4.01 | 1371.39 | 7.31% | 4.80% | Office Supplies & Furniture |
| 🌱 **New Customers** | 15.28 | 3.28 | 952.51 | 2.64% | 1.21% | Office Supplies & Technology |
| ⚡ **Promising** | 40.66 | 3.27 | 965.22 | 2.26% | 1.04% | Office Supplies & Furniture |
| 🥶 **Hibernating** | 378.54 | 3.71 | 1209.27 | 21.56% | 12.48% | Office Supplies & Furniture |

---

## 🏁 Segment-Based Growth Marketing Strategies

### 🚨 Priority 1: Crisis Intervention & Churn Mitigation
* **Non-Champion Whale Accounts (73 Accounts):** Halt all generic, automated push notifications immediately. Account managers must execute manual outbound calls to negotiate custom enterprise-level pricing or distribute high-value, bespoke gift-tier return packages.
* **Can't Lose Them (39 Customers):** This segment leads the entire dataset in transaction frequency (9.97 average) but has been dormant for 212 days. Secure them by offering account-specific priority free shipping, return guarantees, or long-term high-volume pricing agreements on their preferred categories (Office Supplies/Furniture).
* **At Risk (107 Customers):** Holding 65 vital Pareto core customers and driving 14.6% of company revenue, this group requires immediate 48-hour time-bound "Last Chance" product vouchers distributed via custom dynamic retargeting streams based on their last active categories.
* **New Customers (Month 2 Cliff):** To repair the 93.9% systemic sifting defect, construct a post-purchase onboarding email sequence: dispatch an automated experience evaluation survey on Day 7, followed by a time-restricted conditional secondary purchase incentive on Day 25.

### 💰 Priority 2: Margin Preservation & Tier Optimization
* **Pareto Core Pool (445 Customers):** To defend the 445 accounts sustaining the business structure (56.1% customer share generating 80% revenue), isolate and freeze 70% of the retention/marketing budget specifically to support and recover accounts within this group.
* **Loyal Customers (148 Customers):** Driving 26.1% of revenue but holding an alarming 54.3% discount dependency rasyo. Cease raw price-slashing maneuvers immediately. Transition them to a points-accumulation loyalty mechanism (Gamification) while serving cross-category cross-sell attachments (e.g., Office Supplies add-ons paired with Furniture orders).
* **Champions (88 Customers):** Boasting the highest average order value (AOV: 3000), these advocates require zero price reductions. Target them exclusively with experiential loyalty hooks, including priority early access to premium Technology lines and elite community perks.
* **Potential Loyalists (111 Customers):** Visited within 28 days with lower overall discount vulnerability (51.8%). Shorten their purchasing cycle and accelerate upward segment migration by serving automated category expansion offers (e.g., "Buy 3 Pay for 2" on adjacent product categories) exactly 15 days post-purchase.
* **Need Attention (32 Customers):** Dormant for 81 days. Distribute a short feedback and brand perception questionnaire offering a fixed-value store credit upon completion to disrupt their transition down into the "At Risk" category.

### 🥶 Priority 3: Low-Cost Automation & Cost Mitigation
* **Discount Hunters (171 Customers):** Completely price-dependent accounts that have never bought items at full retail price. Exclude them entirely from marketing campaigns targeting high-margin inventory. Treat this group exclusively as an optimization lever to clear out warehouse dead stock during annual liquidation periods.
* **About to Sleep (58 Customers):** Inactive for 75 days with faint historical engagement metrics. Limit outreach to zero-cost, low-priority automated bulk clearance newsletters to test for baseline price responses.
* **Promising (18 Customers):** Highly vulnerable to the Month 2 retention cliff. Warm them up using content-driven educational emails explaining product use cases, anchored with low-tier promotional incentives to lock in their second transaction.
* **Hibernating (171 Customers):** Absent for over a year with minimal past revenue footprints. Suppress them entirely from paid marketing audiences to save capital. Restrict interactions to zero-cost, quarterly automated mail touchpoints.
