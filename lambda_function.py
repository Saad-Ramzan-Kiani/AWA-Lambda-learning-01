import boto3
import csv
import io

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    if 'Records' in event:
        source_bucket = event['Records'][0]['s3']['bucket']['name']
        source_key = event['Records'][0]['s3']['object']['key']
    else:
        source_bucket = 'newwebsitebusket'
        source_key = 'stg_customers.csv'

    destination_bucket = 'learningoutputbacket'

    response = s3.get_object(Bucket=source_bucket, Key=source_key)
    content = response['Body'].read().decode('utf-8').splitlines()

    reader = csv.DictReader(content)
    fieldnames = reader.fieldnames + ['Activity']
    rows = []

    for row in reader:
        row['Activity'] = 'Active'
        rows.append(row)

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

    s3.put_object(Bucket=destination_bucket, Key=source_key, Body=output.getvalue())
