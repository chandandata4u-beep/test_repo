#!/usr/bin/env python3

import boto3
import json
import os
import logging
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.oauth2.service_account import Credentials
from botocore.exceptions import ClientError

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS clients
s3_client = boto3.client('s3')
secrets_client = boto3.client('secretsmanager')

def get_creds():
    secret_response = secrets_client.get_secret_value(SecretId="gdrive-creds")
    secret = json.loads(secret_response['SecretString'])
    gdrive_folder_id = secret['google-drive-folder-id']
    svc_creds = json.loads(secret['google-service-account-credentials'])
    return gdrive_folder_id, svc_creds

def list_s3_files(bucket_name, prefix=""):
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    if 'Contents' in response:
        return [
            obj['Key']
            for obj in response['Contents']
            if not obj['Key'].endswith('/')
        ]
    return []

def list_drive_files(drive_service, folder_id):
    def fetch_files(folder_id, current_path=""):
        query = f"'{folder_id}' in parents and trashed=false"
        results = drive_service.files().list(q=query, fields="files(id, name, mimeType)").execute()
        files = results.get('files', [])
        all_files = []

        for file in files:
            file_path = f"{current_path}/{file['name']}" if current_path else file['name']
            if file['mimeType'] == 'application/vnd.google-apps.folder':
                all_files.extend(fetch_files(file['id'], file_path))
            else:
                all_files.append(file_path)

        return all_files

    return fetch_files(folder_id)

def compare_file_paths(gdrive_files, s3_files):
    return {
        "in_gdrive_not_in_s3": list(set(gdrive_files) - set(s3_files)),
        "in_s3_not_in_gdrive": list(set(s3_files) - set(gdrive_files))
    }

def sync_missing_files(mismatches, gdrive_folder_id, drive_service, s3_bucket):
    def resolve_gdrive_path(full_path, drive_service, root_folder_id):
        path_parts = full_path.split('/')
        parent_id = root_folder_id

        for folder in path_parts[:-1]:
            query = f"name='{folder}' and '{parent_id}' in parents and mimeType='application/vnd.google-apps.folder'"
            response = drive_service.files().list(q=query, fields="files(id)").execute()
            folders = response.get('files', [])
            if folders:
                parent_id = folders[0]['id']
            else:
                folder_metadata = {'name': folder, 'parents': [parent_id], 'mimeType': 'application/vnd.google-apps.folder'}
                folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
                parent_id = folder['id']
        return parent_id

    # Upload S3 → Google Drive
    for s3_key in mismatches.get("in_s3_not_in_gdrive", []):
        local_file_path = f"/tmp/{os.path.basename(s3_key)}"

        try:
            s3_client.download_file(s3_bucket, s3_key, local_file_path)
        except ClientError as e:
            logger.error(f"Failed to download {s3_key} from S3: {e}")
            continue

        parent_id = resolve_gdrive_path(s3_key, drive_service, gdrive_folder_id)
        file_metadata = {'name': os.path.basename(s3_key), 'parents': [parent_id]}
        media = MediaFileUpload(local_file_path, resumable=True)
        drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        os.remove(local_file_path)
        logger.info(f"Uploaded {s3_key} to Google Drive")

    # Upload Google Drive → S3 (commented out for now)
    """
    for gdrive_file in mismatches.get("in_gdrive_not_in_s3", []):
        local_file_path = f"/tmp/{os.path.basename(gdrive_file)}"
        parent_id = resolve_gdrive_path(gdrive_file, drive_service, gdrive_folder_id)
        query = f"name='{os.path.basename(gdrive_file)}' and '{parent_id}' in parents"
        response = drive_service.files().list(q=query, fields="files(id)").execute()
        files = response.get('files', [])
        if not files:
            logger.error(f"{gdrive_file} not found in Google Drive.")
            continue
        file_id = files[0]['id']
        request = drive_service.files().get_media(fileId=file_id)
        with open(local_file_path, 'wb') as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()
        s3_client.upload_file(local_file_path, s3_bucket, gdrive_file)
        os.remove(local_file_path)
        logger.info(f"Uploaded {gdrive_file} to S3")
    """

def main():
    s3_bucket = "pds-comm-contract-attachments-global-dev"
    gdrive_folder_id, svc_creds = get_creds()
    creds = Credentials.from_service_account_info(svc_creds)
    drive_service = build('drive', 'v3', credentials=creds)

    s3_files = list_s3_files(s3_bucket)
    gdrive_files = list_drive_files(drive_service, gdrive_folder_id)

    mismatches = compare_file_paths(gdrive_files, s3_files)
    logger.info(f"Mismatched files: {json.dumps(mismatches, indent=2)}")

    sync_missing_files(mismatches, gdrive_folder_id, drive_service, s3_bucket)

if __name__ == "__main__":
    main()
