
from guizero import App, Text, TextBox, PushButton
import RPi.GPIO as GPIO
import datetime
import sys

sys.path.append('/home/pi/RasPi-Thermostat')
import settings
import domoticz

# Program version
Version = 1.16

# Basic settings
T1w_ID = '28-01191b9257fd'
T1w_dir = '/sys/bus/w1/devices/'
startup_delay = 5 # No. seconds before starting the proper display
T_Room_IDX = '65'
T_Off_IDX = '66'

# Initialise some variables...
T1w_b = settings.T1w_b # Gain
T1w_c = settings.T1w_c # Offset
T_off = settings.T_off # Default target range upper limit
T_d = settings.T_d     # Default hysteresis
T_on = T_off - T_d     # Default target range lower limit
current_time = 0.0
CH_Timer = False
CH_Boost = 0

# Timer defaults
CH1_on = settings.CH1_on
CH1_off = settings.CH1_off
CH2_on = settings.CH2_on
CH2_off = settings.CH2_off
CH3_on = settings.CH3_on
CH3_off = settings.CH3_off

# Waveshare 1.44 LCD GPIO
KEY_UP_PIN     = 26
KEY_DOWN_PIN   = 5
KEY_LEFT_PIN   = 19
KEY_RIGHT_PIN  = 6
KEY_PRESS_PIN  = 13
KEY1_PIN       = 21
KEY2_PIN       = 20
KEY3_PIN       = 16
CH_PIN         = 18

GPIO.setmode(GPIO.BCM) 
GPIO.cleanup()
GPIO.setup(KEY_UP_PIN,      GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY_DOWN_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY_LEFT_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY_RIGHT_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY_PRESS_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY1_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY2_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY3_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(CH_PIN,          GPIO.OUT)                          # Output


# C/H & H/W status defaults
CH_On = False
HW_On = False

GPIO.output(CH_PIN, CH_On) 

# define function to write settings to file
def write_settings():
    f = open("settings.py", 'w')
    f.write ("T1w_b = "   + str(T1w_b) + "\n")
    f.write ("T1w_c = "   + str(T1w_c) + "\n")
    f.write ("T_off = "   + str(T_off) + "\n")
    f.write ("T_d = "     + str(T_d) + "\n")
    f.write ("CH1_on = "   + str(CH1_on) + "\n")
    f.write ("CH1_off = "  + str(CH1_off) + "\n")
    f.write ("CH2_on = "   + str(CH2_on) + "\n")
    f.write ("CH2_off = "  + str(CH2_off) + "\n")
    f.write ("CH3_on = "   + str(CH3_on) + "\n")
    f.write ("CH3_off = "  + str(CH3_off) + "\n")
    f.close()
    
    
# Define function to read one-wire temperature sensors...
def read_temp_T1w(T1w_ID):
    # Read one-wire device
    device_file = T1w_dir + T1w_ID + '/w1_slave'
    f = open(device_file, 'r')
    lines = f.readlines()

    # Extract temperature data
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = f.readlines()
    f.close()

    # Format temperature data
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        measurement = float(temp_string) / 1000.0
        measurement = (measurement * T1w_b) + T1w_c
        measurement = round(measurement,1)
        return measurement

# Function to read & check the temperature
def check_temp():
    global T_Room, CH_On, CH_Timer
    
    T_Room = read_temp_T1w(T1w_ID)
    # C/H Timer
    if (CH_Boost > 0) or (current_time >= CH1_on) and current_time < CH1_off or (current_time >= CH2_on and current_time < CH2_off) or (current_time >= CH3_on and current_time < CH3_off):

        CH_Timer = True
        # C/H Thermostat
        if T_Room < T_on:
            CH_On = True
        elif T_Room > T_off:
            CH_On = False
    else:
        CH_Timer = False
        CH_On = False
            
    GPIO.output(CH_PIN, CH_On) 
    
# Function to update display
def disp_update():
    global startup_delay, current_time, CH_Boost
    now = datetime.datetime.now()
    current_time_hours = now.strftime("%H")
    current_time_minutes = now.strftime("%M")
    current_time_seconds = now.strftime("%S")
    current_date_day = now.strftime("%d")
    current_date_month = now.strftime("%m")
    current_date_year = now.strftime("%Y")

    current_time = float(current_time_hours) + (float(current_time_minutes) / 60.0)
    
    if CH_Boost > 0:
        CH_Boost = CH_Boost - 1
    
    if startup_delay == 0:
        disp_Temperature_Now.value = "{:.1f}°".format(T_Room)
        if CH_On:
            disp_Temperature_Now.bg = "red"
        else:
            disp_Temperature_Now.bg = "black"

        disp_Temperature_Off.value = "{:.1f}".format(T_on) + " - " + "{:.1f}".format(T_off)
        if CH_Boost > 0:
            CH_Boost_min = "0" + str(int(CH_Boost / 60))
            CH_Boost_min = CH_Boost_min[-2:]
            CH_Boost_sec = "0" + str(int(CH_Boost % 60))
            CH_Boost_sec = CH_Boost_sec[-2:]
            disp_Time.value = "Boost: " + CH_Boost_min + ":" + CH_Boost_sec
        else:
            if CH_Timer == True:
                disp_Time.value = current_time_hours + ":" + current_time_minutes + ":" + current_time_seconds + " (On)"
            else:
                disp_Time.value = current_time_hours + ":" + current_time_minutes + ":" + current_time_seconds + " (Off)"
        disp_Date.value = current_date_day + "/" + current_date_month + "/" + current_date_year
        if current_time_seconds == "00":
            check_temp()
            domoticz.LogToDomoticz(T_Room_IDX, T_Room)
            domoticz.LogToDomoticz(T_Off_IDX, T_off)
    else:
        startup_delay = startup_delay - 1
    
# Interrupt callback routine for KEY_PRESS_PIN
def callback_KEY_PRESS_PIN(channel):  
    global CH_Boost
    if CH_Boost == 0:
        CH_Boost = 3600
    else:
        CH_Boost = 0

# Interrupt callback routine for KEY_UP_PIN
def callback_KEY_UP_PIN(channel):  
    global T_off, T_on
    T_off = T_off + 0.5
    T_on = T_off - T_d
    write_settings()

# Interrupt callback routine for KEY_DOWN_PIN
def callback_KEY_DOWN_PIN(channel):  
    global T_off, T_on
    T_off = T_off - 0.5
    T_on = T_off - T_d
    write_settings()

app = App(title="Heating", height=128, width=128, bg="black")
app.tk.attributes("-fullscreen",True)

disp_Temperature_Now = Text(app, text="", size=80, color="white", bg="black")
disp_Temperature_Off = Text(app, text="RasPi-", size=30, color="yellow")
disp_Time = Text(app, text="Thermostat", size=30, color="yellow")
disp_Date = Text(app, text=str(Version), size=30, color="yellow")

# Setup interrupts
GPIO.add_event_detect(KEY_UP_PIN, GPIO.FALLING, callback=callback_KEY_UP_PIN, bouncetime=300) 
GPIO.add_event_detect(KEY_DOWN_PIN, GPIO.FALLING, callback=callback_KEY_DOWN_PIN, bouncetime=300)
GPIO.add_event_detect(KEY_PRESS_PIN, GPIO.FALLING, callback=callback_KEY_PRESS_PIN, bouncetime=300)

# Initial call to check the temperature
check_temp()

# Schedule a call update the time every second
disp_Time.repeat(1000, disp_update)

# Start the display process
app.display()
