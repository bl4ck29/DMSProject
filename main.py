import os, subprocess, pymongo, requests, lxml, re, json
from bs4 import BeautifulSoup
path = "/home/vlu1/CrawlingTool"
os.chdir(path)
ListFile = os.listdir()
DesFile = open("/home/vlu1/CrawledData/recruitments.json", "w")
DesFile.close()
if "crawlingTool.py" in ListFile:
    subprocess.run("python3 %s"%(path + "/" + "crawlingTool.py"), shell=True)
    for file in os.listdir():
        if "scrape" in file:
            print("Running {} ...".format(file), end="")
            subprocess.run("python3 {}".format(path+"/"+file), shell=True)
            print("DONE")
        print("Upload data to MongoDB")
        subprocess.run("python3 {}".format(path+"/"+"InsertToMongo.py"), shell=True)
        print("DONE")
else:
    raise(FileNotFoundError)