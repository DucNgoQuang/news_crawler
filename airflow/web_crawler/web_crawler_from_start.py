from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from fake_useragent import UserAgent
import undetected_chromedriver as uc
import json
from datetime import datetime
from collections import defaultdict
import dateparser
from datetime import datetime
import sys


current_date = datetime.now().date()

def is_current_date(date_str, date_format):
    parsed_date = dateparser.parse(date_str,settings={"DATE_ORDER": f"{date_format}"})
    if parsed_date:
        return parsed_date.date() == current_date
    return False

class News:
    def __init__(self, link="", title="", content="", date=""):
        self.link = link
        self.title = title
        self.content = content
        self.date = date

    def to_dict(self):
        return {
            "Link": self.link,
            "Title": self.title,
            "Content": self.content,
            "Date": self.date
        }

columns = ["Link" , "Title" , "Content" , "Date"]


MAX_PAGE = 1

def init_driver():
    options = Options()
    ua = UserAgent()
    user_agent = ua.random
    
    options.add_argument(f'--user-agent={user_agent}')
    options.add_argument("start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")


    driver = uc.Chrome(options=options, version_main=131, headless=True)

    return driver

def get_anchorLinks(base_url, MAX_PAGE, anchorLink_XPath , button_XPath ) -> list:
    """
        Return List containing Anchor Links
    """
    driver = init_driver()
    wait = WebDriverWait(driver, 10)
    
    try :
        driver.get(base_url)
        counter = 1 
        links = []
        while True: 
            time.sleep(5)
            print(f'Finding all anchor links in page {counter}')
            anchor_links =  wait.until(EC.presence_of_all_elements_located((By.XPATH, anchorLink_XPath)))
            for anchor_link in anchor_links:
                links.append(anchor_link.get_attribute('href'))
            counter += 1 

            buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, button_XPath)))
            for button in buttons :
                if int(button.text) == counter:      
                    driver.execute_script("""
                        var evt = document.createEvent('MouseEvents');
                        evt.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
                        arguments[0].dispatchEvent(evt);
                    """, button)
                    break
            if counter > MAX_PAGE + 1 : 
                break
        return links
    except Exception as e :
        print(e)
        return links
    finally :
        driver.quit()    


def extract_anchorLink(anchor_link, title_XPath, content_XPath , date_XPath, date_format ) :

    try : 
        driver = init_driver()
        post_data = News()
        time.sleep(5)
        driver.get(anchor_link)
        uploaded_time = driver.find_element(By.XPATH, date_XPath ).text
        news_content = ""
  
        title = driver.find_element(By.XPATH, title_XPath).text

        content_elements = driver.find_elements(By.XPATH , content_XPath)

        uploaded_time = driver.find_element(By.XPATH, date_XPath ).text

        
        for elem in content_elements:
            news_content += elem.text
            #news_content += elem.get_attribute('outerHTML')
            #print(elem.get_attribute('outerHTML'))
        

        post_data.link = anchor_link
        post_data.title = title
        post_data.content = news_content
        post_data.date = uploaded_time

        return post_data
    except Exception as e :
        print(e)
    finally:
        driver.quit()



def extract(base_url, MAX_PAGE, anchorLink_XPath , button_XPath , title_XPath, content_XPath , date_XPath, date_format) :
    
    
    news_dict = defaultdict(lambda : News())
    
    links = get_anchorLinks(base_url,MAX_PAGE, anchorLink_XPath, button_XPath)
    for link in links :
        news = extract_anchorLink(link,title_XPath,content_XPath,date_XPath, date_format)
        if news:
            news_dict[link] = news

    return news_dict


def load_to_json(news_list,json_path):
    try : 
        with open(json_path, 'r' , encoding = 'utf8') as f :
            data = json.load(f)
    except Exception as e : 
        data = []
    finally :
        data  = data + news_list
        with open(json_path, 'w', encoding='utf8') as f:
            json.dump(data, f, indent = 2, ensure_ascii= False)
    
    
    
    
    
def extract_process(MAX_PAGE):
    web_url = []
    web_attribute = []

    crawler_config_path = "../web_crawler/crawler.json"
    output_path = "../../staging/data_" +  str(current_date) +".json"

    
    final_news_list = list()
    
    with open(crawler_config_path) as f :
        config = json.load(f)



    for url,a in config.items():
        web_url.append(url)
        web_attribute.append(a)
    
    for i in range (len(web_url)):
        news_dict =  extract(web_url[i] , MAX_PAGE , web_attribute[i]['AnchorLink'] , web_attribute[i][ "Button"] , web_attribute[i]["Title"],  web_attribute[i]["Content"] , web_attribute[i]["Date"], web_attribute[i]["Date_Format"])
        news_list = [news.to_dict() for news in news_dict.values()]
        final_news_list += news_list
    
    load_to_json(final_news_list, output_path)

if __name__ == '__main__':
    extract_process(100)
    sys.exit()
