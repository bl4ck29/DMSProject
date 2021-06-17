import json, pymongo
file = open("/home/vlu1/CrawledData/recruitments.json", encoding="utf-8")
file.seek(0)
connection = pymongo.MongoClient("mongodb://10.86.94.2:27017")
dbTeam1DGC = connection["team1DGC"]
colRecruitments = dbTeam1DGC["recruitments"]
while True:
    line = file.readline()
    if line=="":
        break
    line = json.loads(line)
    colRecruitments.insert_one(line)