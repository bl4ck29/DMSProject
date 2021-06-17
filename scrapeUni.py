from bs4 import BeautifulSoup
import lxml, os, re

def CheckTitle(path):
    lst = []
    os.chdir(path)
    for file in os.listdir():
        file_name = path + "/" +file
        soup = BeautifulSoup(open(file_name, encoding="utf-8"), features="lxml")
        title = soup.find("title").text
        if "tuyển" in title.lower():
            lst.append(file_name)
    return lst

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

def GetRequirements(data):
    indSt = data.index("Yêu cầu công việc:")
    try:
        indEnd = data.index("Quyền lợi được hưởng:")
    except:
        indEnd = data.index("Chế độ phúc lợi:")
    require = data[indSt : indEnd].split("\n")
    while True:
        try:
            require.remove("")
        except: break
    require.remove(require[0])
    return require


DesFile = open("/home/vlu1/CrawledData/recruitments.json", "a", encoding="utf-8")
ListFile = CheckTitle("/home/vlu1/CrawledData/uni-president.com.vn")
for file in ListFile:
    try:
        soup = BeautifulSoup(open(file, encoding="utf-8"), features="lxml")
        content = soup.find("div", class_="entry-content")
        vacancy = soup.find("u").text
        quantity = 1
        workplace = ""
        for p in content.find_all("p"):
            if "số" in p.text.lower() and "đường" in p.text.lower():
                workplace = p.text
        timeStart = None
        timeEnd = None
        if workplace != None:
            vacancy += " - " + workplace
        info ={
            "company_name" : "Uni-president Việt Nam",
            "time_post": timeStart,
            "time_deadline" : timeEnd,
            "vacancy" : vacancy,
            "quantity" : quantity,
            "salary" : None,
            "requirements" : GetRequirements(content.text)
        }
        print(file)
        DictToJsonFile(info, DesFile)
    except:
        continue
DesFile.close()