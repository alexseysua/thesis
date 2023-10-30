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
import keyboard
import serial.tools.list_ports

#import pelco_d     # Uncomment if you want to use Pelco-D 
import pelco_p


speed_deg_per_sec = 5  # Gimbal rotation speed in degrees per second
lookup_table = {}



def calculate_rotation_time(angle):
    
    #Calculates the time needed for the gimbal to rotate to the specified angle based on the lookup table.
    
    if angle in lookup_table:
        return lookup_table[angle]
    else:
        return abs(angle / speed_deg_per_sec)

def build_lookup_table():
    
    # Builds the lookup table for angle-to-time mapping based on gimbal speed.
    
    global lookup_table
    lookup_table = {}
    for angle in range(0, 360):
        time_needed = abs(angle / speed_deg_per_sec)
        lookup_table[angle] = time_needed

# for main
# build_lookup_table() 
# time.sleep(calculate_rotation_time(desired_angle))


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

# Init Function
def gimbal_init():

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
        


# Gimbal Modes
def gimbal_mode1():

    print('Selected Mode: Vertical Scan')

    while (True):
        
        try:
            ser.write(pelco_p.down())
            time.sleep(16)
    
            ser.write(pelco_p.up())
            time.sleep(16)

        except KeyboardInterrupt:     #Ctrl+C interrupt
            ser.write(pelco_p.stop())
            gimbal_mode_selection_menu()


def gimbal_mode2():
    print('Selected Mode: Horizontal Scan')
    
    while (True):
       
        try:
            ser.write(pelco_p.left())
            time.sleep(20)
            ser.flush()
            ser.write(pelco_p.right())
            time.sleep(20)
            ser.flush()

        except KeyboardInterrupt:
            ser.write(pelco_p.stop())
            gimbal_mode_selection_menu()
            

def gimbal_mode3():
        
    print('Selected Mode: Tracking')

    while (True):

        try:

            # TODO: Implement tracking logic
            pass

        except KeyboardInterrupt:
            gimbal_mode_selection_menu()


def gimbal_mode4():
        
    print('Selected Mode: Idle')

    while (True):

        try:
            pass

        except KeyboardInterrupt:
            gimbal_mode_selection_menu()
    


# Gimbal Mode Menu for user selection
def gimbal_mode_selection_menu():
    

    try:

        print_menu()
        input_mode = input()

        match input_mode:

            case "1":
                gimbal_mode1()

            case "2":
                gimbal_mode2()

            case "3":
                gimbal_mode3()

            case "4":
                gimbal_mode4()

    except KeyboardInterrupt:
        return


# Gimbal Menu
def print_menu():
    print('')
    print('Select Mode:')
    print('1: Vertical Scan')
    print('2: Horizontal Scan')
    print('3: Tracking')
    print('4: Idle')
    print('')


def print_com_port_info(port_name):
    # Get a list of available ports
    ports = serial.tools.list_ports.comports()

    # Find the desired port
    port_in_use = None
    for port in ports:
        if port.device == port_name:
            port_in_use = port
            break

    if port_in_use is None:
        print(f"COM port {port_name} not found or not in use.")
    else:

        # Print the port information
        print(f"Port: {port_in_use.device}")
        print(f"Description: {port_in_use.description}")
        print(f"Manufacturer: {port_in_use.manufacturer}")
        print(f"Hardware ID: {port_in_use.hwid}")
        print(f"Product ID: {port_in_use.pid}")
        print(f"Serial Number: {port_in_use.serial_number}")
        print(f"Location: {port_in_use.location}")
        print(f"USB VID:PID: {port_in_use.vid:04x}:{port_in_use.pid:04x}\n")



######################################################################
#                             Main                                   
######################################################################

if __name__ == '__main__':


    '''

        Description: This is the main entry point of the script.

        Execution:
        - The script opens the serial port connection to the gimbal.
        - It prints the information about the COM port being used.
        - The gimbal is initialized to the UP-RIGHT position.
        - The user is presented with a gimbal mode selection menu.
        - Depending on the user's input, the script enters the selected gimbal mode.
        - If the execution is interrupted by pressing Ctrl+C, the script handles the interruption and returns to the mode selection menu.
        - When the user exits the mode selection menu, the script closes the serial port connection.

        Modifying the Configuration:
        - Update the serial port and baud rate in the line where `serial.Serial` is initialized.
        - Modify the gimbal initialization code in `gimbal_init()` to set the gimbal to the desired initial position.
        - Adjust the gimbal mode implementations in `gimbal_mode1()`, `gimbal_mode2()`, `gimbal_mode3()`, and `gimbal_mode4()` according to your specific requirements.

    '''

    
    print('\nOpening port ... \n')

    try:
        ser = serial.Serial('COM4', 9600)  # Replace 'COM4' with the appropriate port and 9600 with the correct baud rate
        print_com_port_info("COM4")
        print('Port is open, ready to use!\n')
        

    except serial.SerialException:
        serial.Serial('COM4', 9600).close()
        raise SystemExit('Unable to connect with Port. System Exit')




    gimbal_init()

    gimbal_mode_selection_menu() 

    print('Exit from Menu, port will close')



    ser.close();
    
