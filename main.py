###################################################################################################################
#University:             Technical University of Crete
#School:                 School of Electrical & Computer Engineering
#Author:                 Manesis Athanasios
#Thesis:                 Embedded gimbal system for land-based tracking of UAV
#Edge Device:            RPi-4
#Gimbal:                 AS20-RS485
#Development Tools:      Sublime Text Editor, Geany IDE, TensorFlow

#Additional Comments:     
'''                         
'''
###################################################################################################################
import sys
import serial
import time
import pelco_p
#import pelco_d     #Uncomment if you want to use Pelco-D



if __name__ == '__main__':

    #init gimbal try, problem with import serial  (import serial ModuleNotFoundError: No module named 'serial')
    '''
    ser = pyserial.Serial('COM4', 9600, timeout=1)  # Replace 'COM1' with the appropriate port and 9600 with the correct baud rate
    frame = (0xA0, 0x00, 0x00, 0x00, 0x00, 0x00, 0xAF, 0x0F)
    ser.write(frame)  # Send the command frame over the serial connection
    time.sleep(0.1)  # Wait for the command to be sent
    '''


    
    #Some examples for Pelco-P frames testing

    '''
    pelco_p.right_deg(30)
    pelco_p.left_deg(45)
    pelco_p.up_deg(42)
    pelco_p.down_deg(15)
    '''

    #Some examples for Pelco-D frames testing

    '''
    pelco_d.right_deg(30)
    pelco_d.left_deg(45)
    pelco_d.up_deg(42)
    pelco_d.down_deg(15)
    '''