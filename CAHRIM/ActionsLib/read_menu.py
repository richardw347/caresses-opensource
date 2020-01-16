# -*- coding: utf-8 -*-
'''
Copyright October 2019 Roberto Menicatti & Università degli Studi di Genova

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

***

Author:      Roberto Menicatti
Email:       roberto.menicatti@dibris.unige.it
Affiliation: Laboratorium, DIBRIS, University of Genova, Italy
Project:     CARESSES (http://caressesrobot.org/en/)
'''
import json
import os

from action import Action
import caressestools.caressestools as caressestools
import caressestools.speech as speech


## Action "Read Menu".
#
#  Pepper reads aloud the meals menu of the day of the care home, written in the file aux_files/meals-conf.json.
class ReadMenu(Action):

    ## The constructor.
    # @param self The object pointer.
    # @param apar (string) Meal, moment of the day
    # @param cpar (string) Volume, speed, pitch, language, username; separated by a white space. <b>Volume</b>, <b>speed</b> and <b>pitch</b> must be compliant with NAOqi ALTextToSpeech requirements. <b>Language</b> must be the full language name lowercase (e.g. english).
    # @param session (qi session) NAOqi session.
    # @param asr (string) Environment noise level, either "normal" or "noisy".
    def __init__(self, apar, cpar, session, asr):
        Action.__init__(self, apar, cpar, session)

        # Parse the action parameters
        self.apar = self.apar.split(' ')

        self.meal_id = self.apar[0]
        self.day_moment = self.apar[1]

        # Parse the cultural parameters
        self.cpar = self.cpar.split(' ')

        self.volume = float(self.cpar[0])
        self.speed = float(self.cpar[1])
        self.pitch = float(self.cpar[2])
        self.language = self.cpar[3].lower().replace('"', '')
        self.username = self.cpar[4].replace('"', '')

        self.meals_params = self.loadParameters("meals.json")

        meal_conf = os.path.join(os.path.dirname(os.path.realpath(__file__)), "aux_files", "meals-conf.json")
        with open(meal_conf) as f:
            self.meals = json.load(f)

        self.meals_IDs = [m.encode('utf-8') for m in self.meals.keys() if not self.meals[m.encode('utf-8')] == []]
        self.meals_options = self.getAllParametersAttributes(self.meals_params, self.meals_IDs, "full")

        # Initialize NAOqi services

        # Set the cultural parameters
        caressestools.Language.setLanguage(self.language)

        caressestools.setRobotLanguage(session, caressestools.Language.lang_naoqi)
        caressestools.setVoiceVolume(session, self.volume)
        caressestools.setVoiceSpeed(session, self.speed)
        caressestools.setVoicePitch(session, self.pitch)

        # Set up speech.py app to get information
        self.sp = speech.Speech("speech_conf.json", self.language)
        self.sp.enablePepperInteraction(session, caressestools.Settings.robotIP.encode('utf-8'))
        self.asr = asr

    ## Method executed when the thread is started.
    def run(self):
        
        if len(self.meals_options) == 0:
            self.sp.monolog(self.__class__.__name__, "1", tag=speech.TAGS[1])
            self.end()
            return

        if not self.isAvailable(self.meal_id):
            self.meal_full = self.sp.dialog(self.__class__.__name__, self.meals_options,
                                                    checkValidity=True, askForConfirmation=True, noisy=self.asr)
            self.meal_id = self.getIDFromAttribute(self.meals_params, "full", self.meal_full)
        else:
            self.meal_full = self.getAttributeFromID(self.meals_params, self.meal_id, "full")
            self.sp.monolog(self.__class__.__name__, "with-keyword", param={"$KEYWORD$": self.meal_full},
                            group="parameter-answer", tag=speech.TAGS[1])

        menu = (", ").join(self.meals[self.meal_id])

        self.sp.monolog(self.__class__.__name__, "0", param={"$MEAL$": self.meal_full, "$MENU$": menu}, tag=speech.TAGS[1])

        self.sp.askYesOrNoQuestion(
            self.sp.script[self.__class__.__name__]["evaluation"]["0"][self.language].encode('utf-8'), speech.TAGS[3], noisy=self.asr)
        self.sp.monolog(self.__class__.__name__, "1", group="evaluation", tag=speech.TAGS[1])

        self.end()

    ## Method containing all the instructions that should be executing before terminating the action.
    def end(self):
        pass


if __name__ == "__main__":

    import qi
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default=caressestools.Settings.robotIP,
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()

    try:
        # Initialize qi framework.
        session = qi.Session()
        session.connect("tcp://" + args.ip + ":" + str(args.port))
        print("\nConnected to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) + ".\n")

    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) + ".\n"
                                                                                              "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    caressestools.Settings.robotIP = args.ip

    # Run Action
    apar = '"n/a" "n/a"'
    cpar = "1.0 100 1.1 english John"

    caressestools.startPepper(session, caressestools.Settings.interactionNode)
    action = ReadMenu(apar, cpar, session, "normal")

    try:
        action.run()
    except speech.StopInteraction as e:
        print e
