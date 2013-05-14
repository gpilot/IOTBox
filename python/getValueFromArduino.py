import serial
import time
import datetime
import sys
import signal

pathToDirectory = "/var/log/sensors/"
pathToLogFile = pathToDirectory+"error/getValues-"+datetime.datetime.now().strftime('%Y-%m-%d')

def writeLog(str):
	fwLogFile = open(pathToLogFile, "a")
	fwLogFile.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	fwLogFile.write(";")
	fwLogFile.write(str)
	fwLogFile.write("\n")
	fwLogFile.close()

def is_numeric(lit):
    'Return value of numeric literal string or ValueError exception'
 
    # Handle '0'
    if lit == '0': return 0
    # Hex/Binary
    litneg = lit[1:] if lit[0] == '-' else lit
    if litneg[0] == '0':
        if litneg[1] in 'xX':
            return int(lit,16)
        elif litneg[1] in 'bB':
            return int(lit,2)
        else:
            try:
                return int(lit,8)
            except ValueError:
                pass
 
    # Int/Float/Complex
    try:
        return int(lit)
    except ValueError:
        pass
    try:
        return float(lit)
    except ValueError:
        pass
    return complex(lit)

locations=['/dev/ttyACM0','/dev/ttyACM1','/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2','/dev/ttyUSB3','/dev/ttyS0','/dev/ttyS1','/dev/ttyS2', 'COM26', 'COM22']
for device in locations:
	try:
		#print ("Trying...", device)
		arduino = serial.Serial(device, 9600, timeout=5)
		break
	except:
		arduino = None
		#writeLog("Failed to connect to USB Serial")
		#print ("Failed to connect on",device)
if arduino is not None:
	while 1:
		try:
			lineArduino = arduino.readline()
			if len(lineArduino) > 0 and lineArduino!="\n":
				lineArduino=lineArduino.split("\n")[0]
				for keyVal in lineArduino.split(";"):
					keyValNet=keyVal.rstrip()
					print (keyValNet)
					keyValSplit = keyValNet.split('=')
					#Write data in file
					if len(keyValSplit)==2:
						label = keyValSplit[0]
						value = keyValSplit[1]
						print (label)
						print (value)
						try:
							if (isinstance(is_numeric(value), float)) or (isinstance(is_numeric(value), int)):
								pathToFile = "/var/log/sensors/"+datetime.datetime.now().strftime('%Y-%m-%d')
								fw = open(pathToFile, "a")
								fw.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
								fw.write(";")
								fw.write(label)
								fw.write(";")
								fw.write(value)
								fw.write("\n")
								fw.close()
								
								pathToFile ="/var/log/sensors/temp"
								fw = open(pathToFile, "a")
								fw.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
								fw.write(";")
								fw.write(label)
								fw.write(";")
								fw.write(value)
								fw.write("\n")
								fw.close()
							else:
								#print ("error data type")
								writeLog("Error data type")
						except:
							#print ("error value")
							writeLog("Error value")
		except:
			#print ("error arduino")
			writeLog("Error arduino")
			arduino.close()
			sys.exit()
		time.sleep(5)
else:
	writeLog("Arduino connection error")