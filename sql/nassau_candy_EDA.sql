-- ======================================================================================================
-- Factory-to-Customer Shipping Route Efficiency Analysis
-- Company : Nassau Candy Distributor
-- Objective:
-- Analyze shipping routes (Factory → Customer State/Region) to identify fastest and slowest performing
-- routes, geographic bottlenecks, ship mode performance, and factory-level volume/efficiency trends,
-- in order to support data-driven improvements to distribution efficiency.
-- Phase: 3 (SQL Exploratory Data Analysis)
-- Author: Kehkasha Ansari
-- Tools: MySQL, Python, Streamlit
-- Note: Shipping Lead Time reflects a known data generation anomaly in Order Date/Ship Date (see Data Validation section).
-- Lead Time is used for relative ranking and route comparison only, not as a literal real-world day count.    
-- ======================================================================================================

-- Setup: create the working database and confirm the table Created & loaded correctly
create database if not exists nassau_candy;
Use nassau_candy;

create table nassau_candy_cleaned (
`Row ID` INT,
    `Order ID` VARCHAR(50),
    `Order Date` DATE,
    `Ship Date` DATE,
    `Ship Mode` VARCHAR(50),
    `Customer ID` INT,
    `Country/Region` VARCHAR(50),
    `City` VARCHAR(100),
    `State/Province` VARCHAR(50),
    `Postal Code` INT,
    `Division` VARCHAR(50),
    `Region` VARCHAR(50),
    `Product ID` VARCHAR(50),
    `Product Name` VARCHAR(100),
    `Sales` DECIMAL(10,2),
    `Units` INT,
    `Gross Profit` DECIMAL(10,2),
    `Cost` DECIMAL(10,2),
    `Lead Time` INT,
    `Year Gap` INT,
    `Normalized Lead Time` INT,
    `Factory` VARCHAR(50),
    `Route_State` VARCHAR(100),
    `Route_Region` VARCHAR(100)
    );
    SHOW TABLES;
    DESCRIBE nassau_candy_cleaned;
    SELECT count(*) FROM nassau_candy_cleaned;

-- Section 1: Data Validation
-- Query 1: Number of Records 
SELECT count(*) as Total_Records from nassau_candy_cleaned;  

-- Query 2: Number of unique order, unique customer
SELECT 
	COUNT(DISTINCT `Order ID`) AS Unique_Orders,
    COUNT(DISTINCT `Customer ID`) AS Unique_Customers
FROM nassau_candy_cleaned;

-- Query 3: Check date range
SELECT 
	MIN(`Order Date`) AS First_Order_Date,
    MAX(`Order Date`) AS Last_Order_Date,
    MIN(`Ship Date`) AS First_Ship_Date,
    MAX(`Ship Date`) AS Last_Ship_Date
from nassau_candy_cleaned;

-- Query 4: Check null across key columns
SELECT 
    SUM(CASE WHEN `Order Date` IS NULL THEN 1 ELSE 0 END) AS Null_Order_Date,
    SUM(CASE WHEN `Ship Date` IS NULL THEN 1 ELSE 0 END) AS Null_Ship_Date,
    SUM(CASE WHEN Factory IS NULL THEN 1 ELSE 0 END) AS Null_Factory,
    SUM(CASE WHEN Route_State IS NULL THEN 1 ELSE 0 END) AS Null_Route_State,
    SUM(CASE WHEN `Lead Time` IS NULL THEN 1 ELSE 0 END) AS Null_Lead_Time
FROM nassau_candy_cleaned;

-- Query 5: Check dataset grain
-- One Order ID can contain multiple product-level records.
-- Therefore, order volume will use COUNT(DISTINCT Order ID).
SELECT
    `Order ID`,
    COUNT(*) AS Rows_Per_Order
FROM nassau_candy_cleaned
GROUP BY `Order ID`
ORDER BY Rows_Per_Order DESC
LIMIT 10;

-- Section 2: Overall KPI Summary
-- Query 6: Overall performance
SELECT
    COUNT(DISTINCT `Order ID`) AS Total_Orders,
    SUM(`Units`) AS Total_Units,
    ROUND(SUM(`Sales`), 2) AS Total_Sales,
    ROUND(SUM(`Gross Profit`), 2) AS Total_Gross_Profit,
    ROUND(AVG(`Lead Time`), 2) AS Avg_Lead_Time,
    ROUND(STDDEV_SAMP(`Lead Time`), 2) AS Lead_Time_Variability
FROM nassau_candy_cleaned; 

-- Section 3: Shipping & Route Performance
-- Query 7: State-level route performance
SELECT
    `Route_State`,
    COUNT(DISTINCT `Order ID`) AS Route_Volume,
    ROUND(AVG(`Lead Time`), 2) AS Avg_Lead_Time,
    ROUND(STDDEV_SAMP(`Lead Time`), 2) AS Lead_Time_Variability
FROM nassau_candy_cleaned
GROUP BY `Route_State`
ORDER BY Avg_Lead_Time ASC;

-- Query 8: Region-Level Route Performance
SELECT
    `Route_Region`,
    COUNT(DISTINCT `Order ID`) AS Route_Volume,
    ROUND(AVG(`Lead Time`), 2) AS Avg_Lead_Time,
    ROUND(STDDEV_SAMP(`Lead Time`), 2) AS Lead_Time_Variability
FROM nassau_candy_cleaned
GROUP BY `Route_Region`
ORDER BY Avg_Lead_Time ASC;

-- Query 9: Factory Performance
SELECT
    `Factory`,
    COUNT(DISTINCT `Order ID`) AS Total_Orders,
    SUM(`Units`) AS Total_Units,
    ROUND(SUM(`Sales`), 2) AS Total_Sales,
    ROUND(SUM(`Gross Profit`), 2) AS Total_Gross_Profit,
    ROUND(AVG(`Lead Time`), 2) AS Avg_Lead_Time,
    ROUND(STDDEV_SAMP(`Lead Time`), 2) AS Lead_Time_Variability
FROM nassau_candy_cleaned
GROUP BY `Factory`
ORDER BY Total_Orders DESC;

-- Query 10: Top 10 Most Efficient State-Level Routes
SELECT
    `Route_State`,
    COUNT(DISTINCT `Order ID`) AS Route_Volume,
    ROUND(AVG(`Lead Time`), 2) AS Avg_Lead_Time,
    ROUND(STDDEV_SAMP(`Lead Time`), 2) AS Lead_Time_Variability
FROM nassau_candy_cleaned
GROUP BY `Route_State`
HAVING COUNT(DISTINCT `Order ID`) >= 10
ORDER BY Avg_Lead_Time ASC,
         Lead_Time_Variability ASC
LIMIT 10;

-- Query 11: Bottom 10 Least Efficient State-Level Routes
SELECT
    `Route_State`,
    COUNT(DISTINCT `Order ID`) AS Route_Volume,
    ROUND(AVG(`Lead Time`), 2) AS Avg_Lead_Time,
    ROUND(STDDEV_SAMP(`Lead Time`), 2) AS Lead_Time_Variability
FROM nassau_candy_cleaned
GROUP BY `Route_State`
HAVING COUNT(DISTINCT `Order ID`) >= 10
ORDER BY Avg_Lead_Time DESC,
         Lead_Time_Variability DESC
LIMIT 10;

-- Query 12: Regional Bottleneck Analysis
SELECT
    `Region`,
    COUNT(DISTINCT `Order ID`) AS Total_Orders,
    SUM(`Units`) AS Total_Units,
    ROUND(SUM(`Sales`), 2) AS Total_Sales,
    ROUND(AVG(`Lead Time`), 2) AS Avg_Lead_Time,
    ROUND(STDDEV_SAMP(`Lead Time`), 2) AS Lead_Time_Variability
FROM nassau_candy_cleaned
GROUP BY `Region`
ORDER BY Total_Orders DESC;

-- Query 13: State-Level Shipment Volume
SELECT
    `State/Province`,
    `Region`,
    COUNT(DISTINCT `Order ID`) AS Total_Orders,
    SUM(`Units`) AS Total_Units,
    ROUND(SUM(`Sales`), 2) AS Total_Sales
FROM nassau_candy_cleaned
GROUP BY
    `State/Province`,
    `Region`
ORDER BY Total_Orders DESC
LIMIT 10;

-- Query 14: Ship Mode Performance
SELECT
    `Ship Mode`,
    COUNT(DISTINCT `Order ID`) AS Total_Orders,
    SUM(`Units`) AS Total_Units,
    ROUND(SUM(`Sales`), 2) AS Total_Sales,
    ROUND(AVG(`Lead Time`), 2) AS Avg_Lead_Time,
    ROUND(STDDEV_SAMP(`Lead Time`), 2) AS Lead_Time_Variability
FROM nassau_candy_cleaned
GROUP BY `Ship Mode`
ORDER BY Avg_Lead_Time ASC;

-- Section 4: Commercial Analysis
-- Query 15: Factory Profitability Analysis
SELECT
    `Factory`,
    COUNT(DISTINCT `Order ID`) AS Total_Orders,
    SUM(`Units`) AS Total_Units,
    ROUND(SUM(`Sales`), 2) AS Total_Sales,
    ROUND(SUM(`Gross Profit`), 2) AS Total_Gross_Profit,
    ROUND(
        SUM(`Gross Profit`) / NULLIF(SUM(`Sales`), 0) * 100,
        2
    ) AS Gross_Profit_Margin
FROM nassau_candy_cleaned
GROUP BY `Factory`
ORDER BY Gross_Profit_Margin DESC;

-- Query 16: Product Performance
SELECT
    `Product Name`,
    `Factory`,
    SUM(`Units`) AS Total_Units,
    ROUND(SUM(`Sales`), 2) AS Total_Sales,
    ROUND(SUM(`Gross Profit`), 2) AS Total_Gross_Profit,
    ROUND(
        SUM(`Gross Profit`) / NULLIF(SUM(`Sales`), 0) * 100,
        2
    ) AS Gross_Profit_Margin
FROM nassau_candy_cleaned
GROUP BY
    `Product Name`,
    `Factory`
ORDER BY Total_Sales DESC;

-- Query 17: Original Division Performance
-- Note: Uses raw Division field before product-level correction.
-- Superseded by Query 21 after correcting Fizzy Lifting Drinks.
SELECT
    `Division`,
    COUNT(DISTINCT `Order ID`) AS Total_Orders,
    SUM(`Units`) AS Total_Units,
    ROUND(SUM(`Sales`), 2) AS Total_Sales,
    ROUND(SUM(`Gross Profit`), 2) AS Total_Gross_Profit,
    ROUND(
        SUM(`Gross Profit`) / NULLIF(SUM(`Sales`), 0) * 100,
        2
    ) AS Gross_Profit_Margin
FROM nassau_candy_cleaned
GROUP BY `Division`
ORDER BY Total_Sales DESC;

-- Query 18: Add Corrected Division column
ALTER TABLE nassau_candy_cleaned
ADD COLUMN `Corrected_Division` VARCHAR(50);

-- Query 19: Populate Corrected Division
SET SQL_SAFE_UPDATES = 0;

UPDATE nassau_candy_cleaned
SET `Corrected_Division` =
    CASE
        WHEN `Product Name` = 'Fizzy Lifting Drinks' THEN 'Other'
        ELSE `Division`
    END
WHERE `Row ID` IS NOT NULL;

SET SQL_SAFE_UPDATES = 1;

-- Query 20: Verify "Fizzy Lifting Drinks" correction
SELECT `Product Name`, `Division`, `Corrected_Division`, COUNT(*) AS Records
FROM nassau_candy_cleaned
WHERE `Product Name` = 'Fizzy Lifting Drinks'
GROUP BY `Product Name`, `Division`, `Corrected_Division`;

-- Query 21: Corrected Division Performance Analysis
SELECT
    `Corrected_Division`,
    COUNT(*) AS Records,
    COUNT(DISTINCT `Order ID`) AS Total_Orders,
    SUM(`Units`) AS Total_Units,
    ROUND(SUM(`Sales`), 2) AS Total_Sales,
    ROUND(SUM(`Gross Profit`), 2) AS Total_Gross_Profit
FROM nassau_candy_cleaned
GROUP BY `Corrected_Division`
ORDER BY Total_Sales DESC;

-- Section 5: Delay & Route Efficiency Analysis
-- Query 22: Lead Time Distribution
SELECT
    `Lead Time`,
    COUNT(*) AS Shipment_Records
FROM nassau_candy_cleaned
GROUP BY `Lead Time`
ORDER BY `Lead Time`;

-- Query 23: Lead Time Cluster Analysis
SELECT
    CASE
        WHEN `Lead Time` BETWEEN 904 AND 912 THEN 'Cluster 1'
        WHEN `Lead Time` BETWEEN 1269 AND 1277 THEN 'Cluster 2'
        WHEN `Lead Time` BETWEEN 1634 AND 1642 THEN 'Cluster 3'
        ELSE 'Other'
    END AS Lead_Time_Cluster,
    COUNT(*) AS Shipment_Records,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM nassau_candy_cleaned), 2) AS Percentage
FROM nassau_candy_cleaned
GROUP BY Lead_Time_Cluster
ORDER BY Lead_Time_Cluster;

-- Query 24: Delay Frequency by Route (State-level)
-- Delay Threshold: Lead Time >= 1634
-- Delay frequency is calculated at the distinct Order ID level.
SELECT
    `Route_State`,
    COUNT(DISTINCT `Order ID`) AS Route_Volume,
    COUNT(DISTINCT CASE
        WHEN `Lead Time` >= 1634 THEN `Order ID`
    END) AS Delayed_Orders,
    ROUND(
        COUNT(DISTINCT CASE
            WHEN `Lead Time` >= 1634 THEN `Order ID`
        END) * 100.0
        / COUNT(DISTINCT `Order ID`),2)
     AS Delay_Frequency_Pct
FROM nassau_candy_cleaned
GROUP BY `Route_State`
HAVING COUNT(DISTINCT `Order ID`) >= 10
ORDER BY Delay_Frequency_Pct DESC;

-- Query 24b: Overall Delay Frequency (dataset-wide)
SELECT
    COUNT(DISTINCT `Order ID`) AS Total_Orders,
    COUNT(DISTINCT CASE
        WHEN `Lead Time` >= 1634 THEN `Order ID`
    END) AS Delayed_Orders,
    ROUND(
        COUNT(DISTINCT CASE
            WHEN `Lead Time` >= 1634 THEN `Order ID`
        END) * 100.0
        / COUNT(DISTINCT `Order ID`),
        2
    ) AS Overall_Delay_Frequency_Pct
FROM nassau_candy_cleaned;

-- Query 25: Route Efficiency Score (0-100, higher = more efficient)
-- Normalized purely on average Lead Time across qualifying routes (volume >= 10).
-- Score of 100 = fastest average route; 0 = slowest average route.
SELECT
    `Route_State`,
    Route_Volume,
    Avg_Lead_Time,
    ROUND(
        100 * (MAX(Avg_Lead_Time) OVER () - Avg_Lead_Time)
        / (MAX(Avg_Lead_Time) OVER () - MIN(Avg_Lead_Time) OVER ()), 2
    ) AS Efficiency_Score
FROM (
    SELECT
        `Route_State`,
        COUNT(DISTINCT `Order ID`) AS Route_Volume,
        AVG(`Lead Time`) AS Avg_Lead_Time
    FROM nassau_candy_cleaned
    GROUP BY `Route_State`
    HAVING COUNT(DISTINCT `Order ID`) >= 10
) AS route_stats
ORDER BY Efficiency_Score DESC;

-- Query 26: High-Volume + Poor-Performance Routes
-- Flags routes with above-average shipment volume AND below-average Efficiency Score
-- among routes with at least 10 orders. Surfaces routes that matter most operationally
-- (frequent, real routes) rather than low-volume statistical outliers.
WITH route_stats AS (
    SELECT
        `Route_State`,
        COUNT(DISTINCT `Order ID`) AS Route_Volume,
        AVG(`Lead Time`) AS Avg_Lead_Time
    FROM nassau_candy_cleaned
    GROUP BY `Route_State`
    HAVING COUNT(DISTINCT `Order ID`) >= 10
),
scored AS (
    SELECT
        `Route_State`,
        Route_Volume,
        ROUND(Avg_Lead_Time, 2) AS Avg_Lead_Time,
        ROUND(
            100 * (MAX(Avg_Lead_Time) OVER () - Avg_Lead_Time)
            / (MAX(Avg_Lead_Time) OVER () - MIN(Avg_Lead_Time) OVER ()), 2
        ) AS Efficiency_Score,
        AVG(Route_Volume) OVER () AS Avg_Volume_Across_Routes,
        AVG(Avg_Lead_Time) OVER () AS Avg_LeadTime_Across_Routes
    FROM route_stats
)
SELECT
    `Route_State`,
    Route_Volume,
    Avg_Lead_Time,
    Efficiency_Score
FROM scored
WHERE Route_Volume > Avg_Volume_Across_Routes
  AND Avg_Lead_Time > Avg_LeadTime_Across_Routes
ORDER BY Route_Volume DESC, Efficiency_Score ASC;

-- Query 27: Ship Mode Cost-Time Trade-off
SELECT
    `Ship Mode`,
    COUNT(DISTINCT `Order ID`) AS Total_Orders,
    ROUND(SUM(`Cost`), 2) AS Total_Cost,
    ROUND(AVG(`Cost`), 2) AS Avg_Cost_Per_Shipment,
    ROUND(AVG(`Lead Time`), 2) AS Avg_Lead_Time,
    ROUND(STDDEV_SAMP(`Lead Time`), 2) AS Lead_Time_Variability,
    ROUND(SUM(`Gross Profit`), 2) AS Total_Gross_Profit
FROM nassau_candy_cleaned
GROUP BY `Ship Mode`
ORDER BY Avg_Lead_Time ASC;