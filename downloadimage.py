# -------------Developer-------------- #
# Rohit Singh
# Email: rohitsingh119cs@gmail.com
# -------------Developer-------------- #


import requests
from pathlib import Path


# Path of the file contain URLS replace with urls.txt and provide the download location
urls_file = open('urls.txt', 'r')
urls = urls_file.readlines()
download_file_path = "download/"


# Variables for logs file
Total_url = 0
Downloaded_Count = 0
Not_Downloadable = 0
already_available_file = 0


# Check the URL Content is Downloadable or not
def is_downloadable(url):
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True


# Get the filename from the urls
def filename_from_url(url):
    if not url:
        return None
    if url.strip().find('/'):
        first = url.strip().rsplit('/', 1)[1]
        split_string = first.split("?", 1)
        return split_string[0]


# Iterate the files urls one by one from file and create the file
for url in urls:
    Total_url += 1
    if is_downloadable(url.strip()):
        filename = filename_from_url(url.strip())
        finale_file = download_file_path + filename
        if Path(finale_file).is_file():
            print("Image File Already Exist...!! File Name: ", filename)
            already_available_file += 1
        else:
            print("Downloading ... File Name : ", filename)
            file = requests.get(url.strip(), allow_redirects=True)
            open(finale_file, 'wb').write(file.content)

            Downloaded_Count += 1

    else:
        Not_Downloadable += 1

print("Total Images URLs = ", Total_url)
print("Total Images New Downloaded = ", Downloaded_Count)
print("Total Images Not Downloadable = ", Not_Downloadable)
print("Already Downloaded Files = ", already_available_file)