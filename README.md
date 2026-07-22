# Introduction to Churn Analysis
In today’s competitive business environment, retaining customers is crucial for long-term success. Churn analysis is a key technique used to understand and reduce this customer attrition. It involves examining customer data to identify patterns and reasons behind customer departures. By using advanced data analytics and machine learning, businesses can predict which customers are at risk of leaving and understand the factors driving their decisions. This knowledge allows companies to take proactive steps to improve customer satisfaction and loyalty.


## 📊 Project Objectives
Create an entire ETL process in a database & a Power BI dashboard to utilize the Customer Data and achieve below goals:

- **Visualize & Analyze Customer Data** at multiple levels:
  - Demographic
  - Geographic
  - Payment & Account Information
  - Services

- **Study Churner Profile** to:
  - Identify behavioral and usage patterns
  - Highlight areas for implementing targeted marketing campaigns

- **Predict Future Churners** by:
  - Applying statistical methods and machine learning models
  - Building actionable insights for retention strategies
 
  - **Metrics Required**

  - Total Customers
  - Total Churn & Churn Rate
  - New Joiners
 
  - **STEP 1 – ETL Process in SQL Server**
  - Creating Database

    After installation, you will land on the following screen. Do remember to copy paste the server name somewhere because we will need this at a later stage. Also enable      the checkbox which says “Trust Server Certificate” and then click on Connect

    Once connected, click on NEW QUERY button at the top ribbon and then write below query. This will create a new Database named db_Churn
    CREATE DATABASE db_Churn

    **Import csv into SQL server staging table – Import Wizard**

    Right click on the newly created database in the explorer window and then go to

    **Task >> Import >> Flat file >> Browse CSV file**

    Remember to add customerId as primary key and allow nulls for all remaining columns. This is done to avoid any errors while data load. Also make sure to change the         datatype where it say Bit to Varchar(50). We are doing this because while using import wizard I faced issues with the BIT data type, however Varchar(50) works fine.

    **Data Exploration – Check Distinct Values**
    # Gender distribution
    	Gender	TotalCount	Percentage
   1	Male	   3555	      0.504756496
   2	Female	 3488	      0.495243504
<img width="426" height="88" alt="image" src="https://github.com/user-attachments/assets/f6c7dfbc-6cd2-41d5-9301-040777ad061d" />

    # Contract distribution
    
    
