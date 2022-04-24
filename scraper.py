from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 
import pandas as pd
from datetime import datetime

YOUTUBE_TRENDING = "https://www.youtube.com/feed/trending"

def get_driver():
    ser =  Service("/usr/bin/chromedriver")
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/google-chrome"
    options.headless = True
    driver = webdriver.Chrome(service=ser,options=options)
    return driver

def get_videos(driver):
    driver.get(YOUTUBE_TRENDING)
    video_div = driver.find_elements(By.TAG_NAME,value="ytd-video-renderer")
    return video_div

def parse_video(video):

    title_tag = video.find_element(by=By.ID,value="video-title")
    title_text = title_tag.text
    url = title_tag.get_attribute("href")

    thumbnail_tag = video.find_element(by=By.ID,value="img")
    thumbnail_url = thumbnail_tag.get_attribute("src")

    channel_tag = video.find_element(by=By.CSS_SELECTOR,value="#text-container a")
    channel_name = channel_tag.text

    metadata_tag =  video.find_elements(by=By.CSS_SELECTOR,value="#metadata-line span")
    views = metadata_tag[0].text
    upload_date = metadata_tag[1].text

    desc_tag = video.find_element(by=By.ID,value="description-text")
    description = desc_tag.text

    return {
        "title" : title_text,
        "url" : url,
        "thumbnail" : thumbnail_url,
        "channel" : channel_name,
        "views" : views,
        "upload-date" : upload_date,
        "description" : description
    }

def write_to_csv(data):

    file_name = "data/data1.csv"
    df = pd.DataFrame(data)
    df.to_csv(file_name)

if __name__ == "__main__" :
    driver = get_driver()
    videos = get_videos(driver)
    videos_data = [parse_video(video) for video in videos[:10]]
    print("writing data")
    write_to_csv(videos_data)
    driver.close()

     






