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

    	#Don't touch this part of the code!###############################################################
    	raw_term = self.request.get('term', default_value="hunger games")								 #
        term = raw_term.replace(" ", "+")																 #
        if term == "":																					 #
            term = "can+you+not"																		 #
            pass																						 #
        food_source = urlfetch.fetch(																	 #
            'https://service.livestrong.com/service/food/foods/?query=' + term + '&limit=1&fill=cals')   #
        food_JSON = food_source.content																	 #
        calorie_dict = json.loads(food_JSON)															 #
        calorie = int(calorie_dict['foods'][0]['cals'])												 #
		#Seriously, don't touch abouve this line!#########################################################

        gender = self.request.get('gender')
        activity = 
        calorie =
        met =
        height = self.request.get('height')
        weight = self.request.get('weight')
        age = self.request.get('age')
        bmrw = (9.56 * weight) + (1.85 * height) - (4.68 * age) + 655
        bmrm = (13.75 * weight) + (5 * height) - (6.76 * age) + 66

        if gender == female:
            return self.response.out.write(template.render({
                        'activity': activity,
                        'calorie': calorie,
                        'time': (calorie*24)/(met*bmrw)}))

        if gender == male:
            return self.response.out.write(template.render({
                        'activity': activity,
                        'calorie': calorie,
                        'time': (calorie*24)/(met*bmrm)}))




app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/result', ResultHandler)
], debug=True)
