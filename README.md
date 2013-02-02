# twilio-caldav

This is a dead simple [cherrypy](http://www.cherrypy.org) app that uses the [caldav](http://pypi.python.org/pypi/caldav) python library to decide who to forward voice and sms messages to based on calendar data.

## summary/usage

You need a caldav calendar. I've tested with Zimbra. The code uses the ical 'summary' field (the event name in Zimbra or Google calendar) for a contact name and the ical 'location' field for an [E.164-formatted]( http://www.twilio.com/help/faq/phone-numbers/how-do-i-format-phone-numbers-to-work-internationally) phone number.

The code first polls your calendar for today's events. It looks first for any events matching the current time, then for any all-day events matching the current day, using the first it finds. It then extracts the name of the event and the phone number from the location field. It then forwards calls and text messages to the number from the location field, after replying with `sms_reply` or `voice_reply` as appropriate.

If there are no calendar events for the day, the messages are forwarded to `default_phone`.

## installation

1. create and activate a fresh virtualenv
1. checkout the code: `git clone https://github.com/wryfi/twilio-caldav.git`
1. `cd twilio-caldav`
1. install requirements: `pip install -r requirements.txt`
1. create `settings.py` file in root of checkout (see below)
1. run natively with cherrypy: `python twilio-caldav.py`, or
1. run with wsgi using `twilio-caldav.wsgi` and your favorite webserver

## configuration

Create a file called `settings.py` in the root of your clone. It must contain the following variables:

    # the path to the python virtualenv for this app
    virtualenv_path = '/path/to/virtualenv'
    # the url to your calendar. For zimbra, it looks something like:
    caldav_url = 'https://<username>:<password>@<zimbrahost>/dav/<zimbraemail>/<calendarname>'
    # the phone number to return when there are no events on the calendar for today
    default_phone = '+18005551234'
    # the name to return when there are no events on the calendar
    default_name = 'Popeye'
    # the twilio phone number to forward sms messages from
    twilio_phone_number = '+14155551234'
    # your twilio account sid from twilio.com
    twilio_account_ssid = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'
    # your twilio auth token from twilio.com
    twilio_auth_token = 'zzzzzzzzzzzzzzzzzzzzzzzzzz'
    # text to auto-respond to sender
    sms_reply = 'Thanks for your text. I will forward your message along.'
    # voice response to caller
    voice_reply = 'Thank you for calling. I will transfer you to the appropriate party'
