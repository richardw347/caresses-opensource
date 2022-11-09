# CAHRIM

The content of this folder have been released in October 2020 according the CARESSES release plan.

## Contractor Notes

I've refactored this repo to facilitate build and execution within a docker environment. This is mainly to deal with the Pepper-Python 2.7 dependencies. Quite a lot of python libraries have stopped supporting Python 2.7 as it's soon to be deprecated. What support remains is legacy and shaky at best.

Particularly to watch are the Choregraphe and pynaoqi dependnencies, given the situation around Aldebaran support of the pepper I think it's probably best to load these to a project repository where they can be maintained.

As long as the Docker images are maintained the system should be able to run without these external resources, it will just be an issue if the image needs to be rebuilt.

I will try and get the image to a fully functional state. Future work on the project should focus on migrating the code base however with the pepper stuck at Python 2.7 that doesn't seem trivial.

## Installation

```
docker pull richardw347/caress:latest
```

```
docker run -it richardw347/caress:latest
```

### Notes

Choreographe Key

Key : 654e-4564-153c-6518-2f44-7562-206e-4c60-5f47-5f45

(Obtained from : <https://developer.softbankrobotics.com/us-en/downloads/pepper> )

#### ActionsLib

##### [aux_files](ActionsLib/aux_files)

[approachObject](ActionsLib/aux_files/approachObject)

This is a object tracking project using the pepper robot, it used SIFT features and FLANN to track target objects. This appears to just be a stand alone demo and not connected to the rest of CAHRIM.

[go_to](ActionsLib/aux_files/go_to)

This is the navigation part of the CAHRIM system, It's a simple graph based map and A* planner with a TK-based utility to draw the maps. From what I can see the robot is relying mainly on Odometry for localisation which will be very unreliable.

[Navigations](ActionsLib/aux_files/Navigations)

This is another standalone project using ROS 1, gmapping and the navigation stack to try and get the pepper to navigate autonomously. The pepper has very limited, noisy distance sensors so this doesn't work very well at all and this isn't integrated into the rest of CAHRIM.

[youtube_helper](ActionsLib/aux_files/youtube_helper)

This module provides two functions, first it creates a local SQLLite database to keep a history of videos watched. Second it provides a number of API helper functions for interacting with youtube including search, retrieving duration and video ids.

[avoidObstacles](ActionsLib/aux_files/avoidObstacles.py)

This is another standalone demo using the front lasers on the pepper robot to move forward while avoiding obstacles.

[city-list](ActionsLib/aux_files/city-list.json)

A json doc of cities including latitude and longitude coordinates. This is used in the display_weather_report.py action

[email-conf](ActionsLib/aux_files/email-conf.json)

A json doc with a sender email address configuration for the take_send_picture.py action

[images](ActionsLib/aux_files/images.csv)

A CSV file with image links, this is used within the chitchat.py action

[meals-conf](ActionsLib/aux_files/meals-conf.json)

A json doc with menu data used within the read_menu.py action

[memorygames-conf](ActionsLib/aux_files/memorygames-conf.json)

A json doc with configuration files for the memory game played on peppers tablet, see play_game_memory.py

[read_news_lib](ActionsLib/aux_files/read_news_lib.py)

A library to access news feeds using the BeautifulSoup XML/HTML parser

[weather-conf](ActionsLib/aux_files/weather-conf.json)

A json object with weather based translations for the display_weather_report.py action

##### [caressestools](ActionsLib/caressestools)

[caressestools](ActionsLib/caressestools/caressestools.py)

A bunch of helper functions for interfacing with the pepper robot and loading the main caresses-conf.json file.

[choice_manager](ActionsLib/caressestools/choice_manager.py)

A helper class to display a choice on the tablet and capture the answer either verbally or on the tablet.

[custom_number](ActionsLib/caressestools/custom_number.py)

A helper class to get the user to input a custom number

[date_time_selector](ActionsLib/caressestools/date_time_selector.py)

A helper class to display a date time selector on the tablet

[input_request_parser](ActionsLib/caressestools/input_request_parser.py)

A helper class to parse a JSON file into an ordered dictionary

[logprocesser](ActionsLib/caressestools/logprocesser.py)

A helper class to process the speech logs into a more readable format

[multipage_choice_manager](ActionsLib/caressestools/multipage_choice_manager.py)

A helper class to create a multi-page choice dialog on the tablet

[speech_conf](ActionsLib/caressestools/speech_conf.json)[speech](ActionsLib/caressestools/speech.py)

A json configuration file for the speech.py class that handles conversation/dialog generation for the robot

[timedateparser_conf](ActionsLib/caressestools/timedateparser_conf.json)[timedateparser](ActionsLib/caressestools/timedateparser.py)

A class and configuration file that handles date parsing

##### [NAOqi_apps](ActionsLib/NAOqi_apps)

[asr2](ActionsLib/NAOqi_apps/asr2)

A speech recognition library for pepper

[Caresses_Multimedia](ActionsLib/NAOqi_apps/Caresses_Multimedia)

????

[choice_manager_app](ActionsLib/NAOqi_apps/choice_manager_app)

The application to support the choice manager action

[Compilation](ActionsLib/NAOqi_apps/Compilation)

A collection of gestures for pepper

[CustomNumber](ActionsLib/NAOqi_apps/CustomNumber)

The application to support the custom number action

[DateSelector](ActionsLib/NAOqi_apps/DateSelector)

The application to support the date selector action

[display_user_emotion_APP](ActionsLib/NAOqi_apps/display_user_emotion_APP)

The application to support the display user emotion action

[display_weather_report_APP](ActionsLib/NAOqi_apps/display_weather_report_APP)

The application to support the display weather report action

[game_memory_APP](ActionsLib/NAOqi_apps/game_memory_APP)

The application to support the memory game action

[learn_user_face](ActionsLib/NAOqi_apps/learn_user_face)

The application to support the learn user face action

[pictures_APP](ActionsLib/NAOqi_apps/pictures_APP)

The application to support the capture and send picture action

[play_youtube_APP](ActionsLib/NAOqi_apps/play_youtube_APP)

The application to support the play youtube action

[read_temperature_APP](ActionsLib/NAOqi_apps/read_temperature_APP)

The application to support the read temperature action

[Time12Selector](ActionsLib/NAOqi_apps/Time12Selector)[Time24Selector](ActionsLib/NAOqi_apps/Time24Selector)

The application to support the time selector action

##### [parameters](ActionsLib/parameters)

Json files with conversational configurations for various actions chitchat, reminders, videos, weather.

##### [RobotGestures](ActionsLib/RobotGestures)

A ML model and associated interface code to automatically generate pepper physical animations to go along with speech.

##### [action.py](ActionsLib/action.py)

Parent class for all actions in the library, all actions are triggered by CSPEM.

#### CAHRIM Threads

[actuation_hub.py](CahrimThreads/actuation_hub.py)
This is the main action execution thread, it pulls all the actions from ActionsLib and contains a number of classes:

* Executor: this class is responsible for parsing a goal message from CSPEM and launching a action in a new Thread
* StateObserver: this class monitors the execution of all the actions
* RunAction: this class creates a thread to execute an action within
* StopAction: spawns a thread to stop an action executing

[behaviour_pattern_estimator.py](CahrimThreads/behaviour_pattern_estimator.py)
This contains a threaded class that does nothing

[pose_viewer.py](CahrimThreads/pose_viewer.py)
The thread creates a TK window displaying the map and the current robot position

[sensory_hub.py](CahrimThreads/sensory_hub.py)
The module contains various classes with varying sensory functions:

* DBObserver: Does nothing
* OdomConverter: Converts pepper odom coordinates to maps coordinates, reading and writing to ALMemory
* DetectUserDepth: Determines how far away the user is from the robot using pepper People Perception module
* Person: Class to keep track of people using facial recognition
* VocalEmotionEstimator: This class is commented out and appears incomplete, there is a copy of the OpenVokaturi library <https://developers.vokaturi.com/getting-started/overview> in the CahrimThreads folder
* EstimateUserEmotion: Uses pepper ALFaceCharacteristics service to determine users emotional state within the range of neutral, happy, surprised, angry, sad

[socket_handlers.py](CahrimThreads/socket_handlers.py)

* Looks like character-based protocol for message passing between components of the system. That's a critical issue to resolve in progressing the project to the future. Message definitions form a contract between sender and receiver text-based protocols do nothing to preserver the contract!
* Also there's not much error handling in the socket communications, replacing these with a modern IPC library is a must

[speech_volume_estimator.py](CahrimThreads/speech_volume_estimator.py)

Uses deep reinforcement learning model to estimate speaker volume level, requires tensorflow, and keras. Not clear yet how this value is used if at all.

[user_behaviour_analysis.py](CahrimThreads/user_behaviour_analysis.py)

Appears to use sensor data from an external sensor network (IOT) to estimate user location and behavior (Sleeping/Eating). This sensor data is pushed into a mysql database which is then read by the python module. Results are sent using an outputhandler from the socket handlers. Assuming this message goes to CSPEN. There is a JAR file for a simulator to replicate the sensor network and push fake data into the database.

#### Google API Client

As per this issue <https://github.com/grpc/grpc/issues/23190> the default install for the api client installs an incompatible version of the RSA library it is necessary to uninstall it and install v4.0.

```
pip uninstall rsa
pip install -v rsa==4.0
```

## Changelog

* Added requirements.txt for all python dependencies
* Added Dockerfile with system and pepper dependencies
