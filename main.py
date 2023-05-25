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

#import serial
import time
import pelco_p
#import pelco_d     #Uncomment if you want to use Pelco-D



if __name__ == '__main__':
    
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