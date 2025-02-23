import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
from datetime import datetime
import time
import subprocess
import sys

def find_arduino_port():
    """Automatically find the Arduino port."""
    ports = list(serial.tools.list_ports.comports())
    
    for port in ports:
        if "Arduino" in port.description:
            return port.device
            
    common_identifiers = ["usbmodem", "ttyACM", "ttyUSB", "cu.usbmodem"]
    for port in ports:
        if any(identifier in port.device for identifier in common_identifiers):
            return port.device
            
    if ports:
        return ports[0].device
        
    return None

SERIAL_PORT = find_arduino_port()
if SERIAL_PORT:
    print(f"Found serial port: {SERIAL_PORT}")
else:
    raise Exception("No suitable serial ports found!")
BAUD_RATE = 9600

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    ser.flush()
    print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
except serial.SerialException as e:
    print(f"Failed to connect to serial port: {e}")
    exit()

time_window = 17  
sample_rate = 100
max_samples = time_window * sample_rate
timestamps = deque(maxlen=max_samples)
heart_rates = deque(maxlen=max_samples)

plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_xlabel('Time (s)')
ax.set_ylabel('Heart Rate (BPM)')
ax.set_title('Live Heart Rate Monitor')
ax.set_xlim(0, 15) 
ax.set_ylim(50, 100) 
ax.grid(True)

initial_hr = 70  # typical resting heart rate
timestamps.append(0)
heart_rates.append(initial_hr)

try:
    start_time = datetime.now()
    running = True
    while running:
        if ser.in_waiting > 0:
            raw_data = ser.readline().decode('utf-8').strip()
            print(f"Raw data received: {raw_data}")

            try:
                heart_rate = int(raw_data)
                current_time = datetime.now()
                elapsed_time = (current_time - start_time).total_seconds()

                if elapsed_time <= time_window:
                    if elapsed_time >= 1:
                        timestamps.append(elapsed_time - 1)
                        heart_rates.append(heart_rate)
                        
                        line.set_xdata(timestamps)
                        line.set_ydata(heart_rates)
                        
                        min_hr = min(heart_rates)
                        max_hr = max(heart_rates)
                        range_hr = max_hr - min_hr
                        
                        if range_hr < 30:
                            mid_point = (max_hr + min_hr) / 2
                            min_hr = mid_point - 15
                            max_hr = mid_point + 15
                        
                        ax.set_ylim(min_hr - 5, max_hr + 5)
                        
                        fig.canvas.draw()
                        fig.canvas.flush_events()
                        plt.pause(0.01)
                else:
                    running = False
                    avg_bpm = int(np.mean(heart_rates))
                    print(f"Average BPM: {avg_bpm}")
                    
                    with open('heart_rate_data.txt', 'w') as f:
                        f.write(str(avg_bpm))

                    ser.close()
                    
                    plt.ioff()
                    plt.close('all')
                    
                    print("Launching health analysis...")
                    subprocess.Popen([sys.executable, 'health_analysis.py'])
                    time.sleep(0.5)  
                    sys.exit(0)

            except ValueError:
                print(f"Invalid data received: {raw_data}. Skipping...")
            except Exception as e:
                print(f"Unexpected error: {e}. Skipping...")

except KeyboardInterrupt:
    print("Exiting...")
finally:
    ser.close()
    plt.close('all')