#!/usr/bin/env python
# coding: utf-8

# # Random header Generator

# In[46]:


from bs4 import BeautifulSoup as bs
import random
import requests as rq

USER_AGENT_SCRAPER_BASE_URL = 'http://www.useragentstring.com/pages/useragentstring.php?name='
POPULAR_BROWSERS = ['Chrome', 'Firefox', 'Mozilla', 'Safari', 'Opera', 'Opera Mini', 'Edge', 'Internet Explorer']

def get_user_agent_strings_for_this_browser(browser):
    url = USER_AGENT_SCRAPER_BASE_URL + browser
    response = rq.get(url)
    soup = bs(response.content, 'html.parser')
    user_agent_links = soup.find('div', {'id': 'liste'}).findAll('a')[:20]
    return [str(user_agent.text) for user_agent in user_agent_links]


def get_user_agents():
    user_agents = []
    for browser in POPULAR_BROWSERS:
        user_agents.extend(get_user_agent_strings_for_this_browser(browser))
    return user_agents[3:] # Remove the first 3 Google Header texts from Chrome's user agents

proxy_user_agents = get_user_agents()
# To randomly select an User-Agent from the collected user-agent strings
random_user_agent = random.choice(proxy_user_agents)
random_user_agent


# # Final

# In[2]:


from ast import literal_eval
from bs4 import BeautifulSoup as bs
from IPython.display import clear_output
import pandas as pd, requests as rq, time, os, sys, logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
chrome_options = Options()
# incognito window
chrome_options.add_argument("--incognito")
# Disable Images
chrome_prefs = {}
chrome_options.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
driver.maximize_window()
driver.get("https://www.brilliance.com/user/login")
total_products = 177780
all_data = []
list_data =[]
for i in range(1,int(total_products/48)):
    clear_output(wait=True)
    print(f"{i}/{int(total_products/48)}")
    resutl = driver.execute_script("""async function send(page_count) {
      try {
        const url = "https://worker.brilliance.com/api/v1/lab-grown-diamond-search";
        const data = {
          "data": {
            "imgOnly": true,
            "view": "grid",
            "priceMin": 150,
            "priceMax": 200000,
            "caratMin": 0.25,
            "caratMax": 12,
            "cutMin": 0,
            "cutMax": 4,
            "colorMin": 0,
            "colorMax": 9,
            "clarityMin": 0,
            "clarityMax": 9,
            "depthMin": 0,
            "depthMax": 100,
            "tableMin": 0,
            "tableMax": 93,
            "shapeList": ["0", "2", "6", "5", "3", "1", "7", "8", "4", "9"],
            "certificateList": [],
            "sort": 0,
            "polish": [],
            "symmetry": [],
            "fluor": [],
            "sort_order": null,
            "pager": page_count
          }
        };
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(data)
        });
        if (response.ok) {
          const result = await response.json();
          //console.log(result);
          return result
        } else {
          console.error("POST request failed");
        }
      } catch (error) {
        console.error("Error:", error);
      }
    }return send(%s)""" %i)
    list_data.extend(resutl['diamond'])
    all_data.append(resutl)
    time.sleep(10)
final_data = []
for data in list_data:
    url     = "https://www.brilliance.com/" + data['alias']
    image_id = data['reportNumber']
    image_url = f'https://cdn.diamonds/cdn-cgi/image/width=720,height=720,fit=pad,quality=100/images_legacy/{image_id}'
    title = data['carat'] + " "  + 'Carat'+ " " + data['shape'] + " "+ "Loose Diamond,"+ " " + data['color'] + ", "+ data['clarity']+ ", " + data['cut']+ ", " + data['report'] + " "+ 'Certification'
    if 'lab-grown-diamonds' in url:
        title = 'Lab Grown Diamond: ' + title
        data['Category'] = 'Lab Grown Diamond'
    data['title'] = title
    data['url'] = url
    data['image_url'] = image_url
    data['SKU'] = data['alias'].split("SKU-")[-1]
    final_data.append(data)


# In[ ]:




