import os
import time
import threading
import requests
import sounddevice as sd
import numpy as np
from datetime import datetime, timezone, timedelta

#your OpenWeather API key goes here!
API_KEY = "---------------------"

ALARM_FILE = "alarm_time.txt"  #stores the alarm time(s)
alarm_thread = None  #global variable to store alarm thread


def get_sunrise_time(city_name): #fetch sunrise time
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_KEY}"
    response = requests.get(geo_url).json()
    if not response:
        print("error: could not find city.")
        return None
    lat, lon = response[0]["lat"], response[0]["lon"]

    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
    weather_data = requests.get(weather_url).json()

    if "sys" in weather_data:
        sunrise_utc = weather_data["sys"]["sunrise"]
        return datetime.fromtimestamp(sunrise_utc, timezone.utc).astimezone()
    print("error: could not retrieve sunrise time.")
    return None


def generate_beep(frequency=1000, duration=1, sample_rate=44100):
    #generates a beep
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return 0.5 * np.sin(2 * np.pi * frequency * t)


def play_alarm():
    #plays an embedded beep sound
    beep = generate_beep()
    sd.play(beep, samplerate=44100)
    sd.wait()
    delete_alarm()


def save_alarm_time(alarm_time):
    #saves the alarm time to a file
    with open(ALARM_FILE, "w") as f:
        f.write(alarm_time)


def load_alarm_time():
    #loads the alarm time from the file
    if os.path.exists(ALARM_FILE):
        with open(ALARM_FILE, "r") as f:
            return f.read().strip()
    return None


def delete_alarm(): #deletes the alarm,duh
    global alarm_thread

    if os.path.exists(ALARM_FILE):
        os.remove(ALARM_FILE)
    print("alarm cleared.")

    #reset alarm thread
    alarm_thread = None


def schedule_alarm(alarm_time):#schedules the alarm
    global alarm_thread

    #cancel previous alarm (if exists)
    if alarm_thread and alarm_thread.is_alive():
        alarm_thread.cancel()

    now = datetime.now()

    #handle different time formats
    if ":" in alarm_time and len(alarm_time) <= 5:  # Format like "06:30"
        alarm_datetime = datetime.strptime(alarm_time, "%H:%M").replace(
            year=now.year, month=now.month, day=now.day
        )
    else:  #assume it's already a full datetime string
        try:
            alarm_datetime = datetime.strptime(alarm_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            #fallback
            alarm_datetime = datetime.strptime(alarm_time, "%H:%M").replace(
                year=now.year, month=now.month, day=now.day
            )

    if alarm_datetime < now:
        alarm_datetime += timedelta(days=1)
        print("alarm set for tomorrow.")
    else:
        print(f"alarm set for {alarm_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

    save_alarm_time(alarm_datetime.strftime('%Y-%m-%d %H:%M:%S'))

    #create and store the timer thread
    alarm_thread = threading.Timer((alarm_datetime - now).total_seconds(), play_alarm)
    alarm_thread.daemon = True  # Make thread daemon so it doesn't block program exit
    alarm_thread.start()


def check_alarm(): #checks if alarm is set
    alarm_time = load_alarm_time()
    if alarm_time:
        print(f"alarm is set for {alarm_time}")
    else:
        print("no alarm has been set.")


if __name__ == "__main__":
    import argparse
#parsing command line arguments + flags
    parser = argparse.ArgumentParser()
    parser.add_argument("--custom", help="set a custom alarm time (HH:MM)")
    args = parser.parse_args()

    if args.custom:
        schedule_alarm(args.custom)
    else:
        city = input("enter your city name: ").strip()
        sunrise_time = get_sunrise_time(city)

        if sunrise_time:
            try:
                wake_before = int(
                    input("how many minutes before sunrise do you want to wake up? (0 for exact sunrise): "))
                alarm_time = sunrise_time - timedelta(minutes=wake_before)
                formatted_alarm_time = alarm_time.strftime("%H:%M")
                confirm = input(
                    f"set alarm for {wake_before} minutes before sunrise at {formatted_alarm_time}? (y/n): ").strip().lower()

                if confirm == 'y':
                    schedule_alarm(formatted_alarm_time)
                else:
                    custom_time = input("enter custom alarm time (HH:MM): ")
                    schedule_alarm(custom_time)
            except ValueError:
                print("invalid input! please enter a valid number.")