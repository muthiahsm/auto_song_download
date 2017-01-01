#This program support windows and mac.

#Song storage path for windows platform. if not used leave it empty

win_base_dir="C:\\Users\\muthiah.somasundaram\\songs\\"

# windows temp dir

win_tmp="c:\\temp\\"

#non windows temp dir

nw_tmp="/tmp/"

#Song storage path for mac platform. if not used leave it empty

mac_base_dir="//Users//muthiah//Music//san//"

# Specify the artist filter name. it supports partial match.
# artist_filter="" # this download all the album from the site

artist_filter="Santh"

#specify the chrome driver location path according to the platform

# if using win, leave it blank

win_web_driver_path="C:\\chromedriver_win32\\chromedriver.exe"

# if using mac, leave it blank

mac_web_driver_path="//Users//muthiah//Downloads//chromedriver"

# configure the site url

site_url="http://www.tamilabeat.com/tamilsongs/movies%20a%20to%20z/"

# Parallel song download YES / NO. this improves song download performance by 50%

PT="NO"

# Amazon web services (AWS) access key
s3_storage="NO" # value could be eiter YES / NO
aws_access_key=""
aws_secret_key=""
s3_bucket="asd"