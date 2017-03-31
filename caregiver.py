import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import requests
import time

app = Flask(__name__)
ask = Ask(app, "/")
noEndpointMsg = 'no endpoint exists'
logging.getLogger("flask_ask").setLevel(logging.DEBUG)
local_url = 'http://localhost:8080/api'
pegasus_ngrok_url = 'https://8887eddd.ngrok.io/api'
url_to_use = pegasus_ngrok_url
questionMsg = 'Any other questions?'

def print_response(webPage):
    print "Request Url: ", webPage.url
    print "Response Status: ", webPage.status_code
    print "Response JSON: ", webPage.json()
        
@ask.launch
def start_caregiver():
	startMsg = 'Welcome to Caregiver.'
	return question(startMsg)
	#return statement(startMsg)

@ask.intent("GetMedicineIntent")
def medicineTime(patient):
	medicineMsg = patient + 'took medicine at 7 15 AM.'
	return question(medicineMsg).reprompt(questionMsg)
	#return statement(medicineMsg)

@ask.intent("GetWakeTimeIntent")
def wakeTime(patient):
	wakeTimeStatement = patient + 'woke up at 7 AM.'
	return question(wakeTimeStatement).reprompt(questionMsg)
	#return statement(wakeTimeStatement)

@ask.intent("GetMemoryGameIntent")
def memGame(patient):
	memGameDictArray = getData('memoryGame')
	newMemGameData = memGameDictArray[0]
	# data available: user(string), score(number), time(timestamp(ISO 8601 date))
	if "time" in newMemGameData and "score" in newMemGameData:
		time = convertTimeStamp(newMemGameData.get("time"))
		score = newMemGameData.get("score")
	memGameMsg = patient + " played memory game on " + str(time) + " and received a score of " + str(score)
	return question(memGameMsg).reprompt(questionMsg)
	#return statement(memGameMsg)

@ask.intent("GetMemoryGameTimeIntent")
def memGameTime(patient):
	memGameTimeMsg = patient
	memGameTimeDictArray = getData('memoryGame')
	# data available: user(string), score(number), time(timestamp(ISO 8601 date))
	if "time" in memGameTimeDictArray[0]:
		time = convertTimeStamp(str(memGameTimeDictArray[0].get("time")))
		memGameTimeMsg = memGameTimeMsg + ' last took memory Quiz at: ' + time
	else:
		memGameTimeMsg = 'There is no recorded time for the last memory quiz taken by ' + patient
	return question(memGameTimeMsg).reprompt(questionMsg)
	#return statement(memGameTimeMsg)

@ask.intent("GetMemoryGameScoreIntent")
def memGameScore(patient):
	memGameScoreMsg = patient
	memGameScoreDictArray = getData('memoryGame')
	# data available: user(string), score(number), time(timestamp(ISO 8601 date))
	if "score" in memGameScoreDictArray[0]:
		memGameScoreMsg = memGameScoreMsg + ' last score for the memory Quiz was: ' + str(memGameScoreDictArray[0].get("score"))
	else:
		memGameScoreMsg = 'There is no score for the last time ' + patient + ' took their memory quiz.'
	return question(memGameScoreMsg).reprompt(questionMsg)
	#return statement(memGameScoreMsg)

@ask.intent("GetMemoryGameTimeAndScoreIntent")
def memGameTimeAndScore(patient):
	memGameFullMsg = patient
	memGameFullDictArray = getData('memoryGame')
	# data available: user(string), score(number), time(timestamp(ISO 8601 date))
	if "time" in memGameFullDictArray[0] and "score" in memGameFullDictArray[0]:
		memGameFullMsg = memGameFullMsg + ' last took memory Quiz at: ' + str(memGameFullDictArray[0].get("time")) + " and their score was " + str(memGameFullDictArray[0].get("score"))
	else:
		memGameFullMsg = 'There is a missing time or score for the last memory quiz taken by ' + patient
	return question(memGameFullMsg).reprompt(questionMsg)
	#return statement(memGameFullMsg)

@ask.intent("GetGPSIntent")
def gps(patient):
	gpsMsg = patient
	gpsDictArray = getData('gps') 
	# data available: deviceID(string), time(timestamp(ISO 8601 date)), lat(number), lon(number) address(string)
	if "lat" in gpsDictArray[0] and "lon" in gpsDictArray[0] and "time" in gpsDictArray[0]:
		lat = str(gpsDictArray[0].get("lat"))
		lon = str(gpsDictArray[0].get("lon"))
		time = convertTimeStamp(str(gpsDictArray[0].get("time")))
		gpsMsg = patient + 's last logged location was latitude: ' + str(lat) + ' and longitude: ' + str(lon) + " on " + str(time)
	else:
		gpsMsg = 'latitude and longitude not available for ' + patient
	return question(gpsMsg).reprompt(questionMsg)
	#return statement(gpsMsg)
	
@ask.intent("GetWemoIntent")
def wemo(patient):
	wemoMsg = patient
	wemoDictArray = getData('wemo') 
	# data available: date(string), time(string), status(boolean) off
	# status: true-on, false-off
	if "status" in wemoDictArray[0] and "time" in wemoDictArray[0] and "date" in wemoDictArray[0]:
		if wemoDictArray[0].get("status") == True:
			wemoMsg = wemoMsg + " lights have been on since " + str(wemoDictArray[0].get("time")) + " on " + str(wemoDictArray[0].get("date"))
		else:
			wemoMsg = wemoMsg + " lights have been off since " + str(wemoDictArray[0].get("time")) + " on " + str(wemoDictArray[0].get("date"))
	return question(wemoMsg).reprompt(questionMsg)
	#return statement(wemoMsg)

@ask.intent("EndCaregiver")
def endCaregiver():
	endMsg = "Shutting down Caregiver, goodbye!"
	return statement(endMsg)

# returns array of Dictionary objects
def getData(endpoint_url):
	full_url = url_to_use + '/' + endpoint_url
	requestedAPIPage = requests.get(full_url)
	return requestedAPIPage.json()

def convertTimeStamp(time):
#2017-03-30T19:28:38.136Z
	timeArray = time.split("T")
	date = timeArray[0]#.split("-")
	time = timeArray[1].split(":")[0] + ":" + timeArray[1].split(":")[1]
	newTime = date + " " + time
	return newTime

  
if __name__ == '__main__':
	app.run(debug=True)  
