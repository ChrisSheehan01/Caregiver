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

@ask.intent("GetMedicineIntent")
def medicineTime(patient):
	medicineMsg = patient + 'took medicine at 7 15 AM.'
	return question(medicineMsg).reprompt(questionMsg)

@ask.intent("GetWakeTimeIntent")
def wakeTime(patient):
	wakeTimeStatement = patient + 'woke up at 7 AM.'
	return question(wakeTimeStatement).reprompt(questionMsg)
	
@ask.intent("GetMemoryGameTimeIntent")
def memGameTime(patient):
	memGameTimeMsg = patient
	memGameDictArray = getData('memoryGame') 
	# user(string), score(number), time(timestamp(ISO 8601 date))
	if "time" in memGameDictArray[0]:
		memGameTimeMsg = memGameTimeMsg + ' last took memory Quiz at: ' + memGameDictArray[0].get("time")
	else:
		memGameTimeMsg = 'There is no recorded time for the last memory quiz taken by ' + patient
	return question(memGameTimeMsg).reprompt(questionMsg)

@ask.intent("GetMemoryGameScoreIntent")
def memGameScore(patient):
	memGameScoreMsg = patient
	memGameDictArray = getData('memoryGame')
	# user(string), score(number), time(timestamp(ISO 8601 date))
	if "score" in memGameDictArray[0]:
		memGameScoreMsg = memGameScoreMsg + ' last score for the memory Quiz was: ' + memGameDictArray[0].get("score")
	else:
		memGameScoreMsg = 'There is no score for the last time ' + patient + ' took their memory quiz.'
	return question(memGameScoreMsg).reprompt(questionMsg)

@ask.intent("GetMemoryGameTimeAndScoreIntent")
def memGameTimeAndScore(patient):
	memGameFullMsg = patient
	memGameDictArray = getData('memoryGame') 
	# user(string), score(number), time(timestamp(ISO 8601 date))
	if "time" in memGameDictArray[0] and "score" in memGameDictArray[0]:
		memGameFullMsg = memGameFullMsg + ' last took memory Quiz at: ' + memGameDictArray[0].get("time") + " and their score was " + memGameDictArray[0].get("score")
	else:
		memGameFullMsg = 'There is a missing time or score for the last memory quiz taken by ' + patient
	return question(memGameFullMsg).reprompt(questionMsg)

@ask.intent("GetGPSIntent")
def gps(patient):
	gpsMsg = patient
	gpsDictArray = getData('gps') 
	# available: deviceID(string), time(timestamp(ISO 8601 date)), lat(number), lon(number) address(string)
	if "lat" in gpsDictArray[0] and "lon" in gpsDictArray[0] and "time" in gpsDictArray[0]:
		lat = str(gpsDictArray[0].get("lat"))
		lon = str(gpsDictArray[0].get("lon"))
		time = str(gpsDictArray[0].get("time"))
		gpsMsg = patient + 's last logged location was latitude: ' + lat + ' and longitude: ' + lon + " on " + time
	else:
		gpsMsg = 'latitude and longitude not available for ' + patient
	return question(gpsMsg).reprompt(questionMsg)
	
@ask.intent("GetWemoIntent")
def wemo(patient):
	wemoMsg = patient
	wemoDictArray = getData('wemo') 
	# available: date(string), time(string), status(boolean) off
	# status: true-on, false-off
	if "status" in wemoDictArray[0] and "time" in wemoDictArray[0] and "date" in wemoDictArray[0]:
		if wemoDictArray[0].get("status") == True:
			wemoMsg = wemoMsg + " lights have been on since " + wemoDictArray[0].get("time") + " on " + wemoDictArray[0].get("date")
		else:
			wemoMsg = wemoMsg + " lights have been off since " + wemoDictArray[0].get("time") + " on " + wemoDictArray[0].get("date")
	return question(wemoMsg).reprompt(questionMsg)

@ask.intent("EndCaregiver")
def endCaregiver():
	endMsg = "Shutting down Caregiver, goodbye!"
	return statement(endMsg)

# returns array of dict objects
def getData(endpoint_url):
	full_url = url_to_use + '/' + endpoint_url
	requestedAPIPage = requests.get(full_url)
	return requestedAPIPage.json()
  
if __name__ == '__main__':
	app.run(debug=True)  
