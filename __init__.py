'''
<Mycroft skill to control LEDs on NodeMCU device. It calls the REST API from local Thinger server.>
    Copyright (C) <2018>  <Abhishek Mathur> <neoscreenager@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
import json
import requests

# Each skill is contained within its own class, which inherits base methods
# from the MycroftSkill class.

class NodeLightController(MycroftSkill):

  # The constructor of the skill, which calls MycroftSkill's constructor
  def __init__(self):
    super(NodeLightController, self).__init__(name="NodeLightController")
    # Initialize working variables used within the skill.

  @intent_handler(IntentBuilder("LightsOnOff").require("Color").require("State"))
  def handle_lights_onoff(self, message):
    # Initialize the URL for Thinger API
    GREEN_LED_URL = "http://192.168.0.101:80/v2/users/machunyu/devices/esp8266/greenled"
    # HEADERS = {'Authorization':'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXYiOiJlc3A4MjY2IiwiaWF0IjoxNTQwMzM5NjExLCJqdGkiOiI1YmNmYjc5YjY1MjNmODk2ZDE4Zjg4OTkiLCJyZXMiOlsiZ3JlZW5sZWQiXSwidXNyIjoibWFjaHVueXUifQ.bpUYOY5gV84Fbx3dpPRYT6cYpyEGI_J21sYKB7NfwZU'}
    RED_LED_URL = "http://192.168.0.101:80/v2/users/machunyu/devices/esp8266/redled"
    if message.data["State"] == "on":
      payload = {"in":True}
      self.speak_dialog("light.is.on",data={"Color":message.data["Color"],"State":message.data["State"]})
      if message.data["Color"] == "green":
        status = callThinger(GREEN_LED_URL,payload)
        if status == 1:
          self.speak_dialog("led.service.notreachable.dialog")
      elif message.data["Color"] == "red":
        status = callThinger(RED_LED_URL,payload)
        if status == 1:
          self.speak_dialog("led.service.notreachable.dialog")
    elif message.data["State"] == "off":
      payload = {"in":False}
      self.speak_dialog("light.is.on",data={"Color":message.data["Color"],"State":message.data["State"]})
      if message.data["Color"] == "green":
        status = callThinger(GREEN_LED_URL,payload)
        if status == 1:
          self.speak_dialog("led.service.notreachable.dialog")
      elif message.data["State"] == "off":
        status = callThinger(RED_LED_URL,payload)
        if status == 1:
          self.speak_dialog("led.service.notreachable.dialog")
    else:
      #self.speak_dialog("light.is.on", data={"Color": self.color})
      self.speak_dialog("how.are.you")
  
  @intent_handler(IntentBuilder("RoomTemp").require("Room").require("temperature"))
  def handle_roomTemp(self,message):
    # Initialize the URL for Thinger API
    ROOM_TEMPERATURE_URL = "http://192.168.0.101:80/v2/users/machunyu/devices/esp8266/temperature";
    HEADERS = {'Authorization':'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXYiOiJlc3A4MjY2IiwiaWF0IjoxNTQwMzM5NjExLCJqdGkiOiI1YmNmYjc5YjY1MjNmODk2ZDE4Zjg4OTkiLCJyZXMiOlsiZ3JlZW5sZWQiXSwidXNyIjoibWFjaHVueXUifQ.bpUYOY5gV84Fbx3dpPRYT6cYpyEGI_J21sYKB7NfwZU'}
    try:
      res = requests.get(ROOM_TEMPERATURE_URL,headers=HEADERS)
      # this line converts the response to a python dict which can then be parsed easily
      response_native = json.loads(res.text)
      self.speak_dialog("room.temperature.is",data={"temperature":response_native.get("out")})
      #print("Response temperature: ",response_native.get("out"))
    except requests.exceptions.RequestException as e:  # If unable to call the service
      self.speak_dialog("temperature.service.notreachable.dialog")
      print(e)
      
def callThinger(URL,data):
    HEADERS = {'Authorization':'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXYiOiJOb2RlTUNVIiwiaWF0IjoxNTI3MzMyNjYzLCJqdGkiOiI1YjA5M2YzNzIyN2MwMDMwN2RjMGEwNTUiLCJyZXMiOlsiZ3JlZW5sZWQiLCJyZWRsZWQiXSwidXNyIjoibmVvIn0.GXxXRJGcQgL-OPqS7UT3BKSyWmJ_qOVFtnCgHs8w_iw'}
    try:
      res = requests.get(URL, json=data,headers=HEADERS)
      return 0
    except requests.exceptions.RequestException as e:  # If unable to call the service
      print(e)
      return 1

    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, there is no need to override it.  If you DO
    # need to implement stop, you should return True to indicate you handled
    # it.
    #
    # def stop(self):
    #    return False

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return NodeLightController()
