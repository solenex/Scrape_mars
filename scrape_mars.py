from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
browser = Browser("chrome", **executable_path, headless=True)


def scrape():
 
    mars_data = {}

    # NASA Mars News

    try:
        # URL of source
        news_url = "https://mars.nasa.gov/news/"
        browser.visit(news_url)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        
        # Search for the class containing the article
        article = soup.find("div", class_='list_text')
        news_title = article.find("div", class_="content_title").text
        news_paragraph = article.find("div", class_ ="article_teaser_body").text
        
        # Save in dictionary
        mars_data ["news_title"] = news_title
        mars_data ["news_paragraph"] = news_paragraph



    except:
        print("Could not scrape mars.nasa.gov site")
    
    # JPL Mars Space Images - Featured Image

    try:
        # URL of source
        image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(image_url)
       
        
        # Search for the class containing the image
        # web_image = soup.find("article", class_="carousel_item").attrs.get("style")
        
        browser.click_link_by_partial_text("FULL IMAGE")
        browser.click_link_by_partial_text("more info")
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        lede = soup.find("figure", class_='lede')
        link = lede.a['href']




        # remove parts of the extracted string that are not needed
        image_items = web_image.split("'", 2)
        featured_image_url = 'https://www.jpl.nasa.gov' + image_items[1]
        
        # Save in dictionary
        mars_data ["featured_image_url"] = featured_image_url
    except:
        print("Could not scrape jpl.nasa.gov site")
    
    # Mars Weather

    try:    
        # URL of source
        tweet_url = "https://twitter.com/MarsWxReport"
        browser.visit(tweet_url)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        
        # Search for the class containing the tweet
        tweet_container = soup.find("div", class_="js-tweet-text-container")
        tweet_txt = tweet_container.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
        
        # remove parts of the extracted string that are not needed
        mars_weather = tweet_txt.split('pic.twitter.com', 1)[0]
        
        # Save in dictionary
        mars_data ["mars_weather"] = mars_weather
    except:    
        print("Could not scrape twitter.com site")
        
    # Mars Facts
    
    try:     
        # URL of source
        facts_url = "https://space-facts.com/mars/"
        browser.visit(facts_url)
        
        # Store data into a dataframe
        facts_data = pd.read_html(facts_url)
        mars_data = pd.DataFrame(facts_data[0])
        mars_data = mars_data[['Mars - Earth Comparison', 'Mars']]
        mars_data.columns=['Description', 'Value']
        
        # Convert dataframe to html table
        mars_facts = mars_data.to_html(header = True, index = False)
        mars_facts = mars_facts.replace('class="dataframe"', 'class="blueTable"',1) 
        mars_facts = mars_facts.replace('"text-align: right;"', '"text-align: center;"',1) 
        
        # Save in dictionary
        mars_data ["mars_facts"] = mars_facts
    except:    
        print("Could not scrape space-facts.com site")
           
    # Mars Hemispheres

    try:
        # URL of source
        hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(hemispheres_url)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        hemisphere_image_urls = []
        
        hemi_list = soup.find("div", class_ = "result-list" )
        hemispheres = hemi_list.find_all("div", class_="item")
        
        for hemisphere in hemispheres:
            title = hemisphere.find("h3").text
            title = title.replace("Enhanced", "")
            end_link = hemisphere.find("a")["href"]
            image_link = "https://astrogeology.usgs.gov/" + end_link 
            
            # Follow the link to the full size image
            browser.visit(image_link)
            html = browser.html
            soup=BeautifulSoup(html, "html.parser")
            downloads = soup.find("div", class_="downloads")
            image_url = downloads.find("a")["href"]
            hemisphere_image_urls.append({"title": title, "img_url": image_url}) 
            
        # Save in dictionary
        mars_data ["hemisphere_image_urls"] = hemisphere_image_urls
    except:    
        print("Could not scrape astrogeology.usgs.gov site")
    
    return mars_data
