-- *EDA*
USE db_churn;
GO
SELECT TABLE_SCHEMA, TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
ORDER BY TABLE_NAME;--Data Exploration –Check Distinct Values--Gender distribution
SELECT Gender, Count(Gender) as TotalCount,
Count(Gender) * 1.0 / (Select Count(*) from stg_Churn)  as Percentage
from stg_Churn
Group by Gender--Contract distribution
SELECT Contract, Count(Contract) as TotalCount,
Count(Contract) * 1.0 / (Select Count(*) from stg_Churn)  as Percentage
from stg_Churn
Group by Contract--Customer status with revenue
SELECT Customer_Status, Count(Customer_Status) as TotalCount, Sum
(Total_Revenue) as TotalRev,
Sum(Total_Revenue) / (Select sum(Total_Revenue) from stg_Churn) * 100  as 
RevPercentage
from stg_Churn
Group by Customer_Status--State distribution
SELECT City, Count(City) as TotalCount,
Count(City) * 1.0 / (Select Count(*) from stg_Churn)  as Percentage
from stg_Churn
Group by City
Order by Percentage desc



-- *Remove Null*
SELECT 
Customer_ID,
Gender,
Age,
Married,
City,
Number_of_Referrals,
Tenure_in_Months,
Phone_Service,
ISNULL(Multiple_Lines, 'No') As Multiple_Lines,
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
ISNULL(Churn_Reason , 'Others') AS Churn_Reason
INTO [db_Churn].[dbo].[prod_Churn]
FROM [db_Churn].[dbo].[stg_Churn];

