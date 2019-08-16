# Dependencies
import requests
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs

def init_browser():
    print("init_b")
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# Create soup and browser objects
def setup_browser(url, browser):
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    return soup

def get_facts_info(soup):
    # Get image URL
    downloads = soup.find(class_="downloads")
    downloads_link = downloads.find("li").find("a")
    img_url = downloads_link.get("href")

    # Get hemisphere title
    title = soup.find(class_="content").find(class_="title").text
    
    # Create dict object
    d = {}
    d["title"] = title
    d["img_url"] = img_url
    
    return d

def scrape_info():
    browser = init_browser()

    # Mars news webpage setup
    soup = setup_browser("https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest", browser)
    # Search for the title and paragraph of most recent news
    news_title_div = soup.find(class_="content_title")
    news_title = news_title_div.find('a').text
    news_p = soup.find(class_="article_teaser_body").text

    # Mars images webpage setup
    base_url="https://www.jpl.nasa.gov"
    soup = setup_browser(base_url + "/spaceimages/?search=&category=Mars", browser)
    # Search for current featured image
    featured_image = soup.find(class_="carousel_container")
    featured_image_a = featured_image.find('a')
    featured_image_url = base_url + featured_image_a.get('data-fancybox-href')

    # Mars weather from twitter setup
    soup = setup_browser("https://twitter.com/marswxreport?lang=en", browser)
    # Search for recent weather update
    weather_info = soup.find_all('p', class_="TweetTextSize")
    for post in weather_info:
        if(post.text.startswith("InSight sol")):
            mars_weather = post.text
            break

    # Mars facts using Pandas
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    # Create a dataframe from tables
    facts_df = tables[1]
    facts_df.columns = ["description", "value"]
    facts_df.set_index("description", inplace=True)
    facts_html_string = facts_df.to_html(justify="left")

    # Initialize dict list for images
    hemisphere_image_urls = []
    # Cerebrus setup
    soup = setup_browser("https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced", browser)
    # Get image
    image_dict = get_facts_info(soup)
    # Add to dictionary list
    hemisphere_image_urls.append(image_dict)
    # Schiaparelli setup
    soup = setup_browser("https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced", browser)
    # Get image
    image_dict = get_facts_info(soup)
    # Add to dictionary list
    hemisphere_image_urls.append(image_dict)
    # Syrtis Major setup
    soup = setup_browser("https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced", browser)
    # Get image
    image_dict = get_facts_info(soup)
    # Add to dictionary list
    hemisphere_image_urls.append(image_dict)
    # Valles Marineris setup
    soup = setup_browser("https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced", browser)
    # Get image
    image_dict = get_facts_info(soup)
    # Add to dictionary list
    hemisphere_image_urls.append(image_dict)


    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "facts_html_string": facts_html_string,
        "hemisphere_image_urls": hemisphere_image_urls
    }
    
    # Close the browser
    browser.quit()

    print(mars_data)
    return mars_data
