###################################################################################################################
#University:             Technical University of Crete
#School:                 School of Electrical & Computer Engineering
#Author:                 Manesis Athanasios
#Thesis:                 Embedded gimbal system for land-based tracking of UAV
#Edge Device:            RPi-4
#Gimbal:                 AS20-RS485
#Development Tools:      Sublime Text Editor, Geany IDE, TensorFlow

#Additional Comments:     
'''                         The main objective of this file is to demonstrate the fundamental functionalities 
                            of a gimbal. This version includes the complete implementation for zoom wide,
                            zoom tele, focus near, and focus far, as per the Pelco-P protocol. 

                            However, these functions are not utilized in this program since 
                            only the pan and tilt functions are required.

                            A test program is provided in the main function, which initializes 
                            the gimbal to a specific position and then performs a customized movement.
'''
###################################################################################################################


import time


#Basic Functions
#The basic Pelco-P frames for pan/tilt and fo+/fo-,zo+/zo-




def stop():
    pelco_d_frame = (0xA0, 0x00, 0x00, 0x00, 0x00, 0x00, 0xAF, 0x0F)
    #ser.write(pelco_d_frame)  #Send the command frame over the serial connection
    #time.sleep(0.1)  # Wait for the command to be sent
    hex_list = [hex(element) for element in pelco_d_frame]
    hex_string = " ".join(hex_list)
    #print(hex_string)
    return pelco_d_frame

def down():
    pelco_d_frame = (0xA0, 0x00, 0x00, 0x10, 0x00, 0x20, 0xAF, 0x3F)
    #ser.write(pelco_d_frame)  # Send the command frame over the serial connection
    #time.sleep(0.1)  # Wait for the command to be sent
    hex_list = [hex(element) for element in pelco_d_frame]
    hex_string = " ".join(hex_list)
    #print(hex_string)
    return pelco_d_frame

def up():
    pelco_d_frame = (0xA0, 0x00, 0x00, 0x08, 0x00, 0x20, 0xAF, 0x27)
    #ser.write(pelco_d_frame)  # Send the command frame over the serial connection
    #time.sleep(0.1)  # Wait for the command to be sent
    hex_list = [hex(element) for element in pelco_d_frame]
    hex_string = " ".join(hex_list)
    # print(hex_string)
    return pelco_d_frame

def left():
    pelco_d_frame = (0xA0, 0x00, 0x00, 0x04, 0x20, 0x00, 0xAF, 0x2B)
    #ser.write(pelco_d_frame)  # Send the command frame over the serial connection
    #time.sleep(0.1)  # Wait for the command to be sent
    hex_list = [hex(element) for element in pelco_d_frame]
    hex_string = " ".join(hex_list)
    # print(hex_string)
    return pelco_d_frame

def right():
    pelco_d_frame = (0xA0, 0x00, 0x00, 0x02, 0x20, 0x00, 0xAF, 0x2D)
    #ser.write(pelco_d_frame)  # Send the command frame over the serial connection
    #time.sleep(0.1)  # Wait for the command to be sent
    hex_list = [hex(element) for element in pelco_d_frame]
    hex_string = " ".join(hex_list)
    # print(hex_string)
    return pelco_d_frame

def zoom_wide():
    pelco_d_frame = (0xA0, 0x00, 0x00, 0x20, 0x00, 0x20, 0xAF, 0x0F)
    hex_list = [hex(element) for element in pelco_d_frame]
    hex_string = " ".join(hex_list)
    # print(hex_string)
    return pelco_d_frame

def zoom_tele():
    pelco_d_frame = (0xA0, 0x00, 0x00, 0x40, 0x00, 0x20, 0xAF, 0x6F)
    hex_list = [hex(element) for element in pelco_d_frame]
    hex_string = " ".join(hex_list)
    # print(hex_string)
    return pelco_d_frame

def focus_near():
    pelco_d_frame = (0xA0, 0x00, 0x01, 0x00, 0x00, 0x00, 0xAF, 0x0E)
    hex_list = [hex(element) for element in pelco_d_frame]
    hex_string = " ".join(hex_list)
    # print(hex_string)
    return pelco_d_frame

def focus_far():
    pelco_d_frame = (0xA0, 0x00, 0x02, 0x00, 0x00, 0x00, 0xAF, 0x0D)
    hex_list = [hex(element) for element in pelco_d_frame]
    hex_string = " ".join(hex_list)
    # print(hex_string)
    return pelco_d_frame

#Degree Functions

#The AS20-RS485 gimbal doesn't support degrees, but it has 5deg/1sec rotation speed
#I add time delay base on this speed.


def down_deg(deg):
    pelco_d_frame = (0xA0, 0x00, 0x00, 0x10, 0x00, 0x20, 0xAF, 0x3F)

    hex_list = [hex(element) for element in pelco_d_frame]
    hex_string = " ".join(hex_list)
    print(hex_string)

    while deg != 0:
        deg -= 1
    stop()

def up_deg(deg):
    pelco_d_frame = (0xA0, 0x00, 0x00, 0x08, 0x00, 0x20, 0xAF, 0x27)
    hex_list = [hex(element) for element in pelco_d_frame]
    hex_string = " ".join(hex_list)
    print(hex_string)

    while deg != 0:
        deg -= 1
    stop()

def left_deg(deg):
    pelco_d_frame = (0xA0, 0x00, 0x00, 0x04, 0x20, 0x00, 0xAF, 0x2B)

    hex_list = [hex(element) for element in pelco_d_frame]
    hex_string = " ".join(hex_list)
    print(hex_string)

    while deg != 0:
        deg -= 1
    stop()


def right_deg(deg):
    pelco_d_frame = (0xA0, 0x00, 0x00, 0x02, 0x20, 0x00, 0xAF, 0x2D)
    
    hex_list = [hex(element) for element in pelco_d_frame]
    hex_string = " ".join(hex_list)
    print(hex_string)

    while deg != 0:
        deg -= 1
    stop()




'''
# Main program
if __name__ == '__main__':
    
    left()
    right()
    up()
    down()
    zoom_wide()
    zoom_tele()
    focus_near()
    focus_far()

'''
