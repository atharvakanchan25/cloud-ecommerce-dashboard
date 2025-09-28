-- ===============================================
-- Analysis Queries for Tableau Dashboard
-- ===============================================

-- 1. Total Revenue
SELECT SUM(revenue) AS total_revenue
FROM fact_sales_transformed;

-- 2. Total Orders
SELECT COUNT(DISTINCT order_id) AS total_orders
FROM fact_sales_transformed;

-- 3. Total Customers
SELECT COUNT(DISTINCT customer_id) AS total_customers
FROM fact_sales_transformed;

-- 4. Monthly Revenue Trend
SELECT order_month, SUM(revenue) AS monthly_revenue
FROM fact_sales_transformed
GROUP BY order_month
ORDER BY order_month;

-- 5. Top 10 Products by Revenue
SELECT product_name, SUM(revenue) AS total_revenue
FROM fact_sales_transformed
GROUP BY product_name
ORDER BY total_revenue DESC
LIMIT 10;

-- 6. Revenue by Category
SELECT category, SUM(revenue) AS total_revenue
FROM fact_sales_transformed
GROUP BY category
ORDER BY total_revenue DESC;

-- 7. Revenue by Customer State (Geo Analysis)
SELECT customer_state, SUM(revenue) AS total_revenue
FROM fact_sales_transformed
GROUP BY customer_state
ORDER BY total_revenue DESC;

-- 8. Payment Type Analysis (if payments table exists)
-- SELECT p.payment_type, SUM(p.payment_value) AS total_revenue
-- FROM payments p
-- JOIN fact_sales_transformed f ON p.order_id = f.order_id
-- GROUP BY p.payment_type
-- ORDER BY total_revenue DESC;
