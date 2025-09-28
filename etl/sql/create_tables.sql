-- ===============================================
-- Create Tables for Cloud E-commerce Dashboard
-- ===============================================

-- Fact Table: Orders + Products + Customers
CREATE EXTERNAL TABLE IF NOT EXISTS fact_sales (
    order_id STRING,
    product_id STRING,
    customer_id STRING,
    order_purchase_timestamp TIMESTAMP,
    price DOUBLE,
    order_item_id INT,
    revenue DOUBLE,
    order_month STRING,
    category STRING,
    product_name STRING,
    customer_state STRING,
    customer_city STRING,
    customer_zip_code STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
STORED AS PARQUET
LOCATION 's3://cloud-ecommerce-dashboard/processed/fact_sales/';
