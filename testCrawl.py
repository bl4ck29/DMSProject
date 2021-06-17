import requests, lxml, subprocess, re
from bs4 import BeautifulSoup

def HaveNextPage(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="lxml")
    nextPage = None
    if soup.find("a", title="Trang sau") != None:
        nextPage = soup.find("a", title="Trang sau")
    elif soup.find("a", class_="sau") != None:
        nextPage = soup.find("a", class_="sau")
    elif soup.find("a", rel=["next"]) != None:
        nextPage = soup.find("a", rel=["next"])
    else :
        nextPage = soup.find("a", title="Go to next page")

    if nextPage == None:
        return False
    return nextPage["href"]

def GetLink(url, lstLinks, urls):
    HomePage = url[ : url.index("/", len("https://"))]
    # Reuqest to the page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="lxml")
    # Check if page has next one
    if HaveNextPage(soup) != False:
        urls.append(HomePage+"/"+HaveNextPage(soup))
    # Get all the link in the a tag
    for a in soup.find_all("a"):
        try:
            link = a["href"]
            if "http" not in link:
                if link.startswith("/"):
                    link = HomePage + link
                else:
                    link = HomePage + "/" + link
            if (link not in lstLinks) and (HomePage in link):
                lstLinks.append(link)
        except KeyError:
            continue
urls= []
links =[]
res = requests.get("https://sgfoods.com.vn/vi/news-categories/tuyen-dung")
HomePage = "https://sgfoods.com.vn"
soup = BeautifulSoup(res.text, features="lxml")
content = soup.find("section", id="news-2")
GetLink(links, content, HomePage)

res = requests.get("https://www.dhgpharma.com.vn/vi/tuyen-dung/tin-tuyen-dung")
HomePage = "https://www.dhgpharma.com.vn"
soup = BeautifulSoup(res.text, features="lxml")
content = soup.find("main", id="content")
GetLink(links, content, HomePage)
for i in links:
    print(i)

res = requests.get("https://www.traphaco.com.vn/vi/tuyen-dung.html")
HomePage = "https://www.traphaco.com.vn"
soup = BeautifulSoup(res.text, features="lxml")
content = soup.find("div", class_="box-content")
GetLink(links, content, HomePage)
for i in links:
    print(i)

res = requests.get("http://vinapharm.com.vn/index.php/listnews/72/1/Tuyen-dung.html")
HomePage = "https://www.traphaco.com.vn"
soup = BeautifulSoup(res.text, features="lxml")
content = soup.find("div", class_="list-product all")

res = requests.get("https://satoricompany.vn/tuyen-dung/")
HomePage = "https://satoricompany.vn"
soup = BeautifulSoup(res.text, features="lxml")
content = soup.find("div", class_="information-table")

res = requests.get("http://tvpharm.com.vn/index.php/vi/tin-tuc/tin-tuyen-dung.html")
HomePage = "http://tvpharm.com.vn"
soup = BeautifulSoup(res.text, features="lxml")
content = soup.find("div", class_="component")

res = requests.get("https://dap.vn/thong-tin-tuyen-dung")
HomePage = "https://dap.vn"
soup = BeautifulSoup(res.text, features="lxml")
content = soup.find("div", class_="page-recruiment")

res = requests.get("https://www.asiafoods.vn/Tuyen-Dung#Landing")
HomePage = "https://www.asiafoods.vn"
soup = BeautifulSoup(res.text, features="lxml")
content = soup.find_all("div", class_="bs-docs-example")[1]

res = requests.get("https://www.nestle.com.vn/vi/jobs/search-jobs")
HomePage = "https://www.nestle.com.vn"
soup = BeautifulSoup(res.text, features="lxml")
content = soup.find("div", class_="table-responsive")

res = requests.get("http://www.archcafe.net/vn/cau-chuyen-archcafe/tuyen-dung/")
HomePage = "http://www.archcafe.net"
soup = BeautifulSoup(res.text, features="lxml")
content = soup.find("section", class_="content")