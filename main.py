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

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/index.html')
        self.response.out.write(template.render())

    def post(self):
        raw_term = self.request.get('term', default_value="hunger games")
        term = raw_term.replace(" ", "+")
        if term == "":
            term = "can+you+not"
            pass
        food_source = urlfetch.fetch(
            'https://service.livestrong.com/service/food/foods/?query=' + term + '&limit=1&fill=cals')
        food_JSON = food_source.content
        calorie_dict = json.loads(food_JSON)
        self.response.write(int(calorie_dict['foods'][0]['cals']))


        #self.response.write("<html>" + calories + "</html>")
       

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
