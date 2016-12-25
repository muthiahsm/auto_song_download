from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import urllib.request
import sys
import os

album_name=""
album_download_counter=0
#base_dir="C:\\Users\\muthiah.somasundaram\\songs\\"
base_dir="//Users//muthiah//Music//san//"
artist_filter="Santh"
#artist_filter=""
class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"
opener = AppURLopener()

#driver=webdriver.Chrome("C:\\chromedriver_win32\\chromedriver.exe")
driver=webdriver.Chrome("//Users//muthiah//Downloads//chromedriver")
sleep_time_value_sec=3
fan=""

def create_album_file_list():
    file_access = open(base_dir + "album_file", 'w')

    for d in os.listdir(base_dir):
        # print(d)
        file_access.write(d)
        file_access.write("\n")
    file_access.close()

def launch_site():
    create_album_file_list()
    driver.get("http://www.tamilabeat.com/tamilsongs/movies%20a%20to%20z/")
  # driver.get("file:///C:/Users/muthiah.somasundaram/PycharmProjects/study/tamilbeat.html")
def album_index_selector():
    temp_list=[]
    album_selector()
    index_table_loc = driver.find_element_by_id('AutoNumber3')
    for top_list_selector in index_table_loc.find_elements_by_tag_name('a'):

        top_level_text_name = top_list_selector.text
        if len(top_level_text_name) == 5 :
            temp_list.append(top_level_text_name)
    print (temp_list)
    size_of_array=len(temp_list)
    for i in range(len(temp_list)):
        print ("### Now in Index_name: " + temp_list[i])
        text_value=temp_list[i]
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, text_value)))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, text_value)))
        driver.find_element_by_link_text(text_value).click()
        time.sleep(3)
        album_selector()

def album_selector():
    global album_name
    global fan
    album_temp_list=[]
    global album_download_counter
    album_counter = 0
    artist_album_counter = 0
    album_table_loc = driver.find_element_by_id('AutoNumber4')
    print("Adding Album to list wait ...")
    for album_list in album_table_loc.find_elements_by_tag_name('a'):

        album_counter += 1
        if len(album_list.text) != 0:
            album_temp_list.append(album_list.text)
           # print("adding data to array")
    print("cached album taken for processing:")
    print (album_temp_list)
    album_temp_list.sort()
    for ai in range(len(album_temp_list)):

        album_name=album_temp_list[ai]
        an = album_name
        fan = an.split('-')[0]
        if fan not in open(base_dir + "album_file").read():

#            print ("Album match not found in base dir, so proceeding further")
            if len(artist_filter) > 0:

               if (artist_filter in album_name) and ( 'music' not in album_name) :
                    print ("artist's album name: " + album_name)
                    os.mkdir(base_dir + fan)
                    artist_album_counter += 1
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, album_name)))
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, album_name)))
                    driver.find_element_by_link_text(album_name).click()
                    time.sleep(3)
                    album_download_counter += 1
                    song_downloader()
  #             else:
 #                   #print ("No artist album match found")
            else:
                 print("filter length is zero. No Filter. going with all albums")
                 print("album_name: " + album_name)
                 os.mkdir(base_dir + fan)
                 WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, album_name)))
                 WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, album_name)))
                 driver.find_element_by_link_text(album_name).click()
                 album_download_counter += 1
                 song_downloader()
        else:
            print("Album :" + fan + " - match found in the base dir, so skipping to next album")
    print ("Total Album in the Current Index: " ,album_counter)
    print ("Total Filtered Album by Artist in the current Index: ", artist_album_counter)
    print ("Over all total download so far: ",album_download_counter)
def song_downloader():
    global album_name
    global fan
    download_counter=0


    #if not os.path.exists(base_dir + fan):
     #   os.mkdir(base_dir + fan)
   # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, album_name)))
   # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, album_name)))
    try:
        for i in driver.find_elements_by_tag_name('a'):


            atri = i.get_attribute('href')

            if 'mp3' in atri:
                download_counter += 1


                url_last_segment=atri.split('/')[-1]
                fn=url_last_segment.replace("%20","")

                print ("Downloading song #: " , download_counter , fn )
                os.chdir(base_dir + fan)

                #response = opener.retrieve(atri,fn)
                opener.retrieve(atri, fn)
    #    else:
     #       print ("Album already Exist" + fan)

        driver.back()
        time.sleep(2)
    except Exception:
        print ("error " + str(IOError))
        driver.back()
        time.sleep(2)
        pass
#create_album_file_list()
launch_site()
album_index_selector()

