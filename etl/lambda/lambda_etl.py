import json
import boto3
import awswrangler as wr
import pandas as pd
import os

# Initialize S3 client
s3 = boto3.client('s3')

# Lambda handler
def lambda_handler(event, context):
    """
    This Lambda function triggers ETL whenever new files are uploaded to S3.
    It reads configuration from lambda_trigger_config.json.
    """

    # Load configuration
    config_bucket = "cloud-ecommerce-dashboard"  # Replace with your bucket if needed
    config_key = "automation/lambda_trigger_config.json"
    
    config_object = s3.get_object(Bucket=config_bucket, Key=config_key)
    config_data = json.loads(config_object['Body'].read().decode('utf-8'))

    raw_bucket = config_data['raw_data_bucket'].replace("s3://", "")
    processed_bucket = config_data['processed_data_bucket'].replace("s3://", "")
    etl_script_path = config_data['etl_script_path']

    # Process each S3 event (new uploaded file)
    for record in event['Records']:
        file_key = record['s3']['object']['key']
        file_type = os.path.splitext(file_key)[1].replace('.', '')
        
        if file_type not in config_data['file_types']:
            print(f"Skipped file {file_key}, not in allowed types")
            continue
        
        print(f"Processing file: {file_key}")
        
        # Read CSV from S3
        df = wr.s3.read_csv(path=f"s3://{raw_bucket}/{file_key}")
        
        # Example ETL: Drop nulls, create revenue column
        df.dropna(inplace=True)
        if 'price' in df.columns and 'order_item_id' in df.columns:
            df['revenue'] = df['price'] * df['order_item_id']
        
        # Save processed file to S3 in Parquet
        output_key = file_key.replace("raw/", "processed/").replace(".csv", ".parquet")
        wr.s3.to_parquet(
            df=df,
            path=f"s3://{processed_bucket}/{output_key}",
            dataset=True,
            mode="overwrite"
        )
        
        print(f"File processed and saved to s3://{processed_bucket}/{output_key}")

    # Optional: Dashboard refresh / notification
    if config_data.get('dashboard_refresh', False):
        print("Dashboard refresh triggered (manual integration required)")

    if config_data.get('notification', {}).get('enabled', False):
        sns_arn = config_data['notification']['sns_topic_arn']
        sns = boto3.client('sns')
        sns.publish(
            TopicArn=sns_arn,
            Message=f"ETL completed for {len(event['Records'])} files.",
            Subject="ETL Job Completed"
        )

    return {
        'statusCode': 200,
        'body': json.dumps('ETL Lambda completed successfully!')
    }
