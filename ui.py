import os
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk, ImageSequence
import threading
from datetime import datetime, timedelta

#import functions from main.py
from main import get_sunrise_time, schedule_alarm, load_alarm_time, delete_alarm

#colors :))
PASTEL_BLUE = "#A6D1E6"
PASTEL_YELLOW = "#FFF3B0"
ACCENT_BLUE = "#7F9EAD"
WHITE = "#FFFFFF"
TEXT_COLOR = "#333333"
ALARM_SET_COLOR = "#FF0000"


class SunriseAlarmUI:
    def __init__(self, root):
        self.root = root
        self.root.title("wake up,sun!")
        # Optimized for phone-like screen size
        self.root.geometry("385x600")
        self.root.configure(bg=PASTEL_BLUE)

                                        #status message variable
        self.status_var = tk.StringVar()
        self.status_var.set("all checks complete, good to go!")

                                #sunrise time variable
        self.sunrise_time = None

                                                       #main container
        main_container = tk.Frame(root, bg=PASTEL_BLUE)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

                                                                         #sun icon header - rounded edges
        header_frame = tk.Frame(main_container, bg=PASTEL_YELLOW, pady=10,
                                highlightbackground=ACCENT_BLUE, highlightthickness=1)
        header_frame.pack(fill="x", pady=(0, 10))

                                                                           #rounded corners
        self._create_rounded_corners(header_frame, PASTEL_YELLOW, 10)

        #sun GIF
        try:

            self.gif_frames = []
            self.current_frame = 0
            gif = Image.open("giphy.gif")

            for frame in ImageSequence.Iterator(gif):
                frame = frame.resize((100, 100), Image.LANCZOS)
                photoframe = ImageTk.PhotoImage(frame)
                self.gif_frames.append(photoframe)

            #animation thingies
            self.sun_label = tk.Label(header_frame, image=self.gif_frames[0], bg=PASTEL_YELLOW)
            self.sun_label.pack()


            self.animate_gif()
        except Exception as e:
            #fallback to sun emoji if GIF loading fails
            self.sun_label = tk.Label(header_frame, text="☀️", font=("Arial", 48), bg=PASTEL_YELLOW, fg="orange")
            self.sun_label.pack()

        #title
        tk.Label(header_frame, text="wakeup,sun!", font=("Arial", 18, "bold"),
                 bg=PASTEL_YELLOW, fg=TEXT_COLOR).pack()


        content_frame = tk.Frame(main_container, bg=WHITE, bd=0, padx=15, pady=15,
                                 highlightbackground=ACCENT_BLUE, highlightthickness=1)
        content_frame.pack(fill="both", expand=True)

        #rounded corners
        self._create_rounded_corners(content_frame, WHITE, 10)

        canvas = tk.Canvas(content_frame, bg=WHITE, highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=WHITE)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        #city input frame
        city_frame = tk.Frame(scrollable_frame, bg=WHITE)
        city_frame.pack(fill="x", pady=(0, 15))

        tk.Label(city_frame, text="you live in...:", font=("Arial", 12, "bold"),
                 bg=WHITE, fg=TEXT_COLOR).pack(side="left")
        self.city_entry = tk.Entry(city_frame, font=("Arial", 12), width=15)
        self.city_entry.pack(side="left", padx=10, fill="x", expand=True)

        #rounded corners
        self.get_btn = tk.Button(city_frame, text="go", bg=ACCENT_BLUE, fg=WHITE,
                                 font=("Arial", 10, "bold"), command=self.get_sunrise,
                                 relief=tk.FLAT, padx=10, pady=3)
        self.get_btn.pack(side="right")
        self._make_button_rounded(self.get_btn)

        #sunrise info
        self.sunrise_info = tk.Label(scrollable_frame,
                                     text="enter your location to get sunrise time",
                                     font=("Arial", 11), bg=WHITE, fg=TEXT_COLOR,
                                     wraplength=300)
        self.sunrise_info.pack(fill="x", pady=(0, 10))

                                        #slider! (minutes before sunrise)
        tk.Label(scrollable_frame, text="(optional) wake me up before the sunrise?",
                 font=("Arial", 12, "bold"), bg=WHITE, fg=TEXT_COLOR).pack(anchor="w")

        slider_frame = tk.Frame(scrollable_frame, bg=WHITE)
        slider_frame.pack(fill="x", pady=(5, 15))

        #configure slider
        style = ttk.Style()
        style.configure("TScale", background=WHITE)

        self.minutes_var = tk.IntVar(value=15)
        self.minutes_slider = ttk.Scale(slider_frame, from_=0, to=60, orient="horizontal",
                                        variable=self.minutes_var, command=self.update_minutes_display)
        self.minutes_slider.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.minutes_display = tk.Label(slider_frame, text="15 min", width=6,
                                        font=("Arial", 11), bg=WHITE)
        self.minutes_display.pack(side="right")

        #button frame
        btn_frame = tk.Frame(scrollable_frame, bg=WHITE)
        btn_frame.pack(fill="x", pady=(5, 10))

        #set alarm button
        self.sunrise_btn = tk.Button(btn_frame, text="set alarm",
                                     bg=ACCENT_BLUE, fg=WHITE,
                                     font=("Arial", 11, "bold"),
                                     command=self.set_sunrise_alarm,
                                     state="disabled", padx=10, pady=5, relief=tk.FLAT)
        self.sunrise_btn.pack(fill="x", pady=(0, 5))
        self._make_button_rounded(self.sunrise_btn)

        #delete alarm button
        self.delete_btn = tk.Button(btn_frame, text="delete alarm", bg=PASTEL_BLUE, fg=TEXT_COLOR,
                                    font=("Arial", 11, "bold"), command=self.delete_alarm,
                                    padx=10, pady=5, relief=tk.FLAT)
        self.delete_btn.pack(fill="x", pady=(5, 0))
        self._make_button_rounded(self.delete_btn)

        #status bar(one of my fave things)
        status_frame = tk.Frame(main_container, bg=PASTEL_YELLOW,
                                highlightbackground=ACCENT_BLUE, highlightthickness=1)
        status_frame.pack(fill="x", pady=(10, 0))

        #round round round
        self._create_rounded_corners(status_frame, PASTEL_YELLOW, 10)

        self.status = tk.Label(status_frame, textvariable=self.status_var,
                               font=("Arial", 10), bg=PASTEL_YELLOW, fg=TEXT_COLOR,
                               pady=5)
        self.status.pack(fill="x")

        #existing alarm check
        self.check_existing_alarm()

    def _create_rounded_corners(self, widget, bg_color, radius):
        #rounded corners 4 a frame
        radius = radius

        def _create_circle(canvas, x, y, r, **kwargs):
            return canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)

        def _create_polygon(canvas, x, y, r, **kwargs):
            points = [
                x - r, y,
                x, y - r,
                x + r, y,
                x, y + r,
            ]
            return canvas.create_polygon(points, **kwargs)

        width = widget.winfo_reqwidth()
        height = widget.winfo_reqheight()

        #width and height are initialisation
        if width == 1 and height == 1:
            widget.update_idletasks()
            width = widget.winfo_reqwidth()
            height = widget.winfo_reqheight()

        canvas = tk.Canvas(widget, width=width, height=height, bg=bg_color,
                           highlightthickness=0)
        canvas.place(x=0, y=0, relwidth=1, relheight=1)

        #widget raise
        widget.lift()

    def _make_button_rounded(self, button):
        #add styling to make buttons appear rounded
        button.config(relief=tk.FLAT, borderwidth=0)
        button.bind("<Enter>", lambda e: button.config(relief=tk.FLAT, borderwidth=0))
        button.bind("<Leave>", lambda e: button.config(relief=tk.FLAT, borderwidth=0))

    def animate_gif(self):
        self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
        self.sun_label.config(image=self.gif_frames[self.current_frame])

        self.root.after(100, self.animate_gif)

    def update_minutes_display(self, value):
        #round off the slider to nearest 5
        minutes = round(float(value) / 5) * 5
        self.minutes_var.set(minutes)
        self.minutes_display.config(text=f"{minutes} min")

    def get_sunrise(self):
        #get sunrise time using API from main.py
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showerror("Error", "Please enter a location name")
            return

        #status while fetching
        self.status_var.set("fetching sunrise time...")
        self.root.update()

        #thread for API call to avoid freezing the UI
        def fetch_sunrise():
            try:
                self.sunrise_time = get_sunrise_time(city)

                if self.sunrise_time:
                    #format sunrise time for display
                    formatted_time = self.sunrise_time.strftime("%H:%M")

                    #update UI from main thread
                    self.root.after(0, lambda: self.sunrise_info.config(
                        text=f"the sun rises at {formatted_time} in {city}"))
                    self.root.after(0, lambda: self.status_var.set(
                        f"fetched sunrise: {formatted_time}"))
                    self.root.after(0, lambda: self.sunrise_btn.config(state="normal"))
                else:
                    self.root.after(0, lambda: messagebox.showerror(
                        "error", "could not get sunrise data for this location"))
                    self.root.after(0, lambda: self.status_var.set("Failed to get sunrise data"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Error: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("Failed to get sunrise data"))

        #start the thread
        threading.Thread(target=fetch_sunrise, daemon=True).start()

    def set_sunrise_alarm(self):
        #set alarm based on sunrise time
        if not self.sunrise_time:
            messagebox.showerror("Error", "no sunrise time available")
            return

        minutes_before = self.minutes_var.get()

        #calculate alarm time based on sunrise and minutes before
        alarm_time = self.sunrise_time - timedelta(minutes=minutes_before)
        formatted_alarm_time = alarm_time.strftime("%H:%M")

        if messagebox.askyesno("confirm",
                               f"set alarm for {minutes_before} minutes before sunrise at {formatted_alarm_time}?"):
            try:
                #schedule the alarm using the function from main.py
                schedule_alarm(formatted_alarm_time)

                #update UI
                self.status.config(fg=ALARM_SET_COLOR)
                self.status_var.set(f"alarm set! you'll wake up at {formatted_alarm_time}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to set alarm: {str(e)}")

    def delete_alarm(self):
        #elete the alarm using function from main.py
        try:
            #call the delete_alarm function from main.py
            delete_alarm()

            #reset status message color
            self.status.config(fg=TEXT_COLOR)
            self.status_var.set("alarm cleared")
        except Exception as e:
            messagebox.showerror("Error", f"failed to delete alarm: {str(e)}")

    def check_existing_alarm(self):
        #check if there's an existing alarm set
        alarm_time = load_alarm_time()
        if alarm_time:
            self.status.config(fg=ALARM_SET_COLOR)
            self.status_var.set(f"alarm is set for {alarm_time} already")


#run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SunriseAlarmUI(root)
    root.mainloop()