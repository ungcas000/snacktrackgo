#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import json
from google.appengine.api import urlfetch
import jinja2
import os
import logging
import random


jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/home.html')
        self.response.write(template.render())

class ResultHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/result.html')
        self.response.write(template.render())

    def post(self):



        def get_calorie():
            raw_term = self.request.get('food', default_value="hunger games")
            term = raw_term.replace(" ", "+")
            if term == "":
                term = "can+you+not"
                pass
            food_source = urlfetch.fetch(
                'https://service.livestrong.com/service/food/foods/?query=' + term + '&limit=1&fill=cals')
            food_JSON = food_source.content
            calorie_dict = json.loads(food_JSON)
            calorie_number = int(calorie_dict['foods'][0]['cals'])
            return calorie_number;

        activity_list = {'run':1, 'walk':2, 'swim':3, 'bike':4, 'jog':5, 'boxing':6, 'yoga':7, 'pilates':8, 'dance':9, 'jump rope':10}
        i = 0
        for key, value in activity_list.range():
            gender = self.request.get('gender')
            gender = gender.lower()
            activity = key
            calorie = get_calorie()
            met = value
            food = self.request.get('food')
            height = int(self.request.get('height'))
            height = height * 2.54
            weight = int(self.request.get('weight'))
            weight = weight/2.2046
            age = int(self.request.get('age'))
            bmrw = (9.56 * weight) + (1.85 * height) - (4.68 * age) + 655
            bmrm = (13.75 * weight) + (5 * height) - (6.76 * age) + 66

            def get_time():

                if gender == "female":
                    return int(((calorie*24)/(met*bmrw))*60)

                elif gender == "male":
                    return int(((calorie*24)/(met*bmrm))*60)

            template = jinja_environment.get_template('templates/result.html')

            if i == 0:
                user_workout = {'food': food + ":", 'activity': activity,'calorie': str(calorie) + " calories", 'time': str(get_time()) + " minutes: "}

            else:
                user_workout = {
                            'activity': activity,
                            'time': str(get_time()) + " minutes: "}

            self.response.write(template.render(user_workout))

            i = 1;






app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/result', ResultHandler)
], debug=True)
