import csv
from bs4 import BeautifulSoup
import html5lib
import requests
import pandas

LIST=[]
URL=[]
Product_Title=[]
Image_Url=[]
Product_Price=[]
Product_Details=[]
count =0

HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

with open('scrapping.csv','r') as t:
    cr=csv.DictReader(t)
    for i in cr:
        l=list(i.values())
        LIST.append(l)
        a=l[2] 
        try:
            if len(l[2])==10:
                a = l[2]
            elif len(l[2])<=10 and len(l[2])==7:
                a ='000'+ l[2]
        except:
            print('Webpage not Available')
        
            
        url ="https://www.amazon."+l[3]+"/dp/"+a
        URL.append(url)
        
    for x in URL:
        r=requests.get(x,headers=HEADERS)
        soup =BeautifulSoup(r.content,'html.parser')
        title=soup.find(id="productTitle")
        try:
            if title != 'none':
                Product_Title.append((title.text).strip())
        except:
            continue
                   
        img = soup.find(id="imgBlkFront")
        try:
            if img != "none":
                Image_Url.append(img.get('src'))
                #print(img.get('src'))
        except:
            pass
            #print("not available")
                
        price = soup.find(class_="a-size-base a-color-price a-color-price")
        try:
            if price!="none":
                Product_Price.append((price.text).strip(''))
                #print(Product_Price)
        except:
            pass
            #print("Not Availabale")

        details=soup.find_all(class_="a-list-item")
        try:
            if details!= "none":
                    Product_Details.append((details.text).strip())
                    #print((details[i].text).strip())
        except:
            pass
    #       print("Not Availabale")  
    
from pandas import DataFrame
data = {
    'Product_Name':Product_Title,'Image_Url':Image_Url,'Products_Price':Product_Price,'Products_Details':Product_Details
}

df = DataFrame(data, columns= ['Product_Name','Image_Url','Products_Price','Products_Details'])
                
df.to_json (r"C:\Users\mahes\job_task100\Json\scrapping.jason")