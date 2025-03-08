from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
import pandas as pd
import time

def google_search(query, num_results=10):
    options = uc.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
    
    driver = uc.Chrome(options=options)
    driver.get("https://www.google.com/")
    
    
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.tF2Cxc")))
    except:
        print("No results found or page took too long to load.")
        driver.quit()
        return
    
    
    if "our systems have detected unusual traffic" in driver.page_source:
        input("Captcha detected! Please solve it manually and press Enter to continue...")
    
    
    results = []
    search_results = driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc")[:num_results]
    
    for result in search_results:
        try:
            title = result.find_element(By.TAG_NAME, "h3").text
            link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
            description = result.find_element(By.CSS_SELECTOR, "div.VwiC3b").text
            results.append({"Title": title, "Link": link, "Description": description})
        except:
            continue  
    
    
    driver.quit()
    
    
    if results:
        df = pd.DataFrame(results)
        df.to_excel("google_search_results.xlsx", index=False)
        print("Search results saved to 'google_search_results.xlsx'")
    else:
        print("No results found. Try changing the query or increasing wait time.")
    

google_search("President")
