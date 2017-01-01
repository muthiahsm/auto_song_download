from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import urllib.request
import threading
import sys
import os
import config as cfg
import boto3 as aws


album_name=""
fan=""
album_download_counter=0
sleep_time_value_sec=3
thread_list=[]
st=""
et=""
s3 = aws.resource('s3')

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"
opener = AppURLopener()

if os.name == "posix":
    driver_path=cfg.mac_web_driver_path
    base_dir=cfg.mac_base_dir
    tmp=cfg.nw_tmp
else:
    driver_path = cfg.win_web_driver_path
    base_dir = cfg.win_base_dir
    tmp=cfg.win_tmp
if cfg.s3_storage == "YES" :
    base_dir=cfg.nw_tmp
    base_bucket=cfg.s3_bucket
artist_filter=cfg.artist_filter

# s3 = aws.client(
#     's3',
#     aws_access_key_id=cfg.aws_access_key,
#     aws_secret_access_key=cfg.aws_secret_key
# )

driver=webdriver.Chrome(driver_path)

def s3_list():

    s3_file_access = open(base_dir + "album_file", 'w')
    print("creating s3 album list")
    for folder_path in s3.Bucket(base_bucket).objects.all():
        folder='/'.join(folder_path.key.split('/')[0:-1])
        print(folder)
        s3_file_access.write(folder)
        s3_file_access.write("\n")
    s3_file_access.close()

def create_album_file_list():

    if cfg.s3_storage != "YES" :
        file_access = open(base_dir + "album_file", 'w')

        for d in os.listdir(base_dir):
            # print(d)
            file_access.write(d)
            file_access.write("\n")

        file_access.close()
    else :
        s3_list()

def launch_site():

    create_album_file_list()
    driver.get(cfg.site_url)

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
        time.sleep(sleep_time_value_sec)
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
                    create_dir(base_dir, fan)
                    #os.mkdir(base_dir + fan)
                    artist_album_counter += 1
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, album_name)))
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, album_name)))
                    driver.find_element_by_link_text(album_name).click()
                    time.sleep(sleep_time_value_sec)
                    album_download_counter += 1
                    song_downloader()
            else:
                 print("filter length is zero. No Filter. going with all albums")
                 print("album_name: " + album_name)
                 #os.mkdir(base_dir + fan)
                 create_dir(base_dir,fan)
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

def create_dir(base_dir, fan):
    if cfg.s3_storage != "YES" :
        if not os.path.exists(base_dir + fan):

            print("creating the album directory ...")
            os.mkdir(base_dir + fan)


def song_downloader():

    global album_name
    global fan
    download_counter=0
    global thread_list
    global st
    global et

    try:
        st = time.time()
        #print ("print start time :" , st)
        for i in driver.find_elements_by_tag_name('a'):


            atri = i.get_attribute('href')

            if 'mp3' in atri:
                download_counter += 1
                url_last_segment=atri.split('/')[-1]
                fn=url_last_segment.replace("%20","")
                print ("Downloading song #: " , download_counter , fn )
                if cfg.s3_storage != "YES":
                    fun_local_disk_storage(atri, base_dir, fan, fn)
                else:
                    fun_s3_storage(atri, base_bucket, fan, fn)
        #print(cfg.PT)

        if cfg.PT == "YES" :
            #print("inside 5")
           # print(thread_list)
            st = time.time()
            for x in thread_list:
                #print(x)
                x.start()
            for x in thread_list:
                print("in x join loop")
                x.join()
                jt=time.time() - st
                print(jt)
            et = time.time() - st
            print("total time took to download the album: ", et)
        else:
     #       print ("Album already Exist" + fan)
         #   print("outside PT final if")
            et = time.time() - st
            print ("total time took to download the album: ", et)

        driver.back()
        time.sleep(sleep_time_value_sec)

    except Exception:
        print ("error " + str(IOError))
        driver.back()
        time.sleep(sleep_time_value_sec)
        pass

def fun_parallel(atri, base_bucket, fan, fn):

    if cfg.s3_storage != "YES":

        opener.retrieve(atri, fn)
    else:

        with opener.open(atri) as data:
            print("storing data in s3")
            s3.meta.client.upload_fileobj(data, base_bucket, fan + '/' + fn)

def fun_local_disk_storage(atri, base_dir, fan, fn):

    global thread_list
   # global st
   # global et

    os.chdir(base_dir + fan)
    if cfg.PT != "YES":
        # response = opener.retrieve(atri,fn)
        npst = time.time()
        opener.retrieve(atri, fn)
        npt = time.time() - npst
        print("completed song download in sec", npt)
    else:
        # print("in thread add loop")
        t = threading.Thread(target=fun_parallel, args=(atri, base_bucket, fan, fn))
        thread_list.append(t)

def fun_s3_storage(atri, base_bucket, fan, fn):

    global thread_list

    if cfg.PT != "YES":

        with opener.open(atri) as data:
            print("storing data in s3")
            s3.meta.client.upload_fileobj(data, base_bucket, fan + '/' + fn)
    else:

        t = threading.Thread(target=fun_parallel, args=(atri, base_bucket, fan, fn))
        thread_list.append(t)
def tearDown():
    print("Browser closed...")
    driver.close()

launch_site()
album_index_selector()
tearDown()
