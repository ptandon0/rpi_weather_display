# rpi_weather_display
Weather Display for Raspberry Pi and Waveshare 7.5" e-Ink Display

Runs on a Raspberry Pi 0W connected to Waveshare 7.5" e-Ink Display; repo includes waveshare test files and driver.

Weather is sourced from OpenWeatherMap [weather](https://openweathermap.org/current) and [forecast](https://openweathermap.org/forecast5) API.
Does not currently have partial refresh with a current time clock, planned for the future.

#### Configuration and Running
Needs a config file conf.ini set up for [configparser](https://docs.python.org/3/library/configparser.html) to read.

Example:

    [WEATHER]
    lat = xxxx
    lon = yyyy
    openWeatherMapToken = zzzz

Run weatherMap.py to generate a current weather report, save output image, and write to waveshare display.
Display is put to sleep (zero power consumption) at the end of script. 

#### Output
Output is an 800x480 pixel black/white image that is written to the e-Ink display.

Example below:

![output](https://github.com/user-attachments/assets/d6c90854-e918-4286-b486-d05668055430)

