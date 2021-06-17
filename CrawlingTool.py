import requests, lxml, subprocess, os, re
from bs4 import BeautifulSoup

def IsInternalLink(workingURL, url):
    if "://" in url:
        if url[ : url.index("/", url.index("://")+3)] in workingURL:
            return True
        return False
    pattern = "(.)*/(.)*/(.)*"
    if re.match(pattern, url):
        return True
    return False
    
def HaveNextPage(soup):
    nextPage = None
    if soup.find("a", title="Trang sau") != None:
        nextPage =soup.find("a", title="Trang sau")
    else :
        nextPage = soup.find("a", title="Go to next page")
    if nextPage == None:
        return False
    return nextPage["href"]

def CrawlWebsite(url, ind):
    links = []

    # Get the home page
    path = url[ : url.index("/", len("https://"))]

    # Path to store crawled data
    FolderName = url[url.index("://")+3 : url.index("/", url.index("://")+3)]
    SourceFolder = "D:/DA_DMS/" + FolderName
    os.chdir("D:/DA_DMS/")
    if FolderName not in os.listdir():
        os.mkdir(SourceFolder)
    #Request to the website
    response = requests.get(url).text

    soup = BeautifulSoup(response, features="lxml")

    if HaveNextPage(soup) != False:
        urls.append(path+"/"+HaveNextPage(soup))
    # Go through each tag a
    for a in soup.find_all("a"):
        try:
            # Get the link
            link = a["href"]
            if IsInternalLink(url, link):
                # Add the link to list
                if link not in urls :
                    links.append(link)
        # Handling when tag a dont have any href
        except:
            continue

    #Store crawled data
    for link in links:
        try:
            if not link.startswith("/") and "http" not in link:
                link = "/"+link
            if "://" in link:
                url = link
            else:
                url = path +link
            file_name = link[link.rindex("/") : ]
            if "." not in file_name:
                file_name += ".txt"
            if not file_name.isalpha():
                file_name = "/file_name"+str(ind)+".txt"
                ind+=1
            print(url, SourceFolder+file_name)
            subprocess.check_output('curl "%s">>%s'%(url, SourceFolder+file_name), shell=True)
        except subprocess.CalledProcessError:
            continue
        except:
            file_name = "/file_name"+str(ind)+".txt"
            print(url, SourceFolder+file_name)
            subprocess.check_output('curl "%s">>%s'%(url, SourceFolder+file_name), shell=True)

# Main function
ind = 0
urls = [
    
    "https://sgfoods.com.vn/vi/news-categories/tuyen-dung"
]
count = 0
while count < len(urls):
    CrawlWebsite(urls[count], ind)
    count += 1