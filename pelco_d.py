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
                            of a gimbal. This version includes the complete implementation for pan/tilt, zoom wide,
                            zoom tele, focus near, and focus far, as per the Pelco-D protocol. 

                            The Pelco-D protocol was not used for the needs of the project, but it can be 
                            supportedin case another gimbal is used or the AS20-RS485 dip-switches are set 
                            for Pelco-D (see AS20-RS485 manual).
'''
###################################################################################################################




import time
TILT_DEG_TIME = 190000 #Tilt time for one degree
PAN_DEG_TIME = 114000 #Pan time for one degree

#Basic Functions
#The basic Pelco-D frames for pan/tilt and fo+/fo-,zo+/zo-


def _delay_us(us):
    time.sleep(us/1000000.0)

def stop():
    pelco_d_frame = (0xFF, 0x01, 0x00, 0x00, 0x00, 0x00, 0x01)

def down():
    pelco_d_frame = (0xFF, 0x01, 0x00, 0x10, 0x00, 0x20, 0x31)

def up():
    pelco_d_frame = (0xFF, 0x01, 0x00, 0x08, 0x00, 0x20, 0x29) 

def left():
    pelco_d_frame = (0xFF, 0x01, 0x00, 0x04, 0x20, 0x00, 0x25)

def right():
    pelco_d_frame = (0xFF, 0x01, 0x00, 0x02, 0x20, 0x00, 0x23)
 
def zoom_wide():
    pelco_d_frame = (0xFF, 0x01, 0x00, 0x20, 0x00, 0x00, 0x21) 

def zoom_tele():
    pelco_d_frame = (0xFF, 0x01, 0x00, 0x40, 0x00, 0x00, 0x41)

def focus_near():
    pelco_d_frame = (0xFF, 0x01, 0x00, 0x80, 0x00, 0x00, 0x81)

def focus_far():
    pelco_d_frame = (0xFF, 0x01, 0x01, 0x00, 0x00, 0x00, 0x02)


#Degree Functions

#The AS20-RS485 gimbal doesn't support degrees, but it has 5deg/1sec rotation speed
#I add time delay base on this speed.


def down_deg(deg):
    pelco_d_frame = (0xFF, 0x01, 0x00, 0x10, 0x00, 0x20, 0x31)

    hex_list = [hex(element) for element in pelco_d_frame]
    hex_string = " ".join(hex_list)
    print(hex_string)

    while deg != 0:
        _delay_us(TILT_DEG_TIME)
        deg -= 1
    stop()

def up_deg(deg):
    pelco_d_frame = (0xFF, 0x01, 0x00, 0x08, 0x00, 0x20, 0x29) 
    hex_list = [hex(element) for element in pelco_d_frame]
    hex_string = " ".join(hex_list)
    print(hex_string)

    while deg != 0:
        _delay_us(TILT_DEG_TIME)
        deg -= 1
    stop()

def left_deg(deg):
    pelco_d_frame = (0xFF, 0x01, 0x00, 0x04, 0x20, 0x00, 0x25)

    hex_list = [hex(element) for element in pelco_d_frame]
    hex_string = " ".join(hex_list)
    print(hex_string)

    while deg != 0:
        _delay_us(PAN_DEG_TIME)
        deg -= 1
    stop()


def right_deg(deg):
    pelco_d_frame = (0xFF, 0x01, 0x00, 0x02, 0x20, 0x00, 0x23)
    
    hex_list = [hex(element) for element in pelco_d_frame]
    hex_string = " ".join(hex_list)
    print(hex_string)

    while deg != 0:
        _delay_us(PAN_DEG_TIME)
        deg -= 1
    stop()



'''

# Main program
if __name__ == '__main__':
    
    right_deg(45)
    up_deg(42)
    left_deg(21)
    down_deg(15)

'''