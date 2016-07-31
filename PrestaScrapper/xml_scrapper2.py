# -- coding: utf-8 --
import xmltodict
import json
import urllib
import pysftp
from HTMLParser import HTMLParser
import os
import mechanize
import cookielib
import time
import random
########################   BEGIN CONFIGURATION DATA ###################################
all_color_dict={
    "VERMEIL": "BRONČANA",
    "COFFEE": "BOJA KAVE",
    "BLUE": "PLAVA",
    "GOLD": "ZLATNA",
    "BLACK RED": "CRNO CRVENA",
    "NAVY BLUE": "MORNARSKO PLAVA",
    "BLUE-GREEN": "PLAVO ZELENA",
    "WHITE BAMBOO": "BOJA BIJELOG BAMBUSA",
    "YELLOW": "ŽUTA",
    "ROSERED": "BOJA RUŽE",
    "LIGHT RED": "SVJETLO CRVENA",
    "LIGTH BLUE": "SVJETLO PLAVA",
    "BLACK": "CRNA",
    "ARMY GREEN": "ZELENA",
    "CHAMPAGNE": "BIJELA",
    "SILVERY GREY": "SREBRNO SIVA",
    "RED": "CRVENA",
    "D": "",
    "BLUE GRAY": "PLAVO SIVA",
    "GRAY": "SIVA",
    "KHAKI": "KAKI",
    "DEEP BLUE": "PLAVA",
    "PURPLE": "LJUBIČASTA",
    "ROSE RED": "BOJA RUŽE",
    "GREY": "SIVA",
    "CHOCOLATE": "BOJA ČOKOLADE",
    "1": "",
    "3": "",
    "2": "",
    "5": "",
    "4": "",
    "7": "",
    "DARK RED": "TAMNO CRVENA",
    "ORANGE": "NARANČASTA",
    "8": "",
    "BROWN": "SMEĐA",
    "A": "",
    "GOLDEN": "ZLATNA",
    "C": "",
    "B": "",
    "E": "",
    "SAPPHIRE": "BOJA SAFIRA",
    "G": "",
    "F": "",
    "I": "",
    "H": "",
    "K": "",
    "6": "",
    "BLACK + RED": "CRNO CRVENA",
    "L": "",
    "ROSE-RED": "BOJA RUŽE",
    "DARK GRAY": "TAMNO SIVA",
    "9": "",
    "LIGHT GRAY": "SVJETLO SIVA",
    "LIGHT BROWN": "SVJETLO SMEĐA",
    "BEIGE": "BEŽ",
    "W": "",
    "DEEP BROWN": "SMEĐA",
    "WHITE": "BIJELA",
    "SILVERY": "SREBRNA",
    "REDDISH BROWN": "CRVENKASTO SMEĐA",
    "SILVER": "SREBRNA",
    "J": "",
    "GLODEN": "ZLATNA",
    "PINK": "LJUBIČASTA",
    "10": "",
    "12": "",
    "ROSE": "ROZA",
    "ROSEGOLD": "ZLATNO ROZA",
    "DARK BLUE": "TAMNO PLAVA",
    "WHITE + GRAY": "BIJELO SIVA",
    "WOOD": "DRVENA",
    "ROSY": "RUŽIČASTA",
    "LIGHT GREEN": "SVJETLO ZELENA",
    "11": "",
    "GREEN": "ZELENA",
    "LIGHT BLUE": "SVJETLO PLAVA",
    "SILVER GREY": "SREBRNO SIVA",
    "DARK BROWN": "TAMNO SMEĐA",
    "T": ""
    }

########################   END  CONFIGURATION DATA ####################################

def translate_colors(color_list):
    translate_colors=[]
    for c in color_list:
        c_trans=all_color_dict.get(c,0)
        if c_trans:
            c=c_trans
        if c not in translate_colors:
            translate_colors.append(c_trans)
    return translate_colors

def save_file(filename,data):
    f=open(filename,"w")
    f.write(data)
    f.close()
def upload_file(filename,uploadDir,host_conf=[]):

    srv = pysftp.Connection(host=host_conf[0], username=host_conf[1],password=host_conf[2])
    srv.chdir(uploadDir)
    srv.put(filename)
    srv.close()
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def handle_entityref(self, name):
        self.fed.append('&%s;' % name)
    def get_data(self):
        return ''.join(self.fed)

def html_to_text(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()



def save_cats(result,cats_file):
    json_data = json.dumps(result)     
    save_file(cats_file,json_data)

def get_colors(options,colors_list,trans=0):
    if options:
        colors=options.get("COLOR",0)
        if not colors:
            colors=options.get("Color",0)
        if not colors:
            colors=options.get("color",0)
        if not colors:
            colors=options.get("Coulor",0)
        

        if colors:
            for c in colors:
                if c not in  colors_list:
                    if trans:
                        try:
                            c=translate_api("en","hr",c)
                            c=c.upper().strip()

                        except:
                            print "gresk s bojom"
                            print c
                    else:
                        c_trans=all_color_dict.get(c.upper(),0)
                        if c_trans:
                            c=c_trans
                            
                    colors_list.append(c)
                        
                            
def get_colors_dict(options,colors_dict):
    if options:
        colors=options.get("COLOR",0)
        if not colors:
            colors=options.get("Color",0)
        if not colors:
            colors=options.get("color",0)
        if not colors:
            colors=options.get("Coulor",0)
        

        if colors:
            for c in colors:
                
                colors_dict[c.upper()]=""


def remove_duplicates(json_list):
    col=[]
    for c in json_list:
        if c not in col:
            col.append(c)


    json_data = json.dumps(col)
    print json_data
    


def translate_api(source,dest,keyword):
    url = "https://www.googleapis.com/language/translate/v2?q="+keyword+"&target="+dest+"&format=text&source="+source+"&key=AIzaSyCTlpL1qX8kHplM34eqisZAZS-0ng6PNcw"
    f = urllib.urlopen(url)
    trans=f.read()
    pos0=trans.find('"translatedText": "') + len('"translatedText": "')
    pos1=trans.find('"',pos0+1)
    
    trans = trans[pos0:pos1]
    
    return trans

def xml_to_dict(path):

    with open(path) as fd:
        doc = xmltodict.parse(fd.read())
        return doc 

def get_usb_name(name):
    sizes=["64-GB","32-GB","16-GB","8-GB","4-GB","2-GB"]
    types=["2.0","3.0"]
    usb_size=""
    for size in sizes:
        match_flag=1
        for s in size.split("-"):
            if s not in name:
                match_flag=0
        if match_flag:
            usb_size=size.replace("-"," ")
            break
    usb_type=""        
    for t in types:
        if t in name:
            usb_type=t+" "
            break
            
    name="USB "+usb_type +"Stick "+usb_size
    return name 
            
    
    
def get_name(scrap_type,name):
    
    desc=""
    if scrap_type =="CAR-HOLDER":
        name=u"Držač Za Mobitele "
    elif scrap_type =="ALCOHOL-TESTER":
        name=u"Alkohol Tester "    
    elif scrap_type =="USB-FLASH-DRIVE-GB":
        name=get_usb_name(name.upper())
        

    elif scrap_type =="HOOK-HOLDER":
        name=u"Držač Za Stvari "

    elif scrap_type =="CAR-CLOCK":
        name=u"Satovi Za Auto "

    elif scrap_type =="CAR-IPHONE-CHARGER":
        name=u"Punjači Za Iphone | Auto "

    elif scrap_type =="PC-GAMING-HEADPHONE":
        name=u"Slušalice Za PC "
        desc=u"Slušalice za PC odlične za igranje igrica. "
    elif scrap_type =="EARPHONE-MOBILE-PHONE":
        name=u"Slušalice Za Mobitel "
            
    elif scrap_type =="MICRO-USB-OTG":
        name=u"Mikro USB Na OTG Kabel "
        desc=u"""Androd platforma podržava USB OTG funkcionalnost, koja u principu omogućuje spajanje perifernih uređaja na vaš Android putem USB porta. Uz pomoć malog adaptera, koji microUSB pretvara u USB standardne veličine, priključit ćete USB memorijski stick i s njega kopirati, uređivati, otvarati i pokretati datoteke jednako kao na pravom računalu.
                Jednako tako možete priključiti USB tipkovnicu ili miša te ih koristiti ne bi li da se radi o računalu. Moguće je čak priključiti i USB kontroler te ga koristiti za igranje igrica.  Što sve možete priključiti ponajviše ovisi i o tome koliko struje taj uređaj treba za pokretanje pa tako teško da ćete klasični vanjski USB čvrsti disk uspjeti pokrenuti, čisto jer mu treba više no što telefon može dati."""
                
    elif scrap_type =="MICRO-USB-DUALINTERFACES":
        name=u"USB S Dvostrukim Sučeljem / Micro USB/ OTG USB "
        desc=u"""USB stick koji je moguće priključiti na mobilni uređaj, tablet i sl. tj. na uređaje s OTG mogućnosti"""
                
    elif scrap_type =="GALAXY-S5-I9600-CASE":
        name=u"Maska  Za Galaxy S5 i9600"
                            
    elif scrap_type =="GALAXY-S4-I9500":
        name=u"Maska Za Samsung Galaxy S4 i9500"
                
                                        
    elif scrap_type =="GALAXY-S3-I9300":
        name=u"Maska Za Samsung Galaxy S3 i9300"
                                                        
    elif scrap_type =="GALAXY-NOTE-III-N9000":
        name=u"Maska  Za Samsung Galaxy Note III N9000"                                                        
            
    elif scrap_type =="GALAXY-NOTE-II-N7100":
        name=u"Maska  Za Samsung Galaxy Note II N7100"   
                
    elif scrap_type =="IPHONE-6-CASE":
                
        name=name.upper()
        if "6/" in name and "6S/" in name and "PLUS" in name:
             name=u"Maska Za iPhone 6/6S/6S Plus"
        elif "6/" in name and "6S/" in name :
             name=u"Maska Za iPhone 6/6S" 
        elif "6/6S PLUS " in name :
             name=u"Maska Za iPhone 6/6s plus"                
        elif " IPHONE 6 PLUS" in name :
             name=u"Maska Za iPhone 6 Plus"
        else:    
            name=u"Maska Za iPhone 6"
                
    elif scrap_type =="IPHONE-5-CASE":
        name=name.upper()
        if "5/" in name and "5S/" in name and "PLUS" in name:
             name=u"Maska Za iPhone 5/5S/5S Plus"
        elif "5/" in name and "5S/" in name :
             name=u"Maska Za iPhone 5/5S" 
        elif "5/5S PLUS " in name :
             name=u"Maska Za iPhone 5/5s plus"                
        elif " IPHONE 65 PLUS" in name :
             name=u"Maska Za iPhone 5 Plus"
        else:    
            name=u"Maska Za iPhone 5"
                                
    elif scrap_type =="IPHONE-4-CASE":
        name=u"Maska  Za iPhone 4"
                                
    elif scrap_type =="IPHONE-3-CASE":
        name=u"Maska  Za iPhone 3"
                                                
    elif scrap_type =="IPHONE-6S-CASE":
        name=name.upper()
        if "6" in name and "6S" in name and "PLUS" in name:
             name=u"Maska Za iPhone 6/6S/6S Plus"
        elif "6/" in name and "6S" in name :
             name=u"Maska Za iPhone 6/6S"
        else:    
            name=u"Maska Za iPhone 6S"
                                                                
    elif scrap_type =="IPHONE-6S-PLUS-CASE":
        name=name.upper()
        if "6" in name and "6S" in name and "PLUS" in name:
             name=u"Maska Za iPhone 6/6S/6S Plus"
        elif "6/" in name and "6S" in name :
             name=u"Maska Za iPhone 6/6S"
        else:    
            name=u"Maska Za iPhone 6S Plus"
                
                
                                                                            
    elif scrap_type =="SAMSUNG-GALAXY-S6-EDGE":
        name=u"Maska Za Samsung Galaxy S6 Edge"

    elif scrap_type =="SAMSUNG-GALAXY-S7-EDGE":

        name=u"Maska Za Samsung Galaxy S7 Edge"
    
        
    return name,desc
                
    


def scrap(xml,col=0,scrap_type="",translate=1,trans_desc=1,save_flag=1) :
    xml_dict=xml_to_dict(xml)


    result=[]
    colors_dict={}

    if col:
        colors_list =[]
    k=0
    JSON_FILES=[]
    for item in xml_dict["root"]["item"]:
        
        k+=1
        sku=item.get("sku",0)   
        sku=sku+"0"
        weight=item.get("weight",0)   
        Price=float(item.get("Price",0))
        Price=Price+Price*40/100

        url=item.get("url",0)   
        name=item.get("name",0)   
        

        category=item.get("category",0)   
        media=item.get("media",0)   
        options=item.get("options",0)   
        category=item.get("category",0)   
        description=item.get("description",0)   
        description =description.replace("<br />","*#*")
        description=html_to_text(description)
        
        if col==2:
            get_colors_dict(options,colors_dict)
            continue
          
        
        if not col:
            colors_list =[]
        get_colors(options,colors_list)
        
        if col:
            continue
        colors=colors_list

        res={}
        skip_flag=0
        for n in scrap_type.split("-"):
            
            if n not in name.upper():
                
                skip_flag=1
       
        if skip_flag:
            continue
                 
        res["ref"]=sku
        res["en_name"]=name
        desc=""
        en_desc=""
        if translate:
            name=translate_api("en","hr",name)
            
            if  scrap_type =="HDMI-CABLE":
                name=name.decode('utf-8')
                name=name.replace(u"na HDMI Male",u'na HDMI Muški')      
                
            if  scrap_type =="MICRO-USB-CABLE-PHONE":
                name=name.decode('utf-8')
                name=name.replace(u"Original",u'Orginalni').replace(u"original",u'Orginalni')
                name=name.replace(u"Strong ",u'Jaki').replace(u"strong ",u'Jaki')
                name=name.replace(u"Metal  ",u'Metalni').replace(u"metal  ",u'Metalni')
        else:
            name,desc=get_name(scrap_type,name)

             
            
            
                
                
                

        res["name"]=name
        #description=translate_api("en","hr",description)
        

        if trans_desc:
            for d in description.split("*#*"):
                try:
                    desc+=translate_api("en","hr",d) +"<br>"
                    en_desc+=d+"<br>"
                except:
                    desc=""
                    break
            desc=desc.replace("<br><br>","<br>")
            desc=desc.replace("\\n*","")
            desc=desc.replace("\\","")
            en_desc=en_desc.replace("<br><br>","<br>")

        res["desc"]=desc
        res["en_desc"]=en_desc
        res["name"]=name
        res["price"]=Price
        res["quantity"]=10
        res["images"]=media
        res["colors"]=colors
        res["url"]=url
        result.append(res)
        if k %10 ==0 :
            json_data = json.dumps(result)
            json_filename=scrap_type+random_number+str(k)+".json"
            save_file(json_filename,json_data)
            result=[]
            JSON_FILES.append(json_filename)

        
    if col==2:
        
        json_data = json.dumps(colors_dict)
        save_file("colorDict.json",json_data)
        print json_data
    elif col:
        json_data = json.dumps(colors_list)
        print json_data
        if save_flag:
            save_file("boje.json",json_data)
    else:
        json_data = json.dumps(result)
        print json_data
        if save_flag:
            save_file(scrap_type+random_number+".json",json_data)
        return JSON_FILES


scrap_type=["" for x in range(100)]
scrap_type[-1]="None"
scrap_type[0]="CAR-HOLDER"
scrap_type[1]="ALCOHOL-TESTER"
scrap_type[2]="HOOK-HOLDER"
scrap_type[3]="CAR-CLOCK"
scrap_type[4]="CAR-IPHONE-CHARGER"
scrap_type[5]="PC-GAMING-HEADPHONE"
scrap_type[6]="EARPHONE-MOBILE-PHONE"
scrap_type[7]="HDMI-CABLE"
scrap_type[8]="MICRO-USB-OTG"
scrap_type[9]="MICRO-USB-DUALINTERFACES"
scrap_type[10]="MICRO-USB-CABLE-PHONE"
scrap_type[11]="GALAXY-S5-I9600-CASE"
scrap_type[12]="GALAXY-S4-I9500"
scrap_type[13]="GALAXY-S3-I9300"
scrap_type[14]="GALAXY-NOTE-III-N9000"
scrap_type[15]="GALAXY-NOTE-II-N7100"
scrap_type[16]="IPHONE-6-CASE"
scrap_type[17]="IPHONE-5-CASE"
scrap_type[18]="IPHONE-4-CASE"
scrap_type[19]="IPHONE-3-CASE"
scrap_type[20]="IPHONE-6S-CASE" #NEMOJ KORISTIT
scrap_type[21]="IPHONE-6S-PLUS-CASE"  #NEMOJ KORISTIT
scrap_type[22]="SAMSUNG-GALAXY-S6-EDGE"
scrap_type[23]="SAMSUNG-GALAXY-S7-EDGE"
scrap_type[24]="USB-FLASH-DRIVE-GB"

random_number=str(random.randint(1, 1000))


#scrap(xml,col=0,scrap_type="",translate=1,trans_desc=1,save_flag=1)

selectList=[0,1,2,3,4,5,11,12,13,14,15,17,18,19,20,21,22,23]
n=len(selectList)
colors_flag=0
if colors_flag:
    os.system("wget http://www.chinabuye.com/dr_rss/computer.xml")  
    scrap("computer.xml",1,"",0,0,1) 
    os.system("rm computer.xml")
    
    
for scrap_index in selectList:
    scrap_string=scrap_type[scrap_index]
    print "Kalkuliraj za "+str(scrap_string)
    upload_flag_products=1
    insert_flag=1
    cats=[]
    
    if scrap_string=="USB-FLASH-DRIVE-GB":
        print "CASE: USB-FLASH-DRIVE-GB "
        os.system("wget http://www.chinabuye.com/dr_rss/computer.xml")
        JSON_FILES=scrap("computer.xml",0,scrap_string,0,0,1) 
        os.system("rm computer.xml")
        cats=[42]
        
    
    if scrap_string=="CAR-HOLDER":
        print "CASE: CAR-HOLDER "
        os.system("wget http://www.chinabuye.com/dr_rss/car_accessories.xml")
        JSON_FILES=scrap("car_accessories.xml",0,scrap_string,0,0,1) 
        os.system("rm car_accessories.xml")
        cats=[15,18]

    elif scrap_string=="ALCOHOL-TESTER":
        print "CASE: ALCOHOL-TESTER "
        os.system("wget http://www.chinabuye.com/dr_rss/car_accessories.xml")
        JSON_FILES=scrap("car_accessories.xml",0,scrap_string,0,0,1) 
        os.system("rm car_accessories.xml")
        cats=[15,17]

    elif scrap_string=="HOOK-HOLDER":
        print "CASE: HOOK-HOLDER "
        os.system("wget http://www.chinabuye.com/dr_rss/car_accessories.xml")
        JSON_FILES=scrap("car_accessories.xml",0,scrap_string,0,0,1) 
        os.system("rm car_accessories.xml")

    elif scrap_string=="CAR-CLOCK":
        print "CASE: CAR-CLOCK "
        os.system("wget http://www.chinabuye.com/dr_rss/car_accessories.xml")
        JSON_FILES=scrap("car_accessories.xml",0,scrap_string,0,0,1) 
        os.system("rm car_accessories.xml")
        cats=[15,19]

    elif scrap_string=="CAR-IPHONE-CHARGER":
        print "CASE: CAR-IPHONE-CHARGER "
        os.system("wget http://www.chinabuye.com/dr_rss/car_accessories.xml")
        JSON_FILES=scrap("car_accessories.xml",0,scrap_string,0,0,1) 
        os.system("rm car_accessories.xml")
        cats=[15,20,]

    elif scrap_string=="PC-GAMING-HEADPHONE":
        print "CASE: PC-GAMING-HEADPHONE "
        os.system("wget http://www.chinabuye.com/dr_rss/electronics.xml")
        JSON_FILES=scrap("electronics.xml",0,scrap_string,0,0,1) 
        os.system("rm electronics.xml")
        cats=[21,22]
    elif scrap_string=="EARPHONE-MOBILE-PHONE":
        print "CASE: EARPHONE-MOBILE-PHONE "
        os.system("wget http://www.chinabuye.com/dr_rss/electronics.xml")
        JSON_FILES=scrap("electronics.xml",0,scrap_string,0,0,1) 
        os.system("rm electronics.xml")
        cats=[21,23]

    elif scrap_string=="HDMI-CABLE":
        print "CASE: HDMI-CABLE "
        os.system("wget http://www.chinabuye.com/dr_rss/computer.xml")
        JSON_FILES=scrap("computer.xml",0,scrap_string,1,0,1) 
        os.system("rm computer.xml")

    elif scrap_string=="MICRO-USB-OTG":
        print "CASE: MICRO-USB-OTG "
        os.system("wget http://www.chinabuye.com/dr_rss/computer.xml")
        JSON_FILES=scrap("computer.xml",0,scrap_string,0,0,1) 
        os.system("rm computer.xml")

    elif scrap_string=="MICRO-USB-DUALINTERFACES":
        print "CASE: MICRO-USB-DUALINTERFACES "
        os.system("wget http://www.chinabuye.com/dr_rss/computer.xml")
        JSON_FILES=scrap("computer.xml",0,scrap_string,0,0,1) 
        os.system("rm computer.xml")

    elif scrap_string== "MICRO-USB-CABLE-PHONE":
        print "CASE: MICRO-USB-CABLE-PHONE "
        os.system("wget http://www.chinabuye.com/dr_rss/cell_phone.xml")
        JSON_FILES=scrap("cell_phone.xml",0,scrap_string,1,0,1) 
        os.system("rm cell_phone.xml")

    elif scrap_string== "GALAXY-S5-I9600-CASE":
        print "CASE: GALAXY-S5-I9600-CASE "
        os.system("wget http://www.chinabuye.com/dr_rss/cell_phone.xml")
        JSON_FILES=scrap("cell_phone.xml",0,scrap_string,0,0,1) 
        os.system("rm cell_phone.xml")
        cats=[28,29]

    elif scrap_string== "GALAXY-S4-I9500":
        print "CASE: GALAXY-S4-I9500 "
        os.system("wget http://www.chinabuye.com/dr_rss/cell_phone.xml")
        JSON_FILES=scrap("cell_phone.xml",0,scrap_string,0,0,1) 
        os.system("rm cell_phone.xml")
        cats=[28,30]

    elif scrap_string== "GALAXY-S3-I9300":
        print "CASE: GALAXY-S3-I9300 "
        os.system("wget http://www.chinabuye.com/dr_rss/cell_phone.xml")
        JSON_FILES=scrap("cell_phone.xml",0,scrap_string,0,0,1) 
        os.system("rm cell_phone.xml")
        cats=[28,31]

    elif scrap_string== "GALAXY-NOTE-III-N9000":
        print "CASE: GALAXY-NOTE-III-N9000 "
        os.system("wget http://www.chinabuye.com/dr_rss/cell_phone.xml")
        JSON_FILES=scrap("cell_phone.xml",0,scrap_string,0,0,1) 
        os.system("rm cell_phone.xml")
        cats=[28,32]


    elif scrap_string== "GALAXY-NOTE-II-N7100":
        print "CASE: GALAXY-NOTE-II-N7100 "
        os.system("wget http://www.chinabuye.com/dr_rss/cell_phone.xml")
        JSON_FILES=scrap("cell_phone.xml",0,scrap_string,0,0,1) 
        os.system("rm cell_phone.xml")
        cats=[28,33]

    elif scrap_string== "IPHONE-6-CASE":
        print "CASE: IPHONE-6-CASE "
        os.system("wget http://www.chinabuye.com/dr_rss/cell_phone.xml")
        JSON_FILES=scrap("cell_phone.xml",0,scrap_string,0,0,1) 
        os.system("rm cell_phone.xml")
        cats=[28,34]


    elif scrap_string== "IPHONE-5-CASE":

        print "CASE: IPHONE-5-CASE "
        os.system("wget http://www.chinabuye.com/dr_rss/cell_phone.xml")
        JSON_FILES=scrap("cell_phone.xml",0,scrap_string,0,0,1) 
        os.system("rm cell_phone.xml")
        cats=[28,35]

    elif scrap_string== "IPHONE-4-CASE":

        print "CASE: IPHONE-5-CASE "
        os.system("wget http://www.chinabuye.com/dr_rss/cell_phone.xml")
        JSON_FILES=scrap("cell_phone.xml",0,scrap_string,0,0,1) 
        os.system("rm cell_phone.xml")
        cats=[28,36]
        
    elif scrap_string== "IPHONE-3-CASE":

        print "CASE: IPHONE-5-CASE "
        os.system("wget http://www.chinabuye.com/dr_rss/cell_phone.xml")
        JSON_FILES=scrap("cell_phone.xml",0,scrap_string,0,0,1) 
        os.system("rm cell_phone.xml")
        cats=[28,37]
        
    elif scrap_string== "IPHONE-6S-CASE":

        print "CASE: IPHONE-6S-CASE "
        os.system("wget http://www.chinabuye.com/dr_rss/cell_phone.xml")
        JSON_FILES=scrap("cell_phone.xml",0,scrap_string,0,0,1) 
        os.system("rm cell_phone.xml")
        cats=[28,38]   
        
    elif scrap_string== "IPHONE-6S-PLUS-CASE":

        print "CASE: IPHONE-6S-PLUS-CASE "
        os.system("wget http://www.chinabuye.com/dr_rss/cell_phone.xml")
        JSON_FILES=scrap("cell_phone.xml",0,scrap_string,0,0,1) 
        os.system("rm cell_phone.xml")
        cats=[28,41]
        
    elif scrap_string== "SAMSUNG-GALAXY-S6-EDGE":

        print "CASE: SAMSUNG-GALAXY-S6-EDGE "
        os.system("wget http://www.chinabuye.com/dr_rss/cell_phone.xml")
        JSON_FILES=scrap("cell_phone.xml",0,scrap_string,0,0,1) 
        os.system("rm cell_phone.xml")
        cats=[28,40]
        
    elif scrap_string== "SAMSUNG-GALAXY-S7-EDGE":

        print "CASE: SAMSUNG-GALAXY-S7-EDGE "
        os.system("wget http://www.chinabuye.com/dr_rss/cell_phone.xml")
        JSON_FILES=scrap("cell_phone.xml",0,scrap_string,0,0,1) 
        os.system("rm cell_phone.xml")
        cats=[28,41]


    scrap_string=scrap_string+random_number
    if upload_flag_products:

        for json_file in JSON_FILES : 

            upload_file(json_file,"/home/blaz1988/webapps/opremise/modules/addproduct/files",["opremise.com","blaz1988","19881989Blaz3"] )
        
        cats_file=random_number+"cats.json"
        save_cats(cats,cats_file)
        upload_file(cats_file,"/home/blaz1988/webapps/opremise/modules/addproduct/files",["opremise.com","blaz1988","19881989Blaz3"] )
        os.system("rm "+cats_file)

    
    if insert_flag:

        for json_file in JSON_FILES :
            url='http://opremise.com/admin32544vdyg/index.php?controller=AdminModules&token=54e780812e3c3ce8f8a799f43dae020a&configure=addproduct&tab_module=others&module_name=addproduct'
            url+="&proizvodi=1&json_file="+json_file
            url+="&cat_file="+random_number+"cats.json"
            print "url: "+str(url)
            br=mechanize.Browser()
            response=br.open("http://opremise.com/admin32544vdyg/")
            br.select_form(nr=0)
            br.form['email']='blaz1988@gmail.com'
            br.form['passwd']='19881989'
            br.submit()
            response=br.open(url) 
            time.sleep(2*60)

    time.sleep(2*60)
    #if n>1:
        #time.sleep(10*60)

#remove_duplicates(["ZLATO", "SREBRO", "ZELENA", "PLAVA", "PURPURNA BOJA", "PLAVA", "SIVA", "CRNO", "PLAVA", "BIJELA", "\u017dUTA BOJA", "ROZE", "ZELENA", "CRNO", "NARAN\u010dASTA", "PLAVA", "ZELENA", "CRNO", "BIJELA", "SME\u0111", "SIVA", "CRNO", "BE\u017e", "CRNO", "SME\u0111", "SIVA", "BE\u017e", "CRNO", "SME\u0111", "SIVA", "NARAN\u010dASTA", "CRNO", "BIJELA", "CRNO", "BIJELA", "ZELENA", "CRNO", "ROZE", "\u017eUTA BOJA", "CRNO", "BIJELA", "ZELENA", "NARAN\u010dASTA", "CRNO", "PURPURNA BOJA", "LEOPARD", "CRNO", "BIJELA", "ROZE", "PLAVA", "TRANSPARENTAN", "\u017dUTA BOJA", "CRNO", "PLAVA", "CRNO", "BIJELA", "\u017dUTA BOJA", "ZELENA", "CRNO", "PLAVA", "PLAVA", "SREBRO", "BIJELA", "TOPLA BIJELA", "BIJELA", "TOPLA BIJELA", "BIJELA", "TOPLA BIJELA", "BIJELA", "TOPLA BIJELA", "BIJELA", "TOPLA BIJELA", "BIJELA", "TOPLA BIJELA", "PLAVA", "ZELENA", "BIJELA", "CRNO", "TRANSPARENTAN", "CRNO", "BIJELA", "CRNO", "SIVA", "BIJELA", "CRNO", "PLAVA", "ZELENA", "CRNO", "PLAVA", "PLAVA", "CRNO", "SREBRO", "PLAVA", "NARAN\u010dASTA", "SREBRO", "PLAVA", "NARAN\u010dASTA", "\u017dUTA BOJA", "PLAVA", "SREBRO", "CRNO", "PLAVA", "SREBRO", "CRNO", "PLAVA", "SREBRO", "CRNO", "PLAVA", "SREBRO", "PLAVA", "BIJELA", "CRNO", "ZLATAN", "SIVA", "\u017dUTA BOJA", "ZLATAN", "SREBRO", "ZLATAN", "SREBRO", "ZLATAN", "SREBRO", "BE\u017e CRNA", "BLUE BLACK", "SIVA CRNA", "CRVENA CRNA", "\u017dUTA CRNA", "CRNO", "PLAVA", "SREBRNAST", "BIJELA", "PLAVA", "ZELENA", "CRNO", "BIJELA", "PLAVA", "BIJELA"])








"""
sku
weight
Price
url
name
category
media
options
short_description
description
"""
