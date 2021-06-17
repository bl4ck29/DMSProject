from bs4 import BeautifulSoup
import lxml, os, re
def CheckTitle(path):
    lst = []
    os.chdir(path)
    for file in os.listdir():
        file_name = path + "/" +file
        soup = BeautifulSoup(open(file_name, encoding="utf-8"), features="lxml")
        title = soup.find("h1")
        try:
            if "tuyển" in title.text.lower():
                lst.append(file_name)
        except:
            continue
    return lst

def CheckDate(data):
    ind = data.index("Thời gian nhận hồ sơ")
    date = data[ind : data.index("<", ind)].lower()
    pattern = "../../...."
    for i in range(len(date)):
        check = date[i : ]
        if re.match(pattern, check):
            return check

def DictToJsonFile(dct, file):
    result = '{'
    for key, item in dct.items():
        if key == "requirements":
            result += '"requirements":['
            for i in range(len(item)):
                if i == len(item)-1:
                    result += '"{}"'.format(item[i])
                else:
                    result += '"{}",'.format(item[i])
            result += ']'
        elif key == "quantity":
            if type(item) == int:
                result += '"{}":{},'.format(key, item)
            else:
                result += '"{}":"{}",'.format(key, item)
        else:
            result += '"{}":"{}",'.format(key, item)
    result += '}\n'
    file.write(result)

DesFile = open("/home/vlu1/CrawledData/recruitments.json", "a", encoding="utf-8")
ListFile = CheckTitle("/home/vlu1/CrawledData/www.traphaco.com.vn")
for file in ListFile:
    print(file)
    data = open(file, encoding="utf-8").read()
    soup = BeautifulSoup(open(file, encoding="utf-8"), features="lxml")
    timeSt = soup.find("span", class_="news-time").text

    vacancy = soup.find("h1").text.lower()
    vacancy = vacancy[vacancy.index("tuyển dụng")+len("tuyển dụng ") : ]
    
    quantity = None
    workplace = None
    requirements = []
    for p in soup.find_all("p"):
        string = p.text.lower()
        if "số lượng cần tuyển: " in string:
            ind = string.index("số lượng cần tuyển: ")
            quantity = int(string[string.index(":", ind)+2 : string.index("\n", ind)])
        if "nơi làm việc: " in string:
            indWork = string.index("nơi làm việc: ")
            workplace = string[string.index(":", indWork)+2 : ]
        if "tiêu chuẩn" in string:
            require = string[len("tiêu chuẩn")+1: ].split("\n")
            for i in require:
                requirements.append(i)
    if len(requirements) <= 1:
        lst = []
        requirements = []
        for p in soup.find_all("p"):
            if p.text != "":
                lst.append(p.text)
        for require in lst[lst.index("Tiêu chuẩn")+1: lst.index("Hồ sơ dự tuyển: Bản cứng")]:
            requirements.append(require)
    if workplace != None:
            vacancy += " - " + workplace
    info={
        "company_name" : "TRAPHACO",
        "time_post" : timeSt,
        "time_deadline" : CheckDate(data),
        "vacancy" : vacancy,
        "quantity" : quantity,
        "salary" : None,
        "requirements" : requirements
    }
    DictToJsonFile(info, DesFile)
DesFile.close()