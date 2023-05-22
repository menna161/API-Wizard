import boto3
import config
import csv
import datetime


def get_latest_bill(aws_id, billing_bucket, billing_file_path, save):
    '\n  get the latest billing CSV from S3 (default) or a local file.\n  args:\n    aws_id:             AWS account number\n    billing_bucket:     name of the billing bucket\n    billing_file_path:  full path to consolidated billing file on a local\n                        FS (optional)\n    save:               save the CSV to disk with the default filename\n\n  returns:\n    csv object of billing data\n  '
    if billing_file_path:
        f = open(billing_file_path, 'r')
        billing_data = f.read()
    else:
        today = datetime.date.today()
        month = today.strftime('%m')
        year = today.strftime('%Y')
        billing_filename = (((((aws_id + '-aws-billing-csv-') + year) + '-') + month) + '.csv')
        s3 = boto3.resource('s3')
        b = s3.Object(billing_bucket, billing_filename)
        billing_data = b.get()['Body'].read().decode('utf-8')
        if (not billing_data):
            print(('unable to find billing data (%s) in your bucket!' % billing_filename))
            sys.exit((- 1))
    if save:
        f = open(billing_filename, 'w')
        f.write(billing_data)
        f.close
    return csv.reader(billing_data.split('\n'))
