#import libraries
from selenium import webdriver
from bs4 import BeautifulSoup

## scrape page to read possible information in it
### scrape paragrapg
def scrap_paragraph(link):

    '''    function to read paragraph in page
           input: url of page
           output: paragraph  '''
    
    url = link
    driver = webdriver.Chrome()
    driver.get(url)
    page_source = driver.page_source
    driver.quit()
    soup = BeautifulSoup(page_source,features="html.parser")
    l=soup.find_all('p',attrs={'class':"body-1 paragraph"})
    text=''
    for l_ in l:
        text=text+(l_.text)
    return text

### scrape pages 
def scrape_page(text,page_num):
    
    '''   function to scrape page
          input: link of page
          output: list of dictionaries each dictionary contain information about one news 
          information scraped: title,desription,section,link of news,image,paragraph of news
    '''
    
    url=f'https://www.alarabiya.net/{text}/archive?pageNo={i}'
    driver = webdriver.Chrome()
    driver.get(url)
    page_source = driver.page_source
    driver.quit()
    soup = BeautifulSoup(page_source,features="html.parser")
    body_news=soup.find_all('li',attrs={'class':"latest_element"})
    for body_new in body_news:
        new={}
        src=body_new.find('img')['src']
        title=((body_new.select('.latest_content'))[0].find('h4').text).replace('\n','').replace('\xa0','').strip()
        link='https://www.alarabiya.net'+(body_new.select('.latest_content'))[0].find('a')['href']
        section=(body_new.select('.latest_section'))[0].find('a')['title']
        descrition=(body_new.select('.latest_description'))[0].text

        new['title']=title
        new['descrition']=descrition
        new['section']=section
        new['link']=link
        new['image']=src
        new['article']=scrap_paragraph(link)
        news.append(new)
        
   
### get news
''' loop for each branch in AL-ARABIA page 
    for each branch loop for all pages in it'''

news=[]
dic={'arab-and-world/syria':1000,'arab-and-world/gulf':468,'arab-and-world/yemen':1000,'north-africa':1000,'arab-and-world/egypt':1000,'arab-and-world/american-elections-2016':1000,'iran':1000,'arab-and-world/iraq':1000,'coronavirus':475,'sport':1000,'politics':1000,'sport/views':764,'saudi-today':1000}
for text,num in dic.items():
    max_page=num
    print(text)
    for i in range(1,max_page+1):
        print(i)
        scrape_page(text,i)

#print(len(news))
# ensure that they are 117000

# save news to csv file
import pandas as pd
df=pd.DataFrame(news)
df.to_csv('Al-Arabia_news.csv',encoding = 'utf-8-sig',index=False)


# save news to json file
import json
with open('Al-Arabia_news.json', 'w', encoding='utf-8') as json_file:
    json.dump(news, json_file, ensure_ascii=False, indent=1)