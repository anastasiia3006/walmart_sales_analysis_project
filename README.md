# walmart_sales_analysis_project


Business Impact and Strategic Decisions:

   Inventory Planning: By analyzing which products sell best during certain seasons or economic conditions, Walmart can optimize its inventory levels, reducing stockouts and overstocks.
   Pricing Strategies: Understanding the relationship between external factors (like temperature or unemployment) and sales can help Walmart adjust its pricing dynamically to remain competitive.
   Marketing and Promotion: Insights into the popularity of products during holidays or specific seasons help Walmart design more effective advertising campaigns and promotional offers.
   Customer Segmentation: By recognizing how different segments (e.g., regions with higher unemployment) behave, Walmart can tailor its product offerings and marketing efforts to better meet customer needs.


all data base have a the same department of products(Skin Care) and same category (Face Masks)

-----DESCTIPTION-OF-THE-DATABASE----

Store: ------------ The store where the product is sold.
Date: ------------ The purchase date.
Weekly_Sales: ----- Weekly sales.
Holiday_Flag: ----- Holiday flag (indicates whether it's a holiday).
Temperature: ------ The temperature in the region.
Fuel_Price: ------- Fuel price.
CPI: -------------- Customer price index.
Unemployment: ----- Unemployment rate in the region.
PRODUCT_NAME: ----- Product name.
DEPARTMENT: ------- Product department.
CATEGORY: --------- Product category.
SKU: -------------- Product identifier.
SELLER: ----------- Product seller.
BRAND: ------------ Product brand.
PRICE_CURRENT: ---- Current price.
PRICE_RETAIL: ----- Retail price.
REVIEW_COUNT: ----- Number of reviews.
REVIEW_RATING: ---- Review rating.
RunDate: ---------- Data collection date.

Data types of all columns in DATABASE

Data columns (total 19 columns):
 #   Column         Non-Null Count  Dtype         
---  ------         --------------  -----         
 0   Store          1130 non-null   int64         
 1   Date           1130 non-null   datetime64[ns]
 2   Weekly_Sales   1130 non-null   float64       
 3   Holiday_Flag   1130 non-null   int64         
 4   Temperature    1130 non-null   float64       
 5   Fuel_Price     1130 non-null   float64       
 6   CPI            1130 non-null   float64       
 7   Unemployment   1130 non-null   float64       
 8   PRODUCT_NAME   1130 non-null   object        
 9   DEPARTMENT     1130 non-null   object        
 10  CATEGORY       1130 non-null   object        
 11  SKU            1130 non-null   int64         
 12  SELLER         1130 non-null   object        
 13  BRAND          1130 non-null   object        
 14  PRICE_CURRENT  1130 non-null   float64       
 15  PRICE_RETAIL   1130 non-null   float64       
 16  REVIEW_COUNT   1130 non-null   int64         
 17  REVIEW_RATING  1130 non-null   float64       
 18  RunDate        1130 non-null   datetime64[ns]
dtypes: datetime64[ns](2), float64(8), int64(4), object(5)
memory usage: 167.9+ KB


# main.py

    Data Cleaning:
        Missing values in the SELLER and BRAND columns are filled with 'Unknown'.
        The Date column is converted to a datetime format.

    Seasonal Sales Analysis:
        Data is grouped by season (Winter, Spring, Summer, Autumn).
        Median and total sales are calculated for each season, providing an overview of sales trends.

    Holiday Sales Impact:
        The code analyzes the effect of holiday sales by calculating their share in total sales and assessing whether they contribute to overall profit growth.
        A t-test is performed to compare holiday vs non-holiday sales.

    Top and Bottom Selling Products by Season:
        The code identifies the products with the highest and lowest sales in each season.
        These results are saved to CSV files for further analysis.

    Popular Products Analysis:
        The best-selling product is identified based on total sales.
        Products are ranked by their sales, and those above the average are classified as "Popular products".
        A new column is added to the dataset to reflect the product popularity, and the updated data is saved.

    Results Storage:
        Key findings, including seasonal sales data and product popularity, are saved to CSV files for future use and visualization.

Key Questions Addressed:

    What are the trends in sales across different seasons?
    How do holiday sales impact overall profits?
    Which products have the highest and lowest sales in each season?
    Which products are the most popular based on sales volume?


Columns Used and Their Purpose in the Analysis

In this analysis, the following columns are utilized to examine the factors affecting Walmart sales:

    Unemployment: Represents the unemployment rate, used to assess its effect on sales by comparing sales in low and high unemployment groups.
    BRAND: Contains information about the product brands. While not directly used in the statistical tests, it could be leveraged for brand-specific insights and comparisons.
    Weekly_Sales: The main variable for analysis, representing the total sales of products, used in all hypothesis tests to determine the impact of various factors.
    Temperature: The temperature of the region, used to analyze how temperature affects sales by comparing sales in different temperature ranges.

# func.py

created a z-test function for use in statistical calculations


# sales_factor.py

Code Summary: Analysis of Factors Affecting Sales

This code tests how Unemployment, Temperature, and Season influence Weekly Sales using statistical tests.

    Unemployment and Sales: A Z-test compares sales between low and high unemployment groups to see if unemployment affects sales.
    Temperature and Sales: A Z-test checks if temperature influences sales.
    Season and Sales: An ANOVA test evaluates if the season affects sales.
Columns Used in the Analysis:

    Unemployment: Represents the unemployment rate, used to analyze its effect on sales by grouping data into low and high unemployment categories.
    BRAND: The brand of each product, used for brand-specific analysis, though not directly in the tests performed.
    Weekly_Sales: The target variable representing the sales of products, used for hypothesis testing and comparisons.
    Temperature: The regional temperature, used to evaluate its influence on sales.


# visualisation.py

Code Summary: Walmart Sales Analysis Visualizations

This code generates visualizations to analyze Walmart sales data, focusing on total sales by season, popular vs. not popular products by season, and the share of holiday sales.

    Total Sales by Season (Bar Plot):
        Purpose: Displays the total sales for each season, sorted in descending order, to show which season contributes the most to sales.
        Columns Used:
            Season: To group the sales by season.
            Weekly_Sales: Total sales value for each season.

    Popular and Not Popular Products by Season (Stacked Bar Plot):
        Purpose: Compares the products with maximum and minimum sales in each season.
        Columns Used:
            Season: To categorize sales by season.
            Weekly_Sales: To visualize the maximum and minimum sales.
            Product Name: To label the products with the highest and lowest sales in each season.

    Share of Holiday Sales (Pie Chart):
        Purpose: Displays the share of holiday vs. non-holiday sales in a pie chart, showing how much of the total sales come from holiday periods.
        Columns Used:
            Holiday_Flag: To separate holiday sales (1 for holiday, 0 for non-holiday).
            Weekly_Sales: To calculate the total holiday and non-holiday sales.
