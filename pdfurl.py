import boto3
import os

# Set environment variables (use your actual AWS keys)
os.environ['AWS_ACCESS_KEY_ID'] = ''
os.environ['AWS_SECRET_ACCESS_KEY'] = ''


def upload_pdf_to_s3(file_path, bucket_name, folder_name):
    """Upload PDF to S3 bucket and return the public URL."""
    s3_client = boto3.client('s3')

    file_name = file_path.split('/')[-1]  # Extract the file name from path
    s3_key = f"{folder_name}/{file_name}"  # S3 key with folder structure (Bills/filename.pdf)

    s3_client.upload_file(file_path, bucket_name, s3_key)  # Upload the file to S3

    # Construct the S3 public URL
    s3_url = f"https://{bucket_name}.s3.eu-north-1.amazonaws.com/{s3_key}"
    print("File uploaded successfully to S3!")
    print("File URL:", s3_url)
    return s3_url

