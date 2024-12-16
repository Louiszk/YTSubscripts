from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

import urllib.parse
import re
import groq_correction as gc

def file_safe_name(filename):
    return urllib.parse.quote(filename, safe='')

def handle_cookie_consent(driver):
    try:
        cookie_button = driver.find_element(
            By.XPATH, "//button[@aria-label='Verwendung von Cookies und anderen Daten zu den beschriebenen Zwecken akzeptieren']")
        if cookie_button:
            cookie_button.click()
            time.sleep(4) 
            print(f"Cookie consent handled")
    except Exception as e:
        print(f"Cookie consent not found or already handled: {e}")

def crawl_url_with_selenium(url):
    try:
        print("Crawling with Selenium...")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        
  
        driver.get(url)
        
        time.sleep(3)  
        handle_cookie_consent(driver)
        
  
        touch_feedback_div = driver.find_element(By.XPATH, "//button[@aria-label= 'Transkript anzeigen']")
        driver.execute_script("arguments[0].click();", touch_feedback_div)
        
        time.sleep(2)

        segments = driver.find_elements(
            By.CSS_SELECTOR, "yt-formatted-string.segment-text.style-scope.ytd-transcript-segment-renderer")
        segment_texts = [segment.text for segment in segments]
        
        driver.quit()
        
        return " ".join(segment_texts)
        
    except Exception as e:
        print(f"An error occurred while crawling the URL: {url}\nError: {e}")
        return None
    

def parse_playlist(url):
 
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get(url)
    
    time.sleep(3)  
    handle_cookie_consent(driver)
    time.sleep(3)
    segments = driver.find_elements(By.XPATH, "//a[@class = 'yt-simple-endpoint style-scope ytd-playlist-panel-video-renderer']")
    segment_hrefs = [
        (segment.find_element(By.ID, 'video-title').get_attribute('title'), segment.get_attribute('href'))
          for segment in segments]
    return segment_hrefs


def correct_extracted_text(text):
    corrected_text = re.sub(r'\[.*?\]', '', text)
    corrected_text = gc.correct_text(corrected_text)
    return corrected_text


if __name__ == "__main__":
    playlist_url = "https://www.youtube.com/watch?v="
    all_videos = parse_playlist(playlist_url)
    
    for videos in all_videos:
        extracted_texts = crawl_url_with_selenium(videos[1])
        if extracted_texts:
            extracted_texts = gc.process_text_in_batches(correct_extracted_text(extracted_texts))
            with open(f"{file_safe_name(videos[0])}.txt", 'w') as f:
                f.write(extracted_texts)
