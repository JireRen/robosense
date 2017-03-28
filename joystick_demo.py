#!/usr/bin/python
import spidev
import time
import os

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
# Define sensor channels
# (channels 3 to 7 unused)
swt_channel = 0
vrx_channel = 1
vry_channel = 2
fsr_channel = 3
# Define delay between readings (s)
delay = 0.1

while True:

  # Read the joystick position data
  vrx_pos = ReadChannel(vrx_channel)
  vry_pos = ReadChannel(vry_channel)

  # Read switch state
  swt_val = ReadChannel(swt_channel)
  fsr_val = ReadChannel(fsr_channel)

  # Print out results
  # print "--------------------------------------------"  
  # print("X : {}  Y : {}  Switch : {}".format(vrx_pos,vry_pos,fsr_val))
  if swt_val > 700:
    if (vrx_pos < 700 and vrx_pos > 400):
      print "waiting command"
    elif vrx_pos > 700:
      print "Start postive"
      os.system('ssh -p 3022 viki@10.144.136.69 -t "sh ~/move.sh"')
    else:
      print "Start negative"
      os.system('ssh -p 3022 viki@10.144.136.69 -t "sh ~/move2.sh"')
    
    if (vry_pos < 700 and vry_pos > 400):
      print "waiting command"
    elif vry_pos > 700:
      print "Start postive"
      os.system('ssh -p 3022 viki@10.144.136.69 -t "sh ~/move3.sh"')
    else:
      print "Start negative"
      os.system('ssh -p 3022 viki@10.144.136.69 -t "sh ~/move4.sh"')


  else:
    print "STOOOOOOOOOOOP"
    os.system('ssh -p 3022 viki@10.144.136.69 -t "sh ~/stop.sh"')
    #print "Stopped"
  
#  if (vry_pos < 700 and vry_pos > 400):
#    print "waiting command"
#  elif vry_pos > 700:
#    print "Start postive"
#    os.system('ssh -p 3022 viki@10.144.136.69 -t "sh ~/move3.sh"')
#  else:
#    print "Start negative"
#    os.system('ssh -p 3022 viki@10.144.136.69 -t "sh ~/move4.sh"')


  #if fsr_channel < 600:
  #  os.system('ssh -p 3022 viki@10.144.136.69 -t "sh ~/stop.sh"')
  #  print "System shutting down"
  # Wait before repeating loop
  time.sleep(delay)
