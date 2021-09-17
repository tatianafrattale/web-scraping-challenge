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


