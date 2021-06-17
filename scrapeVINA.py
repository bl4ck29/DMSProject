from bs4 import BeautifulSoup
import lxml, os, re

def CheckTitle(path):
    lst = []
    os.chdir(path)
    for file in os.listdir():
        try:
            file_name = path + "/" +file
            soup = BeautifulSoup(open(file_name, encoding="utf-8"), features="lxml")
            title = soup.find("title").text
            if "tuyển" in title.lower():
                lst.append(file_name)
        except:
            continue
    return lst

def GetRequirements(data, lstVacancy):
    counter = 0
    ind_st = 0
    ind_end = 0
    lstStartInd = []
    lstEndInd = []
    requirements = []
    while counter < len(lstVacancy):
        if counter == 0:
            try:
                ind_st = data.index("Tiêu chuẩn")
                ind_end = data.index("Nội dung công việc")
            except:
                try:
                    ind_st = data.index("Yêu cầu trình độ")
                    ind_end = data.index("Ưu tiên")
                except:
                    return requirements
            lstStartInd.append(ind_st)
            lstEndInd.append(ind_end)
            counter +=1
        else:
            try:
                ind_st = data.index("Tiêu chuẩn", ind_st + 1)
                ind_end = data.index("Nội dung công việc", ind_end + 1)
            except:
                try:
                    ind_st = data.index("Yêu cầu trình độ", ind_st + 1)
                    ind_end = data.index("Ưu tiên", ind_end + 1)
                except:
                    return requirements
            lstStartInd.append(ind_st)
            lstEndInd.append(ind_end)
            counter += 1
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
        require = require.split("-")
        require.remove(require[0])
        requirements.append(require)
    return requirements

def DictToJsonFile(dct, file):
    result = '{'
    for key, item in dct.items():
        if key == "requirements":
            result += '"requirements":['
            if item != None:
                for i in range(len(item)):
                    if i == len(item)-1:
                        result += '"{}"'.format(item[i].strip())
                    else:
                        result += '"{}",'.format(item[i].strip())
            result += ']'
        elif key == "quantity":
            if type(item) == int:
                result += '"{}":{},'.format(key, item)
            else:
                result += '"{}":"{}",'.format(key, item)
        elif key == "company_code":
            result += '"{}":{}'.format(key, item)
        else:
            result += '"{}":"{}",'.format(key, item)
    result += '}\n'
    file.write(result)

DesFile = open("/home/vlu1/CrawledData/recruitments.json", "a", encoding="utf-8")
ListFile = CheckTitle("/home/vlu1/CrawledData/vinapharm.com.vn")

for file in ListFile:
    print(file)
    file_name = open(file, encoding="utf-8")
    data = file_name.read()
    file_name.seek(0)
    soup = BeautifulSoup(file_name, features="lxml")

    content = soup.find("div", class_="detail all")
    if content != None:
        pattern = "(.)*/(.)*/...."
        time_post = None
        time_deadline = None
        vacancy = []
        quantity = []
        workplace = None
        # Go through tag p
        for p in content.find_all("p"):
            string = p.text
            if "vị trí" in string.lower():
                vacancy.append(string[string.index(":")+1 : ].strip())
            if "số lượng" in string.lower():
                string = string.strip()
                quantity.append(int(string[string.index(":")+2 : string.index(" ", string.index(":")+2)]))
            if "từ ngày" in string.lower():
                string = string.split(" ")
                lst = []
                for item in string:
                    if re.match(pattern, item):
                        lst.append(item)
                if len(lst) == 2:
                    time_post = lst[0]
                    time_deadline = lst[1]
                elif len(lst) == 1:
                    time_post = lst[0]

        # Go through tag span
        for span in content.find_all("span"):
            string = span.text
            if "vị trí" in string.lower():
                vacancy.append(string[string.index(":")+1 : ].strip())
            if "số lượng" in string.lower() and quantity==[]:
                string = string.strip()
                quantity.append(int(string[string.index(":")+2 : string.index(" ", string.index(":")+2)]))
            if "từ ngày" in string.lower() and time_post==None and time_deadline==None:
                string = string.split(" ")
                lst = []
                for item in string:
                    if re.match(pattern, item):
                        lst.append(item)
                if len(lst) == 2:
                    time_post = lst[0]
                    time_deadline = lst[1]
                elif len(lst) == 1:
                    time_post = lst[0]

        # Go through tag div
        for div in content.find_all("div"):
            string = div.text
            if "vị trí công việc" in string.lower() or "vị trí tuyển dụng" in string.lower():
                vacancy.append(string[string.index(":")+1 : ].strip())
            if "số lượng" in string.lower() and quantity==[]:
                string = string.strip()
                quantity.append(int(string[string.index(":")+2 : string.index(" ", string.index(":")+2)]))
            if "từ ngày" in string.lower() and time_post==None and time_deadline==None:
                string = string.split(" ")
                lst = []
                for item in string:
                    if re.match(pattern, item):
                        lst.append(item)
                if len(lst) == 2:
                    time_post = lst[0]
                    time_deadline = lst[1]
                elif len(lst) == 1:
                    time_post = lst[0]
        requirements = GetRequirements(data, vacancy)

        checker = True
        while checker:
            if len(quantity) < len(vacancy):
                quantity.append(None)
            elif len(requirements) < len(vacancy):
                requirements.append(None)
            else:
                checker = False

        for i in range(len(vacancy)):
            if workplace != None:
                vacancy[i] += workplace
            info ={
                "company_name" : "VINAPHARM",
                "time_post" : time_post,
                "time_deadline" : time_deadline,
                "vacancy" : vacancy[i],
                "quantity" : quantity[i],
                "salary" : None,
                "requirements" : requirements[0]
            }
            DictToJsonFile(info, DesFile)
    else:
        pass
