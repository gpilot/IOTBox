import serial
import time
import json
import urllib2


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
		print "Error sending data: ", e,
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
	print "Error reading config file"
else:
	try:
		#read file
		pathToFile = "/var/log/sensors/temp"
		lines = open(pathToFile).readlines()
		#lines = fr
		#fr.close()
	except:
		print "Error reading temporary file"
	else:
		while len(lines)>0:
			try:
				#send result to server
				data_str = dict(version="1.0.0",datastreams=[])
				for i, line in enumerate(lines[:]):
					line=line.replace('\n', '')
					#print line
					if i>=50:
						break
					else:
						#print len(line)
						if len(line)>0:
							#if ";" in line:
							lineSplitVal = line.split(";")
							data_str["datastreams"].append(dict(date_time=lineSplitVal[0],polluant=lineSplitVal[1], value=lineSplitVal[2]))
							#print (i, " : ", lineSplitVal[1], "=", lineSplitVal[2])
							#print (i, " line:" , lines[i])
							#print lines
						#on lit puis on supprime lentree dans le tableau la valeur a supprimer est toujours la premiere entree du tableau donc 0
						del lines[0]
						#print lines
						#print "_"
				if len(data_str)>0:
					#print json.dumps(data_str["datastreams"])
					res = send_data('https://greenservices.inria.fr:8443/gs_api/rest/data_store/list', apiKey, uniqueID, json.dumps(data_str["datastreams"]))
					if res==-1:
						print "Failed to send Data"
					else:
						try:
							open(pathToFile, "w").writelines(lines)
							fr = open(pathToFile, "r")
							lines = fr.readlines()
							fr.close()
							#print(i, len(lines))
						except:
							print "Failed to clear lines in temporary file"
			except:
				print "Failed to send data to server"
			time.sleep(5)