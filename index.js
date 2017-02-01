'use strict';

var Alexa = require('alexa-sdk');

require('dotenv').config();

var SKILL_NAME = 'Caregiver';

exports.handler = function(event, context, callback) {
    var alexa = Alexa.handler(event, context);
    alexa.APP_ID = APP_ID;
    alexa.registerHandlers(handlers);
    alexa.execute();
};

var handlers = {
    'LaunchRequest': function () {
        this.emit('AMAZON.HelpIntent');
    },
    'GetMedicineIntent': function () {
        var patientSlot = this.event.request.intent.slots.Patient;
        var patientName;
        if (patientSlot && patientSlot.value) {
            patientName = patientSlot.value;

            var cardTitle = SKILL_NAME + " Time Medication Taken By - " + patientName;
            var time = "7:15am";
            var speechOutput = patientName + "took their medication at " + time;
            this.emit(':tellWithCard', speechOutput, SKILL_NAME,
                      cardTitle, time);

          } else {
            var speechOutput =
                'I\'m sorry, I don\'t know when ' + patientName + ' took their medication';
            this.emit(':tell', speechOutput);
          }
    },
    'GetWakeTimeIntent': function() {
    	var patientSlot = this.event.request.intent.slots.Patient;
        var patientName;
        if (patientSlot && patientSlot.value) {
            patientName = patientSlot.value;

            var cardTitle = SKILL_NAME + " Wake Up Time For - " + patientName;
            var time = "7:00am";
            var speechOutput = patientName + "woke up at " + time;
            this.emit(':tellWithCard', speechOutput, SKILL_NAME,
                      cardTitle, time);

          } else {
            var speechOutput =
                'I\'m sorry, I don\'t know when ' + patientName + 'woke up';
            this.emit(':tell', speechOutput);
          }
    },
    'AMAZON.HelpIntent': function () {
        var speechOutput = "You can say when or what time did the patient take their medication, or, " +
                           "You can say when or what time did the patient wake up, or, " +
                           "you can say exit... What can I help you with?";
        var reprompt = "What can I help you with?";
        this.emit(':ask', speechOutput, reprompt);
    },
    'AMAZON.CancelIntent': function () {
        this.emit(':tell', 'Goodbye!');
    },
    'AMAZON.StopIntent': function () {
        this.emit(':tell', 'Goodbye!');
    }
};
