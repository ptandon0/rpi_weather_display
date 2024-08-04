import json
import configparser
from datetime import datetime, timedelta
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import sys
import traceback
import logging

libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd7in5_V2

logging.basicConfig(level=logging.DEBUG)

#read configuration
logging.info("Fetching Weather")
conf = configparser.ConfigParser()
conf.read("config.ini")
lat = conf['WEATHER']['lat']
lon = conf['WEATHER']['lon']
wtoken = conf['WEATHER']['openWeatherMapToken']

#get the weather
weather_api_request= f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&exclude=minutely&appid={wtoken}&units=imperial"
forecast_api_request= f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&exclude=minutely&appid={wtoken}&units=imperial"

weather = json.loads(requests.get(weather_api_request).content)
forecast = json.loads(requests.get(forecast_api_request).content)

logging.info("Preparing Image")

#extract current weather data
main = weather["main"]
temp = str(round(main["temp"],1))
tmin = str(round(main["temp_min"],1))
tmax = str(round(main["temp_max"],1))
humidity = str(round(main["humidity"],0)) + "%"
icon = weather["weather"][0]['icon']
cond = weather["weather"][0]["description"].title()
loc = weather["name"]
dt = datetime.fromtimestamp(weather["dt"]).strftime(" %-I:%M %p, %m/%d/%Y")
now = datetime.now()
time_dict = {0:"Night",1:"Night",2:"Night",3:"Night",4:"Night",
             5:"Morning",6:"Morning",7:"Morning",8:"Morning",9:"Morning",10:"Morning",11:"Morning",12:"Afternoon",
             13:"Afternoon",14:"Afternoon",15:"Afternoon",16:"Afternoon",17:"Afternoon",18:"Afternoon",
             19:"Evening",20:"Evening",21:"Evening",22:"Evening",23:"Night"}
welcome_text = "Good "+ time_dict[now.hour] + "!"

#extract forecast data
forecast_list = forecast["list"]
t1 = str(round(forecast_list[0]['main']['temp'],0))
i1 = forecast_list[0]['weather'][0]['icon']
t2 = str(round(forecast_list[1]['main']['temp'],0))
i2 = forecast_list[1]['weather'][0]['icon']
t3 = str(round(forecast_list[2]['main']['temp'],0))
i3 = forecast_list[2]['weather'][0]['icon']

#set up fonts
font12 = ImageFont.truetype('./fonts/Arial Unicode.ttf', 12)
font18 = ImageFont.truetype('./fonts/Arial Unicode.ttf', 18)
font24 = ImageFont.truetype('./fonts/Arial Unicode.ttf', 24)
font48 = ImageFont.truetype('./fonts/Arial Unicode.ttf', 48)
font96 = ImageFont.truetype('./fonts/Arial Unicode.ttf', 96)
font120 = ImageFont.truetype('./fonts/Arial Unicode.ttf', 120)

#establish width and height, fetch images
width = 800
height = 480
degree_sign = u'\N{DEGREE SIGN}'
icon = weather["weather"][0]['icon']
pil_img = Image.open(os.getcwd() +'/pics/'+ icon +'.png').resize((220,220))
day = now.strftime('%a')
date = now.strftime('%-d')
month = now.strftime('%b')

i1_img = Image.open(os.getcwd() +'/pics/'+ i1 +'.png').resize((75,75))
i2_img = Image.open(os.getcwd() +'/pics/'+ i2 +'.png').resize((75,75))
i3_img = Image.open(os.getcwd() +'/pics/'+ i3 +'.png').resize((75,75))


p_w, p_h = pil_img.size

#open blank canvas and paste weather icon images
blank_img = Image.new('1', (width,height), 255)
blank_img.paste(pil_img, box=(int((width-p_w)/2), int((height)/2 )))
blank_img.paste(i1_img, box =(width-200,int(height/4+100)))
blank_img.paste(i2_img, box =(width-200,int(height/4+175)))
blank_img.paste(i3_img, box =(width-200,int(height/4+250)))
pic_img = blank_img.copy()

#write text onto output image
draw_image = ImageDraw.Draw(pic_img)
draw_image.text((width/2,10), welcome_text, anchor="mt",font=font48)
draw_image.text((width/4,48+(96/2)), 'It is currently:', anchor="mm",font=font24)
draw_image.text((width/2+20, height/4), temp + degree_sign, anchor='mm', font=font120)
draw_image.text((width/2, height/4+120/2 + 30), cond, anchor='mm', font=font48)
draw_image.text((width/4-100, height/2), day,anchor='mm',font=font48)
draw_image.text((width/4-100, height/2+ 75), date,anchor='mm',font=font96)
draw_image.text((width/4-100, height/2+ 150), month,anchor='mm',font=font48)
draw_image.text((10, height-40),"Last Updated",anchor='ls', font=font12)
draw_image.text((10, height-10),loc + dt,anchor='ls', font=font24)
draw_image.text((width-200, height/4),"High: ",anchor='ls', font=font24)
draw_image.text((width-140, height/4),tmax+degree_sign,anchor='ls', font=font24)

draw_image.text((width-200, height/4+24),"Low: ",anchor='ls', font=font24)
draw_image.text((width-140, height/4+24),tmin+degree_sign,anchor='ls', font=font24)

draw_image.text((width-200, height/4+48),"Hum: ",anchor='ls', font=font24)
draw_image.text((width-140, height/4+48), humidity,anchor='ls', font=font24)

draw_image.text((width-125, height/4+135),t1+degree_sign,anchor='lm', font=font24)
draw_image.text((width-125, height/4+205),t2+degree_sign,anchor='lm', font=font24)
draw_image.text((width-125, height/4+285),t3+degree_sign,anchor='lm', font=font24)
draw_image.text((width-175, height/4+90),"Next 12h:",anchor='lm', font=font18)

#show the output
pic_img.save("output.png")
logging.info("Saved Image")

