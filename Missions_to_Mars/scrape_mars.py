# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd

# Browser
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

# Scrape
def scrape():
    browser = init_browser()
    mars_dict = {}

    ## NASA Mars News
    # URL 
    news_url = 'https://redplanetscience.com/'
    request = requests.get(news_url)
    browser.visit(news_url)
    # HTML parser
    html = browser.html
    soup = bs(html, "html.parser")
    # Scrape title and text from most recent article
    news_title = soup.find_all('div', class_='content_title')[0].text
    news_text = soup.find_all('div', class_ ='article_teaser_body')[0].text

    ## JPL Mars Space Images - Featured Image
    # URL 
    image_url = 'https://spaceimages-mars.com/'
    request = requests.get(image_url)
    browser.visit(image_url)
    # HTML parser
    html = browser.html
    soup = bs(html, "html.parser")
    # Scrape image url
    image_relative_path = soup.find_all('img', class_='headerimage fade-in')[0]["src"]
    featured_image_url = f"{image_url}{image_relative_path}"

    ## Mars Facts
    # URL 
    fact_url = 'https://galaxyfacts-mars.com/'
    request = requests.get(fact_url)
    browser.visit(fact_url)
    html = browser.html
    soup = bs(html, "html.parser")
    # Scrape table data
    mars_data= pd.read_html(fact_url)
    # Create a data frame
    mars_df= mars_data[1]
    mars_df= mars_df.rename(columns={0:"Element",1:"Value"})
    mars_df.set_index("Element",inplace=True)

    mars_html = mars_df.to_html()

    ## Mars Hemispheres
    # URL
    hemis_url = 'https://marshemispheres.com/'
    request = requests.get(hemis_url)
    browser.visit(hemis_url)
    html = browser.html
    soup = bs(html, "html.parser")
    # Scrape 
    all_hemis = soup.find_all('div',class_='item')
    # Iterate through each hemisphere and scrape data
    for hemi in all_hemis:
        # Title
        hemisphere= hemi.find('div', class_='description')
        title = hemisphere.h3.text
        # Go to each hemisphere link
        hemi_link = hemisphere.a['href']
        img_link = (hemis_url + hemi_link)
        
        request = requests.get(img_link)
        browser.visit(img_link)
        
        html = browser.html
        soup = bs(html, "html.parser")
        
        image_full_link = soup.find('li').a['href']
        image_https = f"{hemis_url}{image_full_link}"
        # Create dictionary
        img_dict = {
            'title': title,
            'img_url': image_https
        }
