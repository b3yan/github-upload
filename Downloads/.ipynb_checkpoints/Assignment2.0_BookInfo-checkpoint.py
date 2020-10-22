#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pprint
import numpy as np
import pandas as pd
from urllib.parse import urlparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
from lxml import etree
from lxml import html 
from html.parser import HTMLParser


# In[2]:


start_url = "https://www.goodreads.com/book/show/3735293-clean-code"
chrome_path = "D:/Google/Chrome/Application/chromedriver.exe"

browser = webdriver.Chrome(executable_path=chrome_path)
browser.get(start_url)


# In[3]:


# Unit Tests
html = etree.HTML(browser.page_source)
relBook_xpath = '//li[@class="cover"]/a/@href'

book_href = []
book_rel = html.xpath(relBook_xpath)
for index,item in enumerate(book_rel):
    href = book_rel[index]
    book_href.append(href)
print(book_href)


# In[4]:


print(len(book_href))


# In[5]:


# Find the xpath for each feature
book_URL_xpath = "/html/body/div[2]/div[3]/div[1]/div[2]/div[4]/div[1]/div[2]/div[5]/div[3]/div[1]/div[4]/div[2]/a/@href"
book_title_xpath = '//*[@id="bookTitle"]' 
book_ISBN_xpath = "/html/body/div[2]/div[3]/div[1]/div[2]/div[4]/div[1]/div[2]/div[5]/div[3]/div[1]/div[2]/div[2]" 
book_author_xpath = "/html/body/div[2]/div[3]/div[1]/div[2]/div[4]/div[1]/div[2]/div[1]/span[2]/div/a/span"
book_authorURL_xpath = "/html/body/div[2]/div[3]/div[1]/div[2]/div[4]/div[1]/div[2]/div[1]/span[2]/div/a/@href"
book_rating_xpath = "/html/body/div[2]/div[3]/div[1]/div[2]/div[4]/div[1]/div[2]/div[2]/span[2]"
book_ratingCount_xpath = "/html/body/div[2]/div[3]/div[1]/div[2]/div[4]/div[1]/div[2]/div[2]/a[2]"
book_reviewCount_xpath = "/html/body/div[2]/div[3]/div[1]/div[2]/div[4]/div[1]/div[2]/div[2]/a[3]"
book_img_xpath = '//*[@id="coverImage"]/@src'


# In[6]:


# Creat Feature Lists
book_URL_list = []
book_title_list = [] 
book_ISBN_list = []
book_author_list = []
book_authorURL_list = []
book_rating_list = []
book_ratingCount_list = []
book_reviewCount_list = []
book_img_list = []
info_list = []


# In[7]:


book_href_1 = []
for i in book_href:
    # print(i)
    try:
        browser.get(i)
        html = etree.HTML(browser.page_source)
        book_rel_child = html.xpath(relBook_xpath)
        for index,item in enumerate(book_rel_child):
            href = book_rel_child[index]
            book_href_1.append(href)            
    except Exception as e:
        print(e)         
print(book_href_1)


# In[8]:


print(len(book_href_1))


# In[9]:


for i in book_href_1:
    try:
        browser.get(i)
        html = etree.HTML(browser.page_source)
        
        # Get book's URL
        book_URL = html.xpath(book_URL_xpath)   
        info_list.append(book_URL[0])
        book_URL_list.append(book_URL[0])
        
        # Get book's title
        book_title = html.xpath(book_title_xpath)
        info_list.append(book_title[0].text.strip())
        book_title_list.append(book_title[0].text.strip())
        
        # Get book's ISBN
        book_ISBN = html.xpath(book_ISBN_xpath)
        info_list.append(book_ISBN[0].text.strip())
        book_ISBN_list.append(book_ISBN[0].text.strip())
        
        # Get book's author
        book_author = html.xpath(book_author_xpath)
        info_list.append(book_author[0].text.strip())
        book_author_list.append(book_author[0].text.strip())
        
        # Get book's authorURL
        book_authorURL = html.xpath(book_authorURL_xpath)   
        info_list.append(book_authorURL[0])
        book_authorURL_list.append(book_authorURL[0])
        
        # Get book's AverageRating
        book_rating = html.xpath(book_rating_xpath)
        info_list.append(book_rating[0].text.strip())
        book_rating_list.append(book_rating[0].text.strip())

        # Get book's RatingCount
        book_ratingCount = html.xpath(book_ratingCount_xpath)
        info_list.append(book_ratingCount[0].text.strip())
        book_ratingCount_list.append(book_ratingCount[0].text.strip())
        
        # Get Author's ReviewCount
        book_reviewCount = html.xpath(book_reviewCount_xpath)
        info_list.append(book_reviewCount[0].text.strip())
        book_reviewCount_list.append(book_reviewCount[0].text.strip())
        
        # Get Author's Image_url
        book_img = html.xpath(book_img_xpath)
        info_list.append(book_img[0])
        book_img_list.append(book_img[0])
        
    except Exception as e:
        pass
pprint.pprint(info_list)   


# In[11]:


cols = {'book_URL': book_URL_list, 
        'book_title': book_title_list, 
        'book_ISBN': book_ISBN_list, 
        'book_author': book_author_list, 
        'book_authorURL': book_authorURL_list, 
        'book_rating': book_rating_list, 
        'book_ratingCount': book_ratingCount_list, 
        'book_reviewCount': book_reviewCount_list, 
        'book_img': book_img_list}


# In[15]:


print(type(cols))


# In[16]:


import json
json.dumps(cols)


# In[18]:


filename='Book_Info.json'
with open(filename,'w') as file_obj:
    json.dump(cols,file_obj)    


# In[24]:


df = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in cols.items()]))
display(df.shape, df.head(), df.tail(), df.describe())


# In[25]:


# Connect to sqlite3 Database
import sqlite3
conn = sqlite3.connect('D:/ClassMaterial/Self-Study/code/data/Assignment2.0_BookInfo')
print("Opened database successfully")


# In[26]:


# Save BookInfo data into sqlite3 Database
from sqlalchemy import create_engine
from pandas.io import sql

# Engine object setting
engine = create_engine('sqlite:///Assignment2.0_BookInfo.sqlite3')
# Save data into Database
df.to_sql('BookInfo',engine)


# In[ ]:




