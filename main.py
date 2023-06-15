########################################################################################################################################
#University:             Technical University of Crete
#School:                 School of Electrical & Computer Engineering
#Author:                 Manesis Athanasios
#Thesis:                 Embedded gimbal system for land-based tracking of UAV
#Edge Device:            RPi-4
#Gimbal:                 AS20-RS485
#Development Tools:      Sublime Text Editor, Geany IDE, TensorFlow

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
import pelco_p
#import pelco_d     #Uncomment if you want to use Pelco-D

# Init Function
def gimbal_init():

    print('Initialize the gimbal to the UP-RIGHT position.')
    print('Initialization takes 40 seconds, please wait...')

    ser.write(pelco_p.up())
    time.sleep(20)
    ser.flush()
    time.sleep(0.1)
    ser.write(pelco_p.right())
    time.sleep(20)
    ser.flush()

    print('Initialization complete!')
    print('')


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


# Gimbal Menu
def print_menu():
    print('')
    print('Select Mode:')
    print('1: Vertical Scan')
    print('2: Horizontal Scan')
    print('3: Tracking')
    print('4: Idle')
    print('')


# Main

if __name__ == '__main__':

    
    print('Opening port...')

    try:
        ser = serial.Serial('COM4', 9600)  # Replace 'COM4' with the appropriate port and 9600 with the correct baud rate
        print('Port is open.')

    except serial.SerialException:
        serial.Serial('COM4', 9600).close()
        print('Port is closed')
        raise SystemExit


    print('Ready to use.')

    gimbal_init()

    gimbal_mode_selection_menu() 

    ser.close();
    
