import os
import csv
import paramiko

# Set source and destination directories for custom declaration documents
src_dir = '/data/offload-custom-raw/'
dest_dir = '/data/offload-custom-upload/'

# Set filename pattern for search
filename_pattern = '*-raw.csv'

# Set column names to extract
columns_to_extract = ['AWB', 'Name', 'Address', 'Post Code']

# Search for files matching the pattern and extract data
data = []
for filename in os.listdir(src_dir):
    if filename.endswith(filename_pattern):
        with open(os.path.join(src_dir, filename)) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                extracted_data = {k: v for k, v in row.items() if k in columns_to_extract}
                data.append(extracted_data)

# Write extracted data to a new CSV file
with open(os.path.join(dest_dir, 'AWB_upload-list.csv'), mode='w', newline='') as csv_file:
    fieldnames = columns_to_extract
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
        writer.writerow(row)

# DHL remote server details
#remote_host = 'dhl-intercon-amis.dhl.com'
remote_host = '52.152.140.6'
remote_username = 'klombar'
remote_password = 'e7_8dh6zp52'
remote_dir = '/opt/intercom-process-daily/'

# Upload file to remote server
transport = paramiko.Transport((remote_host, 22))
transport.connect(username=remote_username, password=remote_password)
sftp = paramiko.SFTPClient.from_transport(transport)
sftp.put(os.path.join(dest_dir, 'AWB_upload-list.csv'), os.path.join(remote_dir, 'AWB_upload-list.csv'))
sftp.close()
transport.close()
