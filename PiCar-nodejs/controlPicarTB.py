#!/usr/bin/env python

# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time
import signal
import sys

# Import the PCA9685 module.
import Adafruit_PCA9685
#and zerorpc!
import zerorpc

# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
servo_min = 280  # Min pulse length out of 4096
servo_mid = 410  # mid 
servo_max = 530  # Max pulse length out of 4096

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

print('Moving  on channel 8, steering on channel 11 press Ctrl-C to quit...')
ch_speed = 8
ch = ch_speed
ch_steer = 11
pwm.set_pwm(ch_speed, 0, servo_mid)
pwm.set_pwm(ch_steer, 0, servo_mid)



def check_speed(beta):
	if beta < -15.0 :
		s = 2 #back
	elif beta > 15.0 :
		s = 8 #forward
	else :
		s = 0 #stopped
	return s

def check_steer(gamma):
	if gamma < -15.0 :
		s = 4 # left
	elif gamma > 15.0 :
		s = 6 #right
	else :
		s = 5 #straight
	return s

c = zerorpc.Client()
c.connect("tcp://127.0.0.1:4242")

while True:
	result = c.hello("RPC")
        print result
	angles = result
	alpha = angles[0]
	beta = angles[1]
	gamma = angles[2]

	# Input  speed demands on channel 8 steering on 11
    	#wait = input() #wait for keystroke
	# this was designed for keboard input

	sp = check_speed(beta)
   	#print("Your speed",sp)
	if sp == 8:
		#print("forward")	
		servo = servo_min
		ch =  ch_speed
	elif sp == 2:
		#print("back")
		servo = servo_max
		ch =  ch_speed		
 	elif sp == 0:
		#print("stop")
		servo = servo_mid
	 	ch =  ch_speed  
	pwm.set_pwm(ch, 0, servo)
 	time.sleep(0.2)
	pwm.set_pwm(ch, 0, servo_mid) #this is impulse speed control 

	st = check_steer (gamma)
        #print("Your steering",st)
        
  	if st == 5:
         	#print("straight")
         	servo = servo_mid
	 	ch =  ch_steer
	elif st == 4:
         	#print("left")
         	servo = servo_max
         	ch =  ch_steer
	elif st == 6:
		#print("right")
		servo = servo_min
		ch =  ch_steer
	pwm.set_pwm(ch, 0, servo)
 	time.sleep(1.0) 
 	
 		

def sigint_handler(signal, frame):
    print 'Interrupted reset we must'
    pwm.set_pwm(8, 0, servo_mid)
    pwm.set_pwm(11, 0, servo_mid)
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)			
