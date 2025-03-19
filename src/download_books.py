import pandas as pd
import requests
import os
import re


csv_file = 'Books.csv'

'''
ENTER ABSOLUTE OR RELATIVE PATH OF THE DIRECTORY YOU WANT TO SAVE THE DOWNLOADED BOOKS IN.

'''
download_dir = 'Books'  # To use the root directory only enter the directory name


# Ensure the download directory exists
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Read the CSV file
df = pd.read_csv(csv_file)

# Function to get file format from URL using regex
def get_file_format(url):
    match = re.search(r'ext=([^&]+)', url)
    if match:
        return '.' + match.group(1)
    return ''

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    title = row['Title']
    download_link = row['Download Link']

    # Get file format from the download link
    file_format = get_file_format(download_link)
    
    # Create a safe file name from the title
    safe_title = "".join([c if c.isalnum() else "_" for c in title])
    file_path = os.path.join(download_dir, f"{safe_title}{file_format}")

    # Download the file
    try:
        response = requests.get(download_link, stream=True)
        response.raise_for_status()  # Check for request errors

        
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Downloaded: {title} as {file_format}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download {title}: {e}")

print("Download completed.")