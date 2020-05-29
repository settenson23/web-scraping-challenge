import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import time

executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)

###NASA Mars News###
def mars_news(browser):

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    browser.is_element_present_by_css("ul.item_list li.slide")
    
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")

    try:
        slide_element = news_soup.select_one("ul.item_list li.slide")
        slide_element.find("div", class_="content_title")

        news_title = slide_element.find("div", class_="content_title").get_text()

        news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_paragraph

###JPL Mars Space Images - Featured Image###
def featured_image(browser):
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()

    browser.is_element_present_by_text("more info")
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")

    img = image_soup.select_one("figure.lede a img")
    try:
        img_url = img.get("src")
    except AttributeError:
        return None 
 
    img_url = f"https://www.jpl.nasa.gov{img_url}"
    return img_url

###Mars Weather###
def mars_current_weather(browser):
    url = "https://twitter.com/marswxreport?lang=en"
   
    request_twitter = requests.get(url)
    soup_twitter = BeautifulSoup(request_twitter.text, 'html.parser')

    mars_weather_tweets = [p.text for p in soup_twitter.findAll('p', class_='tweet-text')]

    mars_weather = mars_weather_tweets[0]
    return mars_weather

###Mars Facts###
def mars_facts():
    try:
        mars_df = pd.read_html("https://space-facts.com/mars/")[0]
    except BaseException:
        return None
    mars_df.columns=["Description", "Value"]
    return mars_df

###Mars Hemispheres###
def mars_hemispheres(browser):
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        dictionary = {"title": title, "img_url": image_url}
        mars_hemisphere.append(dictionary)
    return mars_hemisphere

def scrape_all():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    img_url = featured_image(browser)
    mars_weather = mars_current_weather(browser)
    facts = mars_facts()
    mars_hemisphere = mars_hemispheres(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "mars_image": img_url,
        "mars_weather": mars_weather,
        "mars_facts": facts,
        "mars_hemispheres": mars_hemisphere,
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape_all())




