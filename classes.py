from cal import get_caldav_contact
import cherrypy
import twilio.twiml
from twilio.rest import TwilioRestClient
from settings import twilio_account_ssid, twilio_auth_token, twilio_phone_number, sms_reply, voice_reply

class Root(object):

  @cherrypy.expose
  def index(self, **params):
    return 'hello, browser monkey'

  @cherrypy.expose
  def voice(self, **params):
    response = twilio.twiml.Response()
    response.say(voice_reply)
    response.dial(get_caldav_contact()[1], timeLimit=300)
    return str(response)

  @cherrypy.expose
  def txt(self, **params):
    response = twilio.twiml.Response()
    response.sms(sms_reply)
    if 'Body' in params.keys():
      sms_body = 'From %s:  ' % params['From']
      sms_body += params['Body']
      client = TwilioRestClient(twilio_account_ssid, twilio_auth_token)
      message = client.sms.messages.create(to=get_caldav_contact()[1], from_=twilio_phone_number, body=sms_body)
    return str(response) 
