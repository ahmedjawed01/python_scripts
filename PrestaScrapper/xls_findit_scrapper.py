# -- coding: utf-8 --
import xlrd 
import sys 
import cookielib
import json 
import requests
import time
import pysftp
import random
from ftplib import FTP
import os
import mechanize

random_number=str(random.randint(1, 1000))

def save_cats(result,cats_file):
    json_data = json.dumps(result)     
    save_file(cats_file,json_data)

def delete_JSON_FILES(JSON_FILES):
    for json_file in JSON_FILES:
        os.system("rm "+json_file)
def save_file(filename,data):
    f=open(filename,"w")
    f.write(data)
    f.close()



def upload_file(filename,uploadDir,host_conf=[]):


    ftp = FTP(host_conf[0])  
    ftp.login(user=host_conf[1],passwd=host_conf[2])   
    ftp.cwd(uploadDir) 
    ftp.storlines("STOR " + filename, open(filename, 'r'))
    ftp.quit()

def open_file(path,scrap_type) : 
    JSON_FILES=[]
    #Open and read an Excel file 
    book=xlrd.open_workbook(path)
    #print number of sheets 
    #print book.nsheets

    #print sheet names
    #print book.sheet_names()

    #get the first worksheet
    first_sheet = book.sheet_by_index(0)

    
    #print first row of first sheet
    #print first_sheet.row_values(0)

    #print number of row in sheet 
    #print first_sheet.nrows
    n=first_sheet.nrows
    
    # iterate through rows read a row by row

    
    result=[]
    counter=0
    for i in range(1,n):
        
        row=first_sheet.row_values(i)
        ref = row[0]
        if type(ref) ==float : 
            ref=str(int(ref))
        name=row[2]
        proizvodjac=row[1].strip()
        
        desc = row[3].replace("'","").replace('"',"")
        long_desc=row[3] +row[4]
        long_desc=long_desc.replace("'","").replace('"',"")
        active=row[11]
        skupina=row[5].strip()
        kategorija=row[6].strip()
        #price=row[8]
        price=0
        quantity=row[9]
        images=[]
        image1=row[12]
        if image1:
            images.append(image1)
        image2=row[13]
        if image2:
            images.append(image2)
        image3=row[14]
        if image3:
            images.append(image3)
        category=row[6]
        res={}
        
         


        if active !="Da":
            continue
        part=scrap_type.split("-")
  
        if part[0][0] == "1":
            if part[0][1:] not in name.upper():
                continue
        else:
            if part[0] !=proizvodjac  and part[0] !="0":
                continue
            if part[1] !=skupina  and part[1] !="0":
                continue        
            if part[2] !=kategorija and part[2] !="0":
                continue

   
        counter+=1
        
        res["ref"]=ref
        res["name"]=name
        res["desc"]=""
        res["long_desc"]=""
        res["price"]=price
        res["quantity"]=quantity
        res["images"]=images
        result.append(res)
        if counter%3==0:
            json_data = json.dumps(result)
            json_filename=part[0]+random_number+str(counter)+".json"
            save_file(json_filename,json_data)
            result=[]
            JSON_FILES.append(json_filename)

        
        

    
    return JSON_FILES

#FLAGS#################################
upload_flag=1
delete_flag=0
insert_flag=1
#END FLAGS#############################

path="findit.xlsx"
#scrap_type=proizvodjac-skupina-kategorija
#scrap_type="BlackBerry-Telefoni-Pametni_telefoni"
#scrap_type="Xenon-Telefoni-Dual_SIM_telefoni"
scrap_type="1SSD-0-0"
JSON_FILES=open_file(path,scrap_type)
print JSON_FILES


if upload_flag:
    for json_file in JSON_FILES : 

        upload_file(json_file,"public_html/modules/addproduct/files",["findit.hr","computer","O9tYdd54p9"] )

    cats_file=random_number+"cats.json"
    #25 Mobiteli
    #30 Oprema za mobitele
    #26 Pametni mobiteli
    #64 ASUS
    #63 HTC
    #71 Blackberry
    #28 Dual Sim mobiteli
    #69 Xenon
    #70 CUBOT
    #35 Racunalna periferija
    #75 Monitori
    #34 Komponente
    #42 Hard Disk
    #60 SSD
    cats=[34,42,60]
    save_cats(cats,cats_file)
    upload_file(cats_file,"public_html/modules/addproduct/files",["findit.hr","computer","O9tYdd54p9"] )
    os.system("rm "+cats_file)
if insert_flag:

    for json_file in JSON_FILES :
        url='http://findit.hr/admin499sy7gtb/index.php?controller=AdminModules&token=a69858bf2d611f4b469be7fb384700bb&configure=addproduct&tab_module=others&module_name=addproduct'
        url+="&proizvodi=1&json_file="+json_file
        url+="&cat_file="+random_number+"cats.json"
        print "url: "+str(url)
        br=mechanize.Browser()
        response=br.open("http://findit.hr/admin499sy7gtb")
        br.select_form(nr=0)
        br.form['email']='blaz1988@gmail.com'
        br.form['passwd']='19881989'
        br.submit()
        response=br.open(url) 
        time.sleep(2*60)

if delete_flag:
    delete_JSON_FILES(JSON_FILES)

