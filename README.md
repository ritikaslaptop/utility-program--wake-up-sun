# 🌞 wake up, sun!

a sunrise-based alarm utility program that wakes you up with the sun (or just before it)

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)

## [✨] : what it does

wake up naturally with the sunrise! this app fetches the exact sunrise time for your location and lets you set an alarm to wake up right at sunrise or a few minutes before it ; helping you start your day feeling more refreshed and mindful :) 


## [🎯]: key features

- **sunrise tracking**: uses real-time data to find sunrise times for any city
- **customizable wake-up**: choose how many minutes before sunrise to wake up (0-60 minutes)
- **adaptive scheduling**: if the alarm time is in the past, automatically schedules for tomorrow
- **persistent alarms**: your alarm settings are stored in `alarm_time.txt` and remain after closing the app
- **clean ui**: friendly interface with animated sun, pastel colors, and rounded corners
- **dual interface**: use either the gui or command line to set alarms

  ![Image](https://github.com/user-attachments/assets/35be52e8-cad5-4c6f-a639-6cb4d34eff0b)

## [🚀]: how to use

```bash
# clone the repo
git clone https://github.com/yourusername/wakeup-sun.git
cd wakeup-sun

# install dependencies
pip install pillow requests sounddevice numpy pytz

# set up your api key (get one from openweathermap.org)
# edit main.py and replace API_KEY with your key

# run the app
python ui.py
```


1. enter your city name and click "go"
2. app shows you the exact sunrise time for your location
3. use the slider to set how many minutes before sunrise to wake up
4. click "set alarm" to confirm
5. the status message turns red when your alarm is active
6. to cancel, click "delete alarm"

## [🌐]: command line usage

the app can also be used directly from the command line:

```bash
# interactive mode
python main.py

# set a specific alarm time
python main.py --custom 06:30

# additional testing flags
python main.py --debug  # enables detailed output for troubleshooting
python main.py --test   # runs in test mode without actually setting alarms
```


## [🔧]: libraries used

| library | what it does in our app |
|---------|-------------------------|
| **tkinter** | creates the entire graphical user interface |
| **PIL (Pillow)** | handles the animated sun gif and image processing |
| **requests** | makes api calls to openweathermap for sunrise data |
| **sounddevice** | generates and plays the alarm sound |
| **numpy** | creates the sound wave for the alarm beep |
| **threading** | runs the alarm timer in the background |
| **datetime** | handles all time calculations and conversions |
| **os** | manages the alarm time file storage |


## [🧠]: how it works

1. gets your city location
2. calls the openweathermap api to fetch exact sunrise time
3. calculates your preferred wake-up time
4. sets a timer thread to play the alarm sound
5. stores your alarm in a text file so it persists even if you close the app

## [🔮] : future enhancements

- **global timezone support**: currently optimized for indian time zones
- **executable versions**: standalone .exe for windows and equivalent for mac/linux
- **enhanced sounds**: more alarm sound options including nature sounds
- **recurring alarms**: weekday selector (MTWTFSS) to set alarms for specific days
- **expanded app**: system tray integration, snooze function, and multiple alarms
- **security improvements**: better handling of api keys through environment variables
- **sunset features**: add options for sunset alarms
- **mobile versions**: companion apps for android and ios

## [🤝] : contributing

contributions welcome! feel free to submit issues or pull requests.

## [🏢] : acknowledgments

- sunrise data provided by [openweathermap api](https://openweathermap.org/)
