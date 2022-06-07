#!/usr/bin/python3

import RPi.GPIO as GPIO
import os
import time
from threading import Thread

from upspackv2 import *

def shutdown_check():
	print("UPS - Monitoring Mains Power")
	print("Start Shutdown Check...")

	ups = UPS2("/dev/ttyAMA0")
	version,vin,batcap,vout = ups.decode_uart()
	print("--------------------------------")
	print(" UPS Version: " + version)
	print("--------------------------------")

	i = 1

	cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	start_time = "Start time: "+cur_time + "\n\n"

	with open("/home/pi/log.txt","a+") as f:
		f.write(start_time)

	while True:
		version,vin,batcap,vout = ups.decode_uart()

		if vin == "NG":
			print("USB input adapter: DISCONNECTED!")
			output_string = "USB input adapter: DISCONNECTED! \nBattery Capacity: " + batcap + "% \nUPS Output Voltage: " + vout + " mV \n\n"
			with open("/home/pi/log.txt","a+") as f:
				f.write(output_string)
			i = 1
			break
		else:
			output_string = "USB input adapter: CONNECTED! \nBattery Capacity: " + batcap + "% \nUPS Output Voltage: " + vout + " mV \n\n"
			if i == 1:
				with open("/home/pi/log.txt","a+") as f:
					f.write(output_string)
				i += 1
			print("USB input adapter: CONNECTED!")
		print("Battery Capacity: "+batcap+"%")
		print("UPS Output Voltage: "+vout+" mV")

	print("Mains power disconnected, shutting down Raspberry Pi")
	output_string = "Mains power disconnected, shutting down Raspberry Pi \n"
	with open("/home/pi/log.txt","a+") as f:
		f.write(output_string)

	cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	stop_time = "Raspberry Pi shutdown initiated at:"+ cur_time + "\n\n"

	with open("/home/pi/log.txt","a+") as f:
		f.write(stop_time)

	os.system("sudo sync")
	time.sleep(1)
	os.system("sudo shutdown now -h")
	#print("Raspberry Pi *should* now be shutdown!")

if __name__ == "__main__":
	try:
		t1 = Thread( target = shutdown_check )
		t1.start()
	except:
		t1.stop()