import sys
import serial
import time
import threading
import serial.tools.list_ports
import pelco_p

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
def gimbal_mode3(ser):
    print('Selected Mode: Tracking')
    while True:
        try:
            if mode != 3:
                break
            # TODO: Implement tracking logic
        except KeyboardInterrupt:
            pass

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
