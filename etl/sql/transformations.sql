-- ===============================================
-- Data Transformations for Fact Sales
-- ===============================================

-- 1. Add Month Column for Trend Analysis
CREATE OR REPLACE VIEW fact_sales_transformed AS
SELECT 
    order_id,
    product_id,
    customer_id,
    order_purchase_timestamp,
    price,
    order_item_id,
    revenue,
    category,
    product_name,
    customer_state,
    customer_city,
    customer_zip_code,
    date_format(order_purchase_timestamp, '%Y-%m') AS order_month
FROM fact_sales;

-- 2. Optional: Calculate Total Revenue per Order
-- (If ETL did not calculate revenue)
-- CREATE OR REPLACE VIEW fact_sales_revenue AS
-- SELECT *,
--        price * order_item_id AS revenue
-- FROM fact_sales;
