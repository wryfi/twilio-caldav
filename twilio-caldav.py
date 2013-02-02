#!/usr/bin/env/python

import os
import cherrypy
from classes import Root

def main():

    # Some global configuration; note that this could be moved into a
    # configuration file 
    cherrypy.config.update({
        'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
        'tools.decode.on': True,
        'tools.trailing_slash.on': True,
        'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__)),
        'server.socket_host': '0.0.0.0',
    })  

    cherrypy.quickstart(Root(), '/', {})  

if __name__ == '__main__':
    main()
