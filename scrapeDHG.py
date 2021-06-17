from bs4 import BeautifulSoup
import lxml, os, re

def CheckTitle(path):
    lst = []
    os.chdir(path)
    for file in os.listdir():
        file_name = path + "/" +file
        try:
            soup = BeautifulSoup(open(file_name, encoding="utf-8"), features="lxml")
            title = soup.find("title")
            if "tuyển" in title.text.lower():
                lst.append(file_name)
        except:
            continue
    return lst

def CheckVacancy(string):
    pattern = "(Vị trí).*:(.+)"
    if re.match(pattern, string.text):
        result = string.text.strip()
        return result[result.index(":")+1 : ]

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

# Open json file to write in
DesFile = open("/home/vlu1/CrawledData/recruitments.json", "a", encoding="utf-8")
ListFile = CheckTitle("/home/vlu1/CrawledData/www.dhgpharma.com.vn")
for file in ListFile:
    data = open(file, encoding="utf-8").read()
    soup = BeautifulSoup(open(file, encoding="utf-8"), features="lxml")
    print(file)
    # Get the published date
    TimePublished = soup.find("time", itemprop="datePublished")["datetime"]
    time_post = TimePublished[ : TimePublished.index("T")]
    time_dealine = ""

    lstVacancy = []
    lstQuantity = []
    lstWorkplace = []
    table = soup.find("table")
    for p in table.find_all("p"):
        if CheckVacancy(p) !=None:
            lstVacancy.append(CheckVacancy(p))
        if p.text.find("tại")>=0:
            lstWorkplace.append(p.text[p.text.index("tại") : ])
        try:
            lstQuantity.append(int(p.text))
        except ValueError:
            if re.match("Số lượng: [0-9][0-9]", p.text):
                quan = p.text.strip()
                lstQuantity.append(int(quan[quan.rindex(" ")+1 : ]))
            if re.match("[0-9][0-9] .*", p.text):
                quan = p.text.strip()
                lstQuantity.append(int(quan[ : quan.index(" ")]))
            else:
                continue

    for p in soup.find_all("p"):
        if p.text.find("Thời gian nộp")>=0:
            time_dealine = p.text[p.text.rindex(" ")+1: ].replace(".", "")
    if time_dealine == "":
        for li in soup.find_all("li"):
            if li.text.find("Thời gian nộp")>=0:
                time_dealine = li.text[li.text.rindex(" ")+1: ].replace(".", "")
    # Getting requirments
    counter = 0
    ind_st = 0
    ind_end = 0
    lstStartInd = []
    lstEndInd = []
    while counter < len(lstVacancy):
        if counter == 0:
            ind_st = data.index("Trình độ")
            ind_end = data.index("Mô tả")
            lstStartInd.append(ind_st)
            lstEndInd.append(ind_end)
            counter +=1
        else:
            ind_st = data.index("Trình độ", ind_st + 1)
            ind_end = data.index("Mô tả", ind_end + 1)
            lstStartInd.append(ind_st)
            lstEndInd.append(ind_end)
            counter += 1
    checker = True
    while checker:
        if len(lstQuantity) < len(lstVacancy):
            lstQuantity.append(None)
        elif len(lstWorkplace) < len(lstVacancy):
            lstWorkplace.append(None)
        else:
            checker = False
    for i in range(len(lstVacancy)):
        require = data[lstStartInd[i] : lstEndInd[i]]
        ind_st = 0
        ind_end = 0
        while True:
            try:
                ind_st = require.index("<")
                ind_end = require.index(">") + 1
                subString = require[ind_st : ind_end]
                require = require.replace(subString, "")
                if ind_end == len(require)-1 :
                    break
            except ValueError :
                break
        require = require.replace("\t", "")
        require = require.split("\n")
        while True:
            try:
                require.remove("")
            except ValueError:
                break
        require.remove(require[0])
        try:
            require.remove("&nbsp;")
        except:
            print()
        requirements = []
        for a in range(len(require)):
            try:
                requirements.append(require[a].replace("-&nbsp;", ""))
            except:
                requirements.append(require[a])
        if lstWorkplace[i] != None:
            lstVacancy[i] += " - " + lstWorkplace[i]
        info = {
            "company_name" : "DHG_Pharma",
            "time_post": time_post,
            "time_deadline" : time_dealine,
            "vacancy" : lstVacancy[i],
            "quantity" : lstQuantity[i],
            "salary" : None,
            "requirements" : requirements
        }
        DictToJsonFile(info, DesFile)
DesFile.close()