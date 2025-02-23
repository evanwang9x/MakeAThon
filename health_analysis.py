import tkinter as tk
from tkinter import messagebox
import numpy as np
import time

time.sleep(1)

def force_focus():
    root.focus_force()
    root.lift()

def get_stored_heart_rate():
    try:
        with open('heart_rate_data.txt', 'r') as f:
            return int(f.read())
    except:
        return None

def calculate_health_metrics(heart_rate, gender, height, weight, age):
    if heart_rate == 0:
        return {
            "BMR": 0,
            "Max Heart Rate": 0,
            "Current Zone": "Dead",
            "Calories Burned": 0
        }
    
    if gender.lower() == "male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        max_heart_rate = 220 - age
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        max_heart_rate = 226 - age

    zone0 = max_heart_rate * 0  
    zone1 = max_heart_rate * 0.5  
    zone2 = max_heart_rate * 0.6  
    zone3 = max_heart_rate * 0.7  
    zone4 = max_heart_rate * 0.8  
    zone5 = max_heart_rate * 0.9

    current_zone = "Unknown"
    if heart_rate == zone0:
        current_zone = "Dead"
    elif heart_rate < zone1:
        current_zone = "Rest"
    elif zone1 <= heart_rate < zone2:
        current_zone = "Very Light"
    elif zone2 <= heart_rate < zone3:
        current_zone = "Light"
    elif zone3 <= heart_rate < zone4:
        current_zone = "Moderate"
    elif zone4 <= heart_rate < zone5:
        current_zone = "Hard"
    else:
        current_zone = "Maximum"

    minutes = 0.25  
    calories = (heart_rate * 0.6309 * minutes) / 60

    return {
        "BMR": round(bmr, 2),
        "Max Heart Rate": round(max_heart_rate, 2),
        "Current Zone": current_zone,
        "Calories Burned": round(calories, 2)
    }


def generate_health_advice(metrics, heart_rate):
    advice = []
    if heart_rate == 0:
        advice.append("Your heart has effectively stopped for 15 seconds, if you don't elevate it soon you will be dead.")
    elif heart_rate < 60:
        advice.append("Your heart rate is relatively low. This could be normal if you're very fit, but consult a doctor if you feel unusual symptoms.")
    elif heart_rate > 100:
        advice.append("Your resting heart rate is elevated. Consider relaxation techniques or maintain proper hydration and recovery periods if your exercising.")
    else:
        advice.append("Your heart rate is within normal range.")

    return "\n".join(advice)

def on_submit():
    try:
        gender = gender_var.get()
        height = float(height_entry.get())
        weight = float(weight_entry.get())
        age = int(age_entry.get())
        heart_rate = get_stored_heart_rate()

        metrics = calculate_health_metrics(heart_rate, gender, height, weight, age)
        advice = generate_health_advice(metrics, heart_rate)

        result = f"""
Heart Rate Analysis Results:

Average Heart Rate: {heart_rate} BPM
Current Heart Rate Zone: {metrics['Current Zone']}
Estimated Max Heart Rate: {metrics['Max Heart Rate']} BPM
Basal Metabolic Rate: {metrics['BMR']} calories/day
Estimated Calories Burned: {metrics['Calories Burned']} cal

Health Advice:
{advice}
"""
        result_text.config(text=result)
        
    except ValueError as e:
        result_text.config(text="Error: Please enter valid numbers for height, weight, age, and heart rate.")
    except Exception as e:
        result_text.config(text=f"Error: An error occurred: {str(e)}")


root = tk.Tk()
root.after(100, force_focus)
root.title("Health Information")
root.geometry("500x600")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(expand=True, fill='both')

title_label = tk.Label(frame, text="Heart Rate Analysis", font=('Helvetica', 14, 'bold'))
title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

tk.Label(frame, text="Gender:").grid(row=1, column=0, sticky='w', pady=5)
gender_var = tk.StringVar(value="Male")
tk.Radiobutton(frame, text="Male", variable=gender_var, value="Male").grid(row=1, column=1, sticky='w')
tk.Radiobutton(frame, text="Female", variable=gender_var, value="Female").grid(row=1, column=2, sticky='w')

tk.Label(frame, text="Height (cm):").grid(row=2, column=0, sticky='w', pady=5)
height_entry = tk.Entry(frame)
height_entry.grid(row=2, column=1, columnspan=2, sticky='ew')

tk.Label(frame, text="Weight (kg):").grid(row=3, column=0, sticky='w', pady=5)
weight_entry = tk.Entry(frame)
weight_entry.grid(row=3, column=1, columnspan=2, sticky='ew')

tk.Label(frame, text="Age:").grid(row=4, column=0, sticky='w', pady=5)
age_entry = tk.Entry(frame)
age_entry.grid(row=4, column=1, columnspan=2, sticky='ew')

tk.Label(frame, text="Average Heart Rate (BPM):").grid(row=5, column=0, sticky='w', pady=5)
heart_rate_entry = tk.Entry(frame)
heart_rate_entry.grid(row=5, column=1, columnspan=2, sticky='ew')

stored_heart_rate = get_stored_heart_rate()
if stored_heart_rate is not None:
    heart_rate_entry.insert(0, str(stored_heart_rate))

def on_submit():
    try:
        gender = gender_var.get()
        height = float(height_entry.get())
        weight = float(weight_entry.get())
        age = int(age_entry.get())
        heart_rate = int(heart_rate_entry.get())

        metrics = calculate_health_metrics(heart_rate, gender, height, weight, age)
        advice = generate_health_advice(metrics, heart_rate)

        result = f"""
Heart Rate Analysis Results:

Average Heart Rate: {heart_rate} BPM
Current Heart Rate Zone: {metrics['Current Zone']}
Estimated Max Heart Rate: {metrics['Max Heart Rate']} BPM
Basal Metabolic Rate: {metrics['BMR']} calories/day
Estimated Calories Burned: {metrics['Calories Burned']} cal

Health Advice:
{advice}
"""
        result_text.config(text=result)
        
    except ValueError as e:
        result_text.config(text="Error: Please enter valid numbers for height, weight, age, and heart rate.")
    except Exception as e:
        result_text.config(text=f"Error: An error occurred: {str(e)}")

submit_btn = tk.Button(frame, text="Analyze Health Data", command=on_submit)
submit_btn.grid(row=6, column=0, columnspan=3, pady=20)

result_text = tk.Label(frame, text="Results will appear here...", justify='left', wraplength=400)
result_text.grid(row=7, column=0, columnspan=3, pady=10)

window_width = 500
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

root.mainloop()