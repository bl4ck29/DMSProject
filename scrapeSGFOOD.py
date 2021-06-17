from bs4 import BeautifulSoup
import lxml, os, re

def CheckTitle(path):
    lst = []
    os.chdir(path)
    for file in os.listdir():
        file_name = path + "/" +file
        soup = BeautifulSoup(open(file_name, encoding="utf-8"), features="lxml")
        title = soup.find("title")
        if "tuyển" in title.text.lower():
            lst.append(file_name)
    return lst

def CheckDate(date):
    date = date.text.lower()
    pattern = "../../...."
    for i in range(len(date)):
        check = date[i : ]
        if re.match(pattern, check):
            return check

def GetRequirements(data, lstVacancy):
    indSt = 0
    indEnd = 0
    lstSt = []
    lstEnd = []
    count = 0
    res = []
    try:
        while count < len(lstVacancy):
            if count == 0:
                indSt = data.index("YÊU CẦU CÔNG VIỆC:")
                lstSt.append(indSt)
                indEnd = data.index("MÔ TẢ CÔNG VIỆC")
                lstEnd.append(indEnd)
                count +=1
            else:
                indSt = data[indSt+len("YÊU CẦU CÔNG VIỆC:") : ].index("YÊU CẦU CÔNG VIỆC:")
                lstSt.append(indSt)
                indEnd = data.index("MÔ TẢ CÔNG VIỆC")
                lstEnd.append(indEnd)
                count+=1
            for i in range(len(lstVacancy)):
                require = data[lstSt[i] : lstEnd[i]]
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
                requirements = []
                for a in range(len(require)):
                    requirements.append(require[a])
                res.append(requirements)
    except:
        return res
    return res

def DictToJsonFile(dct, file):
    result = '{'
    for key, item in dct.items():
        if key == "requirements":
            result += '"requirements":['
            if item != None:
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
    

DesFile = open("/home/vlu1/CrawledData/recruitments.json", mode="a", encoding="utf-8")
ListFile = CheckTitle("/home/vlu1/CrawledData/sgfoods.com.vn")

for file in ListFile:
    data = open(file, encoding="utf-8").read()
    soup = BeautifulSoup(open(file, encoding="utf-8"), features="lxml")
    print(file)
    lstVacancy = []
    for vacancy in soup.find_all("h1", class_="page-titte"):
        lstVacancy.append(vacancy.text)
    
    lstTimeStart = []
    for timeStart in soup.find_all("div", class_="col-sm-6 right-box"):
        lstTimeStart.append(CheckDate(timeStart))
    
    lstTimeEnd = []
    lstWorkplace = []
    lstSalary = []
    for li in soup.find_all("li"):
        if "hạn" in li.text.lower():
            lstTimeEnd.append(CheckDate(li))
        if "địa điểm" in li.text.lower():
            lstWorkplace.append(li.text[li.text.index(":")+1 : ])
        if "mức lương:" in li.text.lower():
            lstSalary.append(li.text[li.text.index(":")+1 : ].strip())
    
    for p in soup.find_all("p"):
        if "hạn" in p.text.lower():
            lstTimeEnd.append(CheckDate(p))
        if "địa điểm" in p.text.lower():
            lstWorkplace.append(p.text[p.text.index(":")+1 : ])
        if "mức lương:" in p.text.lower():
            lstSalary.append(p.text[p.text.index(":")+1 : ].strip())

    lstQuantity = []
    requirements = GetRequirements(data, lstVacancy)
    checker = True
    while checker:
        if len(lstQuantity) < len(lstVacancy):
            lstQuantity.append(None)
        elif len(lstWorkplace) < len(lstVacancy):
            lstWorkplace.append(None)
        elif len(lstTimeEnd) < len(lstVacancy):
            lstTimeEnd.append(None)
        elif len(lstSalary) < len(lstVacancy):
            lstSalary.append(None)
        elif len(requirements) < len(lstVacancy):
            requirements.append(None)
        else:
            checker = False
    for i in range(len(lstVacancy)):
        if lstWorkplace[i] != None:
            lstVacancy += " - " + lstWorkplace[i]
        info = {
            "company_name" : "SaigonFood",
            "time_post": lstTimeStart[i].strip(),
            "time_deadline" : lstTimeEnd[i],
            "salary" : lstSalary[i],
            "vacancy" : lstVacancy[i],
            "quantity" : lstQuantity[i],
            "requirements" : requirements[i]
        }
        DictToJsonFile(info, DesFile)
DesFile.close()