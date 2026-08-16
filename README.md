# 📊 Customer Churn Analysis & Prediction

## 📌 Project Overview

Customer retention is an important factor in maintaining sustainable business growth. This project focuses on analyzing customer churn to understand **who is leaving, why they are leaving, and which customer characteristics are associated with churn**.

The project implements an end-to-end analytics workflow using **SQL Server, Power BI, Excel, and Machine Learning**. Customer data is first loaded and prepared in SQL Server, transformed into analysis-ready datasets, and then visualized through an interactive Power BI dashboard. A **Random Forest classification model** is also used to support customer churn prediction.

The overall workflow is:

**Raw Customer Data → SQL Server ETL → Data Transformation → Power BI Dashboard → Churn Analysis → Machine Learning Prediction**

---

## 🎯 Project Objectives

The primary objectives of this project are:

* Build an end-to-end **ETL pipeline using SQL Server**.
* Clean and transform raw customer information into an analysis-ready dataset.
* Analyze customers across multiple dimensions:

  * Demographics
  * Geography
  * Account information
  * Payment methods
  * Services used
* Identify common characteristics and behavioral patterns among churned customers.
* Analyze the major reasons and categories associated with customer churn.
* Develop an interactive **Power BI dashboard** for business-level analysis.
* Calculate important customer and churn KPIs.
* Prepare customer data for machine learning.
* Use a **Random Forest model** to predict potential customer churn.
* Generate insights that can support targeted customer-retention strategies.

---

# 🛠️ Technology Stack

| Technology                    | Purpose                                                                 |
| ----------------------------- | ----------------------------------------------------------------------- |
| **SQL Server**                | Database creation, ETL, cleaning, transformation, and data preparation  |
| **Power BI**                  | Data transformation, measures, dashboard development, and visualization |
| **Excel**                     | Preparing datasets for machine-learning analysis                        |
| **Python / Machine Learning** | Customer churn prediction                                               |
| **Random Forest**             | Churn classification                                                    |
| **GitHub**                    | Project documentation and version control                               |

---

# 🔄 Project Workflow

```text
                    ┌──────────────────────┐
                    │   Raw Customer Data  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     SQL Server       │
                    │   Staging / ETL      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Data Cleaning &       │
                    │ Transformation        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Production Dataset   │
                    │    prod_Churn         │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴───────────┐
                    ▼                      ▼
          ┌─────────────────┐    ┌──────────────────┐
          │    Power BI     │    │ Machine Learning │
          │    Dashboard    │    │  Random Forest   │
          └────────┬────────┘    └─────────┬────────┘
                   │                       │
                   ▼                       ▼
          ┌─────────────────┐    ┌──────────────────┐
          │ Churn Insights  │    │ Churn Prediction │
          └─────────────────┘    └──────────────────┘
```

---

# 🗄️ Step 1 — ETL Process in SQL Server

## 1.1 Create the Database

Create a dedicated database for the churn analysis project:

```sql
CREATE DATABASE db_Churn;
```

After connecting to SQL Server, use the newly created `db_Churn` database for the remaining ETL operations.

---

## 1.2 Import the CSV Dataset

The raw customer dataset is imported into SQL Server using the **Import Flat File Wizard**.

### Import procedure

1. Open SQL Server Management Studio.
2. Connect to the required SQL Server instance.
3. Select the `db_Churn` database.
4. Open:

```text
Tasks → Import Flat File
```

5. Select the customer CSV file.
6. Configure the column data types.
7. Set `Customer_ID` as the primary key.
8. Allow nullable values where required.

> **Note:** During the original import process, Boolean/BIT fields caused import issues. These fields can therefore be initially imported as `VARCHAR(50)` and converted later during the transformation stage.

---

# 🔍 1.3 Data Exploration

Before transforming the data, the dataset should be inspected to understand its structure and identify possible data-quality issues.

The analysis includes:

* Gender distribution
* Contract distribution
* Customer status and revenue
* Geographic distribution
* Distinct values
* Missing-value analysis

---

## 1.4 Check for Missing Values

The following query checks the dataset for NULL values across important customer attributes:

```sql
SELECT 
    SUM(CASE WHEN Customer_ID IS NULL THEN 1 ELSE 0 END) AS Customer_ID_Null_Count,
    SUM(CASE WHEN Gender IS NULL THEN 1 ELSE 0 END) AS Gender_Null_Count,
    SUM(CASE WHEN Age IS NULL THEN 1 ELSE 0 END) AS Age_Null_Count,
    SUM(CASE WHEN Married IS NULL THEN 1 ELSE 0 END) AS Married_Null_Count,
    SUM(CASE WHEN City IS NULL THEN 1 ELSE 0 END) AS City_Null_Count,
    SUM(CASE WHEN Number_of_Referrals IS NULL THEN 1 ELSE 0 END) AS Number_of_Referrals_Null_Count,
    SUM(CASE WHEN Tenure_in_Months IS NULL THEN 1 ELSE 0 END) AS Tenure_in_Months_Null_Count,
    SUM(CASE WHEN Phone_Service IS NULL THEN 1 ELSE 0 END) AS Phone_Service_Null_Count,
    SUM(CASE WHEN Multiple_Lines IS NULL THEN 1 ELSE 0 END) AS Multiple_Lines_Null_Count,
    SUM(CASE WHEN Internet_Service IS NULL THEN 1 ELSE 0 END) AS Internet_Service_Null_Count,
    SUM(CASE WHEN Internet_Type IS NULL THEN 1 ELSE 0 END) AS Internet_Type_Null_Count,
    SUM(CASE WHEN Online_Security IS NULL THEN 1 ELSE 0 END) AS Online_Security_Null_Count,
    SUM(CASE WHEN Online_Backup IS NULL THEN 1 ELSE 0 END) AS Online_Backup_Null_Count,
    SUM(CASE WHEN Device_Protection_Plan IS NULL THEN 1 ELSE 0 END) AS Device_Protection_Plan_Null_Count,
    SUM(CASE WHEN Premium_Tech_Support IS NULL THEN 1 ELSE 0 END) AS Premium_Support_Null_Count,
    SUM(CASE WHEN Streaming_TV IS NULL THEN 1 ELSE 0 END) AS Streaming_TV_Null_Count,
    SUM(CASE WHEN Streaming_Movies IS NULL THEN 1 ELSE 0 END) AS Streaming_Movies_Null_Count,
    SUM(CASE WHEN Streaming_Music IS NULL THEN 1 ELSE 0 END) AS Streaming_Music_Null_Count,
    SUM(CASE WHEN Unlimited_Data IS NULL THEN 1 ELSE 0 END) AS Unlimited_Data_Null_Count,
    SUM(CASE WHEN Contract IS NULL THEN 1 ELSE 0 END) AS Contract_Null_Count,
    SUM(CASE WHEN Paperless_Billing IS NULL THEN 1 ELSE 0 END) AS Paperless_Billing_Null_Count,
    SUM(CASE WHEN Payment_Method IS NULL THEN 1 ELSE 0 END) AS Payment_Method_Null_Count,
    SUM(CASE WHEN Monthly_Charge IS NULL THEN 1 ELSE 0 END) AS Monthly_Charge_Null_Count,
    SUM(CASE WHEN Total_Charges IS NULL THEN 1 ELSE 0 END) AS Total_Charges_Null_Count,
    SUM(CASE WHEN Total_Refunds IS NULL THEN 1 ELSE 0 END) AS Total_Refunds_Null_Count,
    SUM(CASE WHEN Total_Extra_Data_Charges IS NULL THEN 1 ELSE 0 END) AS Total_Extra_Data_Charges_Null_Count,
    SUM(CASE WHEN Total_Long_Distance_Charges IS NULL THEN 1 ELSE 0 END) AS Total_Long_Distance_Charges_Null_Count,
    SUM(CASE WHEN Total_Revenue IS NULL THEN 1 ELSE 0 END) AS Total_Revenue_Null_Count,
    SUM(CASE WHEN Customer_Status IS NULL THEN 1 ELSE 0 END) AS Customer_Status_Null_Count,
    SUM(CASE WHEN Churn_Category IS NULL THEN 1 ELSE 0 END) AS Churn_Category_Null_Count,
    SUM(CASE WHEN Churn_Reason IS NULL THEN 1 ELSE 0 END) AS Churn_Reason_Null_Count
FROM stg_Churn;
```

---

# 🧹 1.5 Clean and Load the Production Table

After identifying missing values, the cleaned dataset is loaded into a production-ready table.

Default values are assigned to selected categorical fields where information is unavailable.

```sql
SELECT 
    Customer_ID,
    Gender,
    Age,
    Married,
    City,
    Number_of_Referrals,
    Tenure_in_Months,
    Phone_Service,
    ISNULL(Multiple_Lines, 'No') AS Multiple_Lines,
    Internet_Service,
    ISNULL(Internet_Type, 'None') AS Internet_Type,
    ISNULL(Online_Security, 'No') AS Online_Security,
    ISNULL(Online_Backup, 'No') AS Online_Backup,
    ISNULL(Device_Protection_Plan, 'No') AS Device_Protection_Plan,
    ISNULL(Premium_Tech_Support, 'No') AS Premium_Support,
    ISNULL(Streaming_TV, 'No') AS Streaming_TV,
    ISNULL(Streaming_Movies, 'No') AS Streaming_Movies,
    ISNULL(Streaming_Music, 'No') AS Streaming_Music,
    ISNULL(Unlimited_Data, 'No') AS Unlimited_Data,
    Contract,
    Paperless_Billing,
    Payment_Method,
    Monthly_Charge,
    Total_Charges,
    Total_Refunds,
    Total_Extra_Data_Charges,
    Total_Long_Distance_Charges,
    Total_Revenue,
    Customer_Status,
    ISNULL(Churn_Category, 'Others') AS Churn_Category,
    ISNULL(Churn_Reason, 'Others') AS Churn_Reason
INTO db_Churn.dbo.prod_Churn
FROM db_Churn.dbo.stg_Churn;
```

### Data layers

The ETL process uses two primary layers:

```text
stg_Churn
    ↓
Data Cleaning & Standardization
    ↓
prod_Churn
```

* `stg_Churn` → staging layer containing imported/raw data
* `prod_Churn` → cleaned and analysis-ready dataset

---

# 👁️ 1.6 Create SQL Views for Power BI

Two SQL views are created to provide Power BI with purpose-specific datasets.

### Churn Analysis View

```sql
USE db_Churn;
GO

CREATE VIEW vw_ChurnData AS
SELECT *
FROM dbo.prod_Churn
WHERE Customer_Status IN ('Churned', 'Stayed');
GO
```

### New Customer View

```sql
CREATE VIEW vw_JoinData AS
SELECT *
FROM dbo.prod_Churn
WHERE Customer_Status = 'Joined';
GO
```

These views separate existing customer outcomes from newly joined customers and simplify downstream Power BI analysis.

---

# 📊 Step 2 — Power BI Data Transformation

After connecting Power BI to SQL Server, additional calculated fields and mapping tables are created.

---

## 2.1 Churn Status

Create a binary indicator for churned customers:

```text
Churn Status =
IF [Customer_Status] = "Churned" THEN 1 ELSE 0
```

Convert the resulting column to a numeric data type.

---

## 2.2 Monthly Charge Categories

Customers are grouped according to their monthly charges:

```text
< 20
20 - 50
50 - 100
> 100
```

This segmentation makes it easier to compare churn behavior across different pricing levels.

---

# 👥 2.3 Age Group Mapping

Create a reference table containing unique age values and classify customers into four age segments:

| Age      | Group     |
| -------- | --------- |
| Below 20 | `< 20`    |
| 20–35    | `20 - 35` |
| 36–50    | `36 - 50` |
| Above 50 | `> 50`    |

Create a numerical sorting column:

```text
< 20       → 1
20 - 35    → 2
36 - 50    → 3
> 50       → 4
```

This prevents Power BI from displaying the groups in an unintended alphabetical order.

---

# ⏳ 2.4 Tenure Group Mapping

Customers are also segmented according to their tenure:

| Tenure         | Group          |
| -------------- | -------------- |
| Below 6 months | `< 6 Months`   |
| 6–12 months    | `6-12 Months`  |
| 12–18 months   | `12-18 Months` |
| 18–24 months   | `18-24 Months` |
| 24+ months     | `>= 24 Months` |

A numerical sorting column is created to maintain the correct chronological order.

---

# 📡 2.5 Service-Level Transformation

Create a reference table for service analysis.

The service columns are **unpivoted** so that multiple service attributes can be analyzed through a common structure.

Rename the generated fields:

```text
Attribute → Services
Value     → Status
```

This structure makes it easier to compare service adoption and churn across different offerings.

---

# 🧮 Step 3 — Power BI Measures

The dashboard uses the following core measures.

### Total Customers

```DAX
Total Customers =
COUNT(prod_Churn[Customer_ID])
```

### New Joiners

```DAX
New Joiners =
CALCULATE(
    COUNT(prod_Churn[Customer_ID]),
    prod_Churn[Customer_Status] = "Joined"
)
```

### Total Churn

```DAX
Total Churn =
SUM(prod_Churn[Churn Status])
```

### Churn Rate

```DAX
Churn Rate =
DIVIDE(
    [Total Churn],
    [Total Customers]
)
```

Using `DIVIDE()` helps prevent errors when the denominator is zero.

---

# 📈 Step 4 — Power BI Dashboard

The Power BI report is organized into an interactive summary dashboard and a churn-reason tooltip page.

## 📌 Summary Page

### 1. KPI Cards

The dashboard displays:

* **Total Customers**
* **New Joiners**
* **Total Churn**
* **Churn Rate %**

### 2. Demographic Analysis

Customer churn is analyzed using:

* Gender-wise churn rate
* Age group-wise customer count
* Age group-wise churn rate

### 3. Account Analysis

The dashboard evaluates:

* Payment method vs. churn rate
* Contract type vs. churn rate
* Tenure group vs. customer count and churn rate

### 4. Geographic Analysis

The dashboard highlights the:

* Top 5 states by churn rate

### 5. Churn Distribution

Churn is examined by:

* Churn category
* Churn reason

The churn-reason information is also used as a tooltip to provide additional context without overcrowding the main dashboard.

### 6. Service Analysis

The dashboard compares:

* Internet type vs. churn rate
* Individual services vs. churn status

---

# 🔎 Churn Reason Tooltip Page

A dedicated tooltip page provides additional detail for churn analysis.

### Included visualization

* Churn Reason vs. Total Churn

This allows users to hover over relevant dashboard elements and investigate the underlying reasons for customer attrition.

---

# 🤖 Step 5 — Customer Churn Prediction

The project extends descriptive analytics into predictive analytics using a **Random Forest classification model**.

## What is Random Forest?

Random Forest is an ensemble machine-learning algorithm that combines predictions from multiple decision trees.

For classification problems, individual trees generate class predictions and the forest selects the final class based on the collective vote of the trees.

The approach introduces randomness in both the training samples and selected features, which generally makes the model more robust than relying on a single decision tree.

In this project, Random Forest is used to identify customers who may be at higher risk of churn.

---

# 📥 Data Preparation for Machine Learning

The SQL views are exported to Excel before being used for the prediction workflow.

### Procedure

1. Open Excel.
2. Navigate to:

```text
Data → Get Data → SQL Server Database
```

3. Enter the SQL Server name.
4. Select the `db_Churn` database.
5. Import:

   * `vw_ChurnData`
   * `vw_JoinData`
6. Save the resulting workbook as:

```text
Prediction_Data
```

The resulting dataset can then be prepared for machine-learning training and prediction.

---

# 📌 Data Architecture Summary

| Component        | Role                                            |
| ---------------- | ----------------------------------------------- |
| `db_Churn`       | Database used for the churn analysis project    |
| `stg_Churn`      | Staging table containing imported customer data |
| `prod_Churn`     | Cleaned, production-ready customer dataset      |
| `vw_ChurnData`   | View containing churned and retained customers  |
| `vw_JoinData`    | View containing newly joined customers          |
| `dbo`            | Default SQL Server database schema              |
| `Churn Category` | Broad grouping of churn causes                  |
| `Churn Reason`   | Specific reason associated with customer churn  |

---

# 💡 Business Insights Supported by the Project

This analytical framework can help businesses:

* Monitor overall customer churn.
* Identify customer segments with elevated churn rates.
* Compare churn across demographic groups.
* Evaluate the relationship between contracts and customer retention.
* Analyze churn across payment methods.
* Identify geographic regions with comparatively higher churn.
* Understand the most common churn categories and reasons.
* Examine whether particular services are associated with higher or lower churn.
* Identify customers who may require proactive retention efforts.
* Support targeted marketing and customer-retention campaigns.

---

# 🚀 Key Skills Demonstrated

* **SQL Server**

  * Database creation
  * Data ingestion
  * ETL
  * Data cleaning
  * NULL handling
  * SQL views
  * Data transformation

* **Power BI**

  * Power Query transformations
  * Data modeling
  * Calculated columns
  * DAX measures
  * KPI development
  * Interactive dashboards
  * Tooltip pages
  * Customer segmentation

* **Machine Learning**

  * Classification
  * Feature preparation
  * Random Forest
  * Churn prediction

* **Data Analytics**

  * Customer segmentation
  * Exploratory data analysis
  * Churn analysis
  * Business KPI development
  * Retention-focused insights

---

# 📂 Suggested Repository Structure

```text
customer-churn-analysis/
│
├── README.md
│
├── data/
│   └── customer_data.csv
│
├── sql/
│   ├── database_creation.sql
│   ├── data_cleaning.sql
│   ├── views.sql
│   └── churn_analysis.sql
│
├── powerbi/
│   └── customer_churn_dashboard.pbix
│
├── ml/
│   ├── churn_prediction.ipynb
│   └── prediction_data.xlsx
│
├── images/
│   ├── dashboard.png
│   ├── gender_distribution.png
│   ├── contract_distribution.png
│   └── churn_analysis.png
│
└── LICENSE
```

---

# 🏁 Conclusion

This project demonstrates a complete customer-churn analytics pipeline, starting with raw customer data and progressing through **SQL-based ETL, data transformation, Power BI visualization, and machine-learning-based churn prediction**.

By combining descriptive, diagnostic, and predictive analytics, the project provides a structured approach for understanding customer attrition and identifying opportunities for improved customer retention.

> **Note:** The project documentation has been rewritten in original wording while preserving the technical workflow and project logic contained in the supplied material. The underlying SQL logic, transformations, metrics, and analytical structure remain aligned with the original project.
