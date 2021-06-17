import subprocess
source_path = input("File path: ")
des_path = input("Destination folder: ")
ind = 0
try:
    file = open(source_path)
    file.seek(0)
    while True:
        line = file.readline()
        if "<loc>" in line:
            url = line.strip()
            url = url.replace("<loc>", "")
            url = url.replace("</loc>", "")
            file_name = url[url.rindex("/")+1 : ]
            try:
                if "." not in file_name:
                    file_name += ".txt"
                if not file_name.isalpha():
                    ind += 1
                    file_name = "file_name" +str(ind)+".txt"
                subprocess.check_output("curl {}>>{}/{}".format(url,des_path, file_name), shell=True)
            except:
               continue
        if line == "":
            break
except FileNotFoundError as err_FileNotFound:
    print("Can not locate the sitemap file")
