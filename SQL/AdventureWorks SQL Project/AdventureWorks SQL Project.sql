--Q1: Calc Quantity of items, Sales value & Order quantity by each Subcategory in L12M
SELECT 
  FORMAT_DATETIME('%b %Y', sale_detail.ModifiedDate) as period,
  product_sub.Name,
  SUM(sale_detail.OrderQty) as qty_item,
  SUM(sale_detail.LineTotal) as total_sales,
  COUNT(distinct sale_detail.SalesOrderID) as order_cnt
FROM `adventureworks2019.Sales.SalesOrderDetail` as sale_detail
LEFT JOIN `adventureworks2019.Production.Product` as product_tab
ON sale_detail.ProductID = product_tab.ProductID
LEFT JOIN `adventureworks2019.Production.ProductSubcategory` as product_sub
ON cast(product_tab.ProductSubcategoryID as INT) = product_sub.ProductSubcategoryID
WHERE date(sale_detail.ModifiedDate) >= 
        (SELECT DATE_SUB(max(date(ModifiedDate)), interval 12 month) 
          FROM `adventureworks2019.Sales.SalesOrderDetail`)
GROUP BY period, name
ORDER BY period DESC, name;

--Q2: Calc % YoY growth rate by SubCategory & release top 3 cat with highest grow rate. Can use metric: quantity_item. Round results to 2 decimal
WITH Total_Order as
(SELECT
  EXTRACT(YEAR FROM sale_detail.ModifiedDate) as year,
  product_sub.Name,
  SUM(sale_detail.OrderQty) as Qty_Order
FROM `adventureworks2019.Sales.SalesOrderDetail` as sale_detail
LEFT JOIN `adventureworks2019.Production.Product` as product_tab
ON sale_detail.ProductID = product_tab.ProductID
LEFT JOIN `adventureworks2019.Production.ProductSubcategory` as product_sub
ON cast(product_tab.ProductSubcategoryID as INT) = product_sub.ProductSubcategoryID
GROUP BY year, Name
ORDER BY year),

curr_prev_qty as
(SELECT 
  year,
  Name,
  Qty_Order as qty_item,
  LAG(Qty_Order) OVER(PARTITION BY Name ORDER BY year) as prv_qty    
FROM Total_Order
ORDER BY year)

SELECT
  Name,
  qty_item,
  prv_qty,
  ROUND((qty_item - prv_qty)/prv_qty , 2) as qty_diff
FROM curr_prev_qty
ORDER BY qty_diff DESC
LIMIT 3;

--Q3: Ranking Top 3 TeritoryID with biggest Order quantity of every year. If there's TerritoryID with same quantity in a year, do not skip the rank number
WITH sum_ord_territory as
(SELECT
  EXTRACT(YEAR FROM sale_detail.ModifiedDate) as year,
  sale_header.TerritoryID as TerritoryID,
  SUM(sale_detail.OrderQty) as order_cnt
FROM `adventureworks2019.Sales.SalesOrderDetail` as sale_detail
LEFT JOIN `adventureworks2019.Sales.SalesOrderHeader` as sale_header
ON sale_detail.SalesOrderID = sale_header.SalesOrderID
GROUP BY EXTRACT(YEAR FROM sale_detail.ModifiedDate),sale_header.TerritoryID
ORDER BY order_cnt DESC),

ranked_ord_qty as 
(SELECT
  year as yr,
  TerritoryID,
  order_cnt,
  DENSE_RANK() OVER(PARTITION BY year ORDER BY order_cnt DESC) as ranked_order
FROM sum_ord_territory)

SELECT
  yr,
  TerritoryID,
  order_cnt,
  ranked_order as rk
FROM ranked_ord_qty
WHERE ranked_order between 1 and 3;

--Q4: Calc Total Discount Cost belongs to Seasonal Discount for each SubCategory
WITH discount_cost as 
(SELECT 
  EXTRACT(YEAR FROM sale_detail.ModifiedDate) as year,
  product_sub.Name,
  (sale_offer.DiscountPct * sale_detail.UnitPrice * sale_detail.OrderQty) as discount
FROM `adventureworks2019.Sales.SalesOrderDetail` as sale_detail
LEFT JOIN `adventureworks2019.Production.Product` as product_tab
ON sale_detail.ProductID = product_tab.ProductID
LEFT JOIN `adventureworks2019.Production.ProductSubcategory` as product_sub
ON cast(product_tab.ProductSubcategoryID as INT) = product_sub.ProductSubcategoryID
LEFT JOIN `adventureworks2019.Sales.SpecialOffer` as sale_offer
ON sale_detail.SpecialOfferID = sale_offer.SpecialOfferID
WHERE lower(sale_offer.Type) like '%seasonal discount%')

SELECT
  year,
  Name,
FROM discount_cost
GROUP BY year, Name;

--Q5: Retention rate of Customer in 2014 with status of Successfully Shipped (Cohort Analysis).
WITH cust_all_month as
(SELECT
  EXTRACT(MONTH FROM  ModifiedDate) as month_all,
  CustomerID,
  COUNT(distinct SalesOrderID) as num_sales
FROM `adventureworks2019.Sales.SalesOrderHeader`
WHERE EXTRACT(YEAR FROM ModifiedDate) = 2014 and Status = 5
GROUP BY EXTRACT(MONTH FROM  ModifiedDate), CustomerID),

first_month_shipped as
(SELECT 
  month_all as month_first,
  CustomerID,
  num_sales
FROM 
  (SELECT 
      *,
      ROW_NUMBER() OVER(PARTITION BY CustomerID ORDER BY month_all) as rn_cust
  FROM cust_all_month)
WHERE rn_cust = 1)

SELECT
  month_first as month_join,
  CONCAT('M',' - ',full_ord.month_all - first_ord.month_first) as month_diff,
  count(first_ord.CustomerID) as customer_cnt
FROM cust_all_month as full_ord
LEFT JOIN first_month_shipped as first_ord
ON full_ord.CustomerID = first_ord.CustomerID
GROUP BY  month_first, month_all
ORDER BY month_join, month_diff;

--Q6: Trend of Stock level & MoM diff % by all product in 2011. If %gr rate is null then 0. Round to 1 decimal.
WITH num_stock as
(SELECT
  EXTRACT(YEAR FROM  wod.ModifiedDate) as year,
  EXTRACT(MONTH FROM  wod.ModifiedDate) as month,
  prod.Name as product_name,
  SUM(wod.StockedQty) as total_stock
FROM `adventureworks2019.Production.Product` as prod
LEFT JOIN `adventureworks2019.Production.WorkOrder` as wod
ON prod.ProductID = wod.ProductID
GROUP BY 1,2,3
ORDER BY product_name),

prev_total as
(SELECT
  month,
  year,
  product_name,
  total_stock as current_stock,
  LAG(total_stock) OVER(PARTITION BY product_name ORDER BY year, month) as prev_stock
FROM num_stock)

SELECT
  *,
  ROUND(COALESCE(((current_stock-prev_stock)/prev_stock)*100.0,0),1) as diff
FROM prev_total
WHERE year = 2011
ORDER BY product_name, month DESC;

--Q7:  Calc Ratio of Stock / Sales in 2011 by product name, by month. Order results by month desc, ratio desc. Round Ratio to 1 decimal mom yoy.
WITH cte1 as
(SELECT
  EXTRACT(YEAR FROM  sale_detail.ModifiedDate) as year,
  EXTRACT(MONTH FROM  sale_detail.ModifiedDate) as month,
  prod.Name as product_name,
  sale_detail.ProductID as product_ID,
  SUM(sale_detail.OrderQty) as total_order
FROM `adventureworks2019.Sales.SalesOrderDetail` as sale_detail
LEFT JOIN `adventureworks2019.Production.Product` as prod
ON sale_detail.ProductID = prod.ProductID
WHERE EXTRACT(YEAR FROM  sale_detail.ModifiedDate) = 2011
GROUP BY 1,2,3,4),

cte2 as
(SELECT
  EXTRACT(YEAR FROM  ModifiedDate) as year1,
  EXTRACT(MONTH FROM  ModifiedDate) as month1,
  ProductID,  
  SUM(StockedQty) as total_stock,
FROM`adventureworks2019.Production.WorkOrder`
WHERE EXTRACT(YEAR FROM  ModifiedDate) = 2011
GROUP BY 1,2,3)

SELECT
  a.month,
  a.year,
  a.product_ID,
  a.product_name,
  a.total_order as sales,
  COALESCE(b.total_stock,0) as stock,
  ROUND(COALESCE((total_stock/total_order),0),1) as ratio
FROM cte1 as a
LEFT JOIN cte2 as b
ON a.product_ID = b.ProductID
AND a.month = b.month1
ORDER BY month DESC,ratio DESC;

--Q8: No of order and value at Pending status in 2014.
SELECT 
  EXTRACT(YEAR FROM  ModifiedDate) as year,
  Status,
  COUNT(distinct PurchaseOrderID) as order_cnt ,
  SUM(TotalDue) as value
FROM `adventureworks2019.Purchasing.PurchaseOrderHeader`
WHERE Status = 1
AND EXTRACT(YEAR FROM  ModifiedDate) = 2014
GROUP BY 1,2;
 