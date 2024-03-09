########################################################################################################################################
#University:             Technical University of Crete
#School:                 School of Electrical & Computer Engineering
#Author:                 Manesis Athanasios
#Thesis:                 Embedded gimbal system for land-based tracking of UAV
#GitHub Repo:            https://github.com/amanesis/thesis
#Edge Device:            RPi-4
#Gimbal:                 AS20-RS485

#Additional Comments:     
'''
                        This script controls an embedded gimbal system for land-based tracking of UAVs. It is designed to run on an
                        edge device, specifically an RPi-4, and communicates with the gimbal over RS485 protocol. The script provides
                        different modes of operation for the gimbal, including vertical scan, horizontal scan, tracking, and idle.
                        Please make sure to update the COM port and baud rate in the serial connection setup.                         
'''
########################################################################################################################################

import sys
import serial
import time
import threading
import serial.tools.list_ports

#import pelco_d     # Uncomment if you want to use Pelco-D 
import pelco_p

'''
    Modifying for Pelco-D API:
    If you want to use the Pelco-D API instead of Pelco-P and the function names are the same, you need to make the following changes:
    - Uncomment the import statement for the pelco_d module at the top of the script.
    - Replace the function calls and commands from pelco_p with the corresponding ones from pelco_d.
    - Update the implementation of gimbal mode functions and gimbal init to use the Pelco-D commands and logic.

    Example:
    - Uncomment the line: import pelco_d
    - Replace pelco_p.up() with pelco_d.up()
    - Replace pelco_p.down() with pelco_d.down()
    - Replace pelco_p.right() with pelco_d.right()
    - Replace pelco_p.left() with pelco_d.left()

    Note: Ensure that you have the pelco_d module available
'''
import cv2
import numpy as np
import tflite_runtime.interpreter as tflite

# Load the TensorFlow Lite model
model_path = 'path/to/your/model.tflite'
interpreter = tflite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Placeholder function for drone detection
def detect_drone(image):
    # Preprocess the input image for the TensorFlow Lite model
    input_shape = input_details[0]['shape']
    input_data = cv2.resize(image, (input_shape[1], input_shape[2]))
    input_data = np.expand_dims(input_data, axis=0)
    input_data = input_data.astype(np.float32) / 255.0  # Normalize the image

    # Set the input tensor
    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Run inference
    interpreter.invoke()

    # Get the output tensor
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # TODO: Process the output_data to get the bounding box of the detected drone
    # This will depend on the format of your model's output

    # For demonstration purposes, returning a random bounding box
    x, y, width, height = 50, 50, 20, 20
    return x, y, width, height


speed_deg_per_sec = 5  # Gimbal rotation speed in degrees per second
mode = 0  # Initialize mode variable
active_thread = None  # Initialize active_thread variable
mode_lock = threading.Lock()  # Lock for synchronizing mode changes

# Function to calculate the rotation time for a given angle
def calculate_rotation_time(angle):
    return abs(angle / speed_deg_per_sec)

# Function to initialize the gimbal to the UP-RIGHT position
def gimbal_init(ser):
    try:
        print('Initialize the gimbal to the UP-RIGHT position.')
        print('Initialization takes 40 seconds, please wait ...')

        ser.write(pelco_p.up())
        time.sleep(20)
        ser.flush()
        time.sleep(0.1)
        ser.write(pelco_p.right())
        time.sleep(20)
        ser.flush()

        print('Initialization complete!')
        print('')
    except KeyboardInterrupt:
        ser.write(pelco_p.stop())

# Mode 1: Vertical Scan
def gimbal_mode1(ser):
    print('Selected Mode: Vertical Scan')
    while True:
        try:
            if mode != 1:
                break
            ser.write(pelco_p.down())
            time.sleep(16)
            ser.write(pelco_p.up())
            time.sleep(16)
        except KeyboardInterrupt:
            ser.write(pelco_p.stop())

# Mode 2: Horizontal Scan
def gimbal_mode2(ser):
    print('Selected Mode: Horizontal Scan')
    while True:
        try:
            if mode != 2:
                break
            ser.write(pelco_p.left())
            time.sleep(20)
            ser.flush()
            ser.write(pelco_p.right())
            time.sleep(20)
            ser.flush()
        except KeyboardInterrupt:
            ser.write(pelco_p.stop())

# Mode 3: Tracking
# Mode 3: Tracking
def gimbal_mode3(ser):
    print('Selected Mode: Tracking')
    while True:
        try:
            if mode != 3:
                break

            # Capture an image from your camera (replace this with your actual image capture logic)
            # For demonstration purposes, using a blank image
            image = np.zeros((480, 640, 3), dtype=np.uint8)

            # Detect drone and get bounding box
            x, y, width, height = detect_drone(image)

            # Calculate the center of the bounding box
            center_x = x + width / 2
            center_y = y + height / 2

            # TODO: Implement gimbal tracking logic to keep the drone in the center
            # You may use pelco_p commands like pelco_p.pan_tilt_absolute(pan_value, tilt_value)
            # based on the center coordinates and camera resolution

            # Example:
            pan_value = int(center_x / 100 * 255)  # Adjust the factor based on your camera resolution
            tilt_value = int(center_y / 100 * 255)  # Adjust the factor based on your camera resolution

            ser.write(pelco_p.pan_tilt_absolute(pan_value, tilt_value))
            
            # Add a delay to control the tracking update rate
            time.sleep(0.5)

        except KeyboardInterrupt:
            ser.write(pelco_p.stop())

# Rest of your code remains unchanged

# Mode 4: Idle
def gimbal_mode4(ser):
    print('Selected Mode: Idle')
    while True:
        try:
            if mode != 4:
                break
            # TODO: Implement idle logic
        except KeyboardInterrupt:
            pass

# Function to print COM port information
def print_com_port_info(port_name):
    ports = serial.tools.list_ports.comports()
    port_in_use = None
    for port in ports:
        if port.device == port_name:
            port_in_use = port
            break
    if port_in_use is None:
        print(f"COM port {port_name} not found or not in use.")
    else:
        print(f"Port: {port_in_use.device}")
        print(f"Description: {port_in_use.description}")
        print(f"Manufacturer: {port_in_use.manufacturer}")
        print(f"Hardware ID: {port_in_use.hwid}")
        print(f"Product ID: {port_in_use.pid}")
        print(f"Serial Number: {port_in_use.serial_number}")
        print(f"Location: {port_in_use.location}")
        print(f"USB VID:PID: {port_in_use.vid:04x}:{port_in_use.pid:04x}\n")

# Function to stop the active thread
def stop_active_thread(active_thread):
    if active_thread is not None and active_thread.is_alive():
        active_thread.join()

            


# Main control loop
def gimbal_control_loop(ser):

    """
    Main control loop for selecting and switching between gimbal modes.

    Args:
        ser (Serial): Serial connection object.

    Description:
        This function serves as the main control loop of the program. It allows the user to select and switch between
        different gimbal modes by inputting the desired mode number. The function continuously prompts the user for mode
        selection until the user enters 'exit' to quit the program.

        The function takes a serial connection object 'ser' as an argument, which is used to communicate with the gimbal
        controller.

        The function first initializes the global variables 'mode' and 'active_thread'.

        Inside the main loop, it prompts the user to enter a gimbal mode (1-4) or 'exit'. If the mode is already active,
        it displays a message and continues to the next iteration.

        When a new mode is selected, the function acquires the 'mode_lock' to synchronize mode changes. It stops the
        active thread if it is running by calling the 'stop_active_thread' function.

        Based on the selected mode, it creates a new thread using the corresponding gimbal mode function (gimbal_mode1,
        gimbal_mode2, gimbal_mode3, gimbal_mode4) as the target. The 'daemon' argument is set to True to allow the
        program to exit even if the thread is still running.

        If an invalid mode is entered, it displays an error message and continues to the next iteration.

        Finally, it starts the newly created thread and continues to the next iteration of the loop.

        If the user enters 'exit', the loop breaks, and the function calls 'stop_active_thread' to ensure the active
        thread is stopped before exiting the program.



    """
    global mode
    global active_thread

    while True:
        new_mode = input("Enter gimbal mode (1-4) or 'exit' to quit: ")

        if new_mode == "exit":
            break

        new_mode = int(new_mode)

        if new_mode == mode:
            print("Already in that mode.")
            continue

        with mode_lock:
            mode = new_mode

            if active_thread is not None:
                stop_active_thread(active_thread)

            if mode == 1:
                active_thread = threading.Thread(target=gimbal_mode1, args=(ser,), daemon=True)

            elif mode == 2:
                active_thread = threading.Thread(target=gimbal_mode2, args=(ser,), daemon=True)
                
            elif mode == 3:
                active_thread = threading.Thread(target=gimbal_mode3, args=(ser,), daemon=True)

            elif mode == 4:
                active_thread = threading.Thread(target=gimbal_mode4, args=(ser,), daemon=True)

            else:
                print("Invalid mode! Please enter a valid mode (1-4) or 'exit'.")
                continue

            active_thread.start()

    stop_active_thread(active_thread)


if __name__ == '__main__':
    mode = 0  # Initialize mode variable
    print('\nOpening port ... \n')

    # Set the COM port here
    port_name = 'COM4'

    # Print COM port information
    print_com_port_info(port_name)


    try:

        ser = serial.Serial(port_name, 9600, timeout=1)
        gimbal_init(ser) 
        gimbal_control_loop(ser) 
        ser.close()

    except serial.SerialException as e:
        print(f"Failed to open serial port: {e}")
        sys.exit(1)

