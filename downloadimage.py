# -------------Developer-------------- #
# Rohit Singh
# Email: rohitsingh119cs@gmail.com
# -------------Developer-------------- #

import concurrent.futures
import requests
from pathlib import Path

# Path of the file contain URLS replace with urls.txt and provide the download location
urls_file = open('urls.txt', 'r')
urls = urls_file.readlines()
download_file_path = "download/"
logfile = open("logs.txt", "a")

# Variables for logs file
Total_url = 0
Downloaded_Count = 0
Not_Downloadable = 0
already_available_file = 0
Total_downloaded_size = 0


# Check the URL Content is Downloadable or not

def is_downloadable(url):
    try:
        h = requests.head(url, allow_redirects=True)
        header = h.headers
        content_type = header.get('content-type')
        content_size = header.get('Content-Length')
        print("File Size", int(content_size) / 1000, "kb")
        global Total_downloaded_size
        Total_downloaded_size += int(content_size)
        if 'text' in content_type.lower():
            return False
        if 'html' in content_type.lower():
            return False
        return True
    except Exception as e:
        return False


# Get the filename from the urls
def filename_from_url(url):
    if not url:
        return None
    if url.strip().find('/'):
        first = url.strip().rsplit('/', 1)[1]
        split_string = first.split("?", 1)
        return split_string[0]


# Iterate the files urls one by one from file and create the file
def download_urls(url):
    global Total_url
    global already_available_file
    global Downloaded_Count
    global Not_Downloadable
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
        logfile.write(url.strip())
        logfile.write("\n")


with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(download_urls, urls)

logfile.write("###############################################################################\n" +
              "Total URLs To be Downloaded = " + str(Total_url) + " Links" + '\n' +
              "Total Images Link Not Downloadable = " + str(Not_Downloadable) + " Files" + '\n' +
              "Total New Images Downloaded = " + str(Downloaded_Count) + " Files" + '\n' +
              "Images Already Available or Downloaded in Folder = " + str(already_available_file) + " Files" + '\n' +
              "Total Downloaded Size = " + str(round(int(Total_downloaded_size) / 1048576, 2)) + "Mb" + "\n" +
              "###############################################################################\n")

message = "-------------------------------------------------------------------------------\n"
message += "Total Images URLs = " + str(Total_url) + "\n"
message += "Total Images Link Not Downloadable = " + str(Not_Downloadable) + "\n"
message += "Total New Images Downloaded = " + str(Downloaded_Count) + "\n"
message += "Downloaded Images Already Available in Folder = " + str(already_available_file) + "\n"
message += "Downloaded Size = " + str(round(int(Total_downloaded_size) / 1048576, 2))+ "Mb" + "\n"
message += "-------------------------------------------------------------------------------" + "\n"
print(message)
logfile.close()
