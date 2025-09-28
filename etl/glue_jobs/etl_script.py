import pandas as pd
import awswrangler as wr
import boto3

# ===============================
# S3 Buckets
# ===============================
RAW_BUCKET = "s3://cloud-ecommerce-dashboard/raw"
PROCESSED_BUCKET = "s3://cloud-ecommerce-dashboard/processed"

# Filenames (CSV files in raw bucket)
ORDERS_FILE = "orders.csv"
PRODUCTS_FILE = "products.csv"
CUSTOMERS_FILE = "customers.csv"

# ===============================
# Read CSV files from S3
# ===============================
print("Reading raw CSV files from S3...")

orders_df = wr.s3.read_csv(f"{RAW_BUCKET}/{ORDERS_FILE}")
products_df = wr.s3.read_csv(f"{RAW_BUCKET}/{PRODUCTS_FILE}")
customers_df = wr.s3.read_csv(f"{RAW_BUCKET}/{CUSTOMERS_FILE}")

print("Files loaded successfully!")

# ===============================
# Data Cleaning
# ===============================
# Drop rows with missing essential data
orders_df.dropna(subset=['order_id', 'product_id', 'customer_id', 'price'], inplace=True)
products_df.dropna(subset=['product_id', 'category'], inplace=True)
customers_df.dropna(subset=['customer_id'], inplace=True)

# Standardize date column
orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])

# ===============================
# Merge Datasets
# ===============================
print("Merging datasets...")
merged_df = orders_df.merge(products_df, on='product_id', how='left')
merged_df = merged_df.merge(customers_df, on='customer_id', how='left')

# ===============================
# Feature Engineering
# ===============================
# Calculate revenue per order item
merged_df['revenue'] = merged_df['price'] * merged_df['order_item_id']

# Optional: create order_month for trend analysis
merged_df['order_month'] = merged_df['order_purchase_timestamp'].dt.to_period('M')

# ===============================
# Save Processed Data to S3
# ===============================
print("Saving processed data to S3 in Parquet format...")

wr.s3.to_parquet(
    df=merged_df,
    path=f"{PROCESSED_BUCKET}/fact_sales.parquet",
    dataset=True,
    mode="overwrite"
)

print("ETL job completed successfully!")
