import serial
import time
import datetime
import json
import urllib2

pathToDirectory = "/var/log/sensors/"
pathToLogFile = pathToDirectory+"error/sendValues-"+datetime.datetime.now().strftime('%Y-%m-%d')

def writeLog(str):
	fwLogFile = open(pathToLogFile, "a")
	fwLogFile.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	fwLogFile.write(";")
	fwLogFile.write(str)
	fwLogFile.write("\n")
	fwLogFile.close()

def send_data(url, apikey, platkey, content):
	opener = urllib2.build_opener(urllib2.HTTPSHandler)
	request = urllib2.Request(url, data=content)
	request.add_header('Content-Type', 'application/json')
	request.add_header('GS_API_KEY', apikey)
	request.add_header('GS_PLAT_KEY', platkey )
	request.get_method = lambda: 'POST'
	try:
		res = opener.open(request, timeout=120)
	except urllib2.URLError,e:
		writeLog("Error sending data: ", e)
		#print "Error sending data: ", e,
		return -1

#read Config
try:
	fr = open("/var/www/sys/apikey", "r")
	apiKey = fr.read().replace('\n', '')
#	print apiKey
	fr.close()

	fr = open("/var/www/sys/uniqueID", "r")
	uniqueID = fr.read().replace('\n', '')
#	print uniqueID
	fr.close()
except:
	writeLog("Error reading config file")
	#print "Error reading config file"
else:
	try:
		#read file
		pathToFile = "/var/log/sensors/temp"
		lines = open(pathToFile).readlines()
		#lines = fr
		#fr.close()
	except:
		writeLog("Error reading temporary file")
		#print "Error reading temporary file"
	else:
		while len(lines)>0:
			try:
				#send result to server
				data_str = dict(version="1.0.0",datastreams=[])
				for i, line in enumerate(lines[:]):
					line=line.replace('\n', '')
					if i>=50:
						break
					else:
						if len(line)>0:
							lineSplitVal = line.split(";")
							data_str["datastreams"].append(dict(date_time=lineSplitVal[0],polluant=lineSplitVal[1], value=lineSplitVal[2]))
						#on lit puis on supprime lentree dans le tableau la valeur a supprimer est toujours la premiere entree du tableau donc 0
						del lines[0]
				if len(data_str)>0:
					#print json.dumps(data_str["datastreams"])
					res = send_data('https://greenservices.inria.fr:8443/gs_api/rest/data_store/list', apiKey, uniqueID, json.dumps(data_str["datastreams"]))
					if res==-1:
						writeLog("Failed to send Data")
						#print "Failed to send Data"
					else:
						try:
							fw = open(pathToFile, "w")
							fw.writelines(lines)
							fw.close()
							#fr = open(pathToFile, "r")
							#lines = fr.readlines()
							#fr.close()
							#print(i, len(lines))
						except:
							writeLog("Failed to clear lines in temporary file")
							print "Failed to clear lines in temporary file"
			except:
				writeLog("Failed to send data to server")
				print "Failed to send data to server"
			time.sleep(5)
fwLogFile.close()