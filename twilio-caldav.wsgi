#!/usr/bin/env/python

import os
import site
import sys

prev_sys_path = list(sys.path)

appDir = os.path.dirname(os.path.realpath( __file__ ))
site.addsitedir(appDir)

import settings

vEnv = settings.virtualenv_path
site.addsitedir(vEnv)

new_sys_path = [] 
for item in list(sys.path): 
  if item not in prev_sys_path: 
    new_sys_path.append(item) 
    sys.path.remove(item) 

sys.path[:0] = new_sys_path 

import cherrypy
from classes import Root

cherrypy.config.update({'environment': 'embedded'})
sys.stdout = sys.stderr

application = cherrypy.Application(Root(), script_name=None, config=None)
