from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import urllib.request
import sys
import os

test line added

album_name=""
base_dir="C:\\Users\\muthiah.somasundaram\\songs\\"
artist_filter="Ilai"
#artist_filter=""
class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"
opener = AppURLopener()

driver=webdriver.Chrome("C:\\chromedriver_win32\\chromedriver.exe")

sleep_time_value_sec=3
fan=""

test line added

def launch_site():
     driver.get("http://www.tamila.com/tamilsongs/movies%20a%20to%20z/")
  #  driver.get("file:///C:/Users/muthiah.somasundaram/PycharmProjects/study/tamil.html")
def album_index_selector():
    temp_list=[]
    index_table_loc = driver.find_element_by_id('AutoNumber3')

    for top_list_selector in index_table_loc.find_elements_by_tag_name('a'):

        top_level_text_name = top_list_selector.text
        if len(top_level_text_name) == 5 :
            temp_list.append(top_level_text_name)
    print (temp_list)
    size_of_array=len(temp_list)
    for i in range(len(temp_list)):
        print (temp_list[i])
        text_value=temp_list[i]
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, text_value)))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, text_value)))
        driver.find_element_by_link_text(text_value).click()
        time.sleep(3)
        album_selector()

def album_selector():
    global album_name
    album_temp_list=[]

    album_counter = 0
    artist_album_counter = 0
    album_table_loc = driver.find_element_by_id('AutoNumber4')
    for album_list in album_table_loc.find_elements_by_tag_name('a'):

        album_counter += 1
        if len(album_list.text) != 0:
            album_temp_list.append(album_list.text)
            print("adding data to array")
    print (album_temp_list)
    album_temp_list.sort()
    for ai in range(len(album_temp_list)):

        album_name=album_temp_list[ai]
        if len(artist_filter) > 0:
           if (artist_filter in album_name) and ( 'music' not in album_name) :
                print ("artist's album name: " + album_name)
                artist_album_counter += 1
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, album_name)))
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, album_name)))
                driver.find_element_by_link_text(album_name).click()
                song_downloader()
           else:
                print ("No artist album match found")
        else:
             print("filter length is zero. No Filter. going with all albums")
             print("album_name: " + album_name)
             WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, album_name)))
             WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, album_name)))
             driver.find_element_by_link_text(album_name).click()
             song_downloader()

    print ("Total Album in the Current Index: " ,album_counter)
    print ("Total Filtered Album by Artist in the current Index: ", artist_album_counter)

def song_downloader():
    global album_name
    download_counter=0
    an=album_name
    fan = an.split('-')[0]

    if not os.path.exists(base_dir + fan):
        os.mkdir(base_dir + fan)
        for i in driver.find_elements_by_tag_name('a'):


            atri = i.get_attribute('href')

            if 'mp3' in atri:
                download_counter += 1


                url_last_segment=atri.split('/')[-1]
                fn=url_last_segment.replace("%20","")

                print ("Downloading song #: " , download_counter , fn )
                os.chdir(base_dir + fan)

                response = opener.retrieve(atri,fn)
    else:
        print ("Album already Exist" + fan)

    driver.back()
    time.sleep(2)


launch_site()
album_index_selector()

