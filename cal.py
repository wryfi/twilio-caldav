import caldav
from datetime import date, datetime
import pytz
from settings import caldav_url as url, default_phone, default_name

def get_caldav_contact():
  '''
  Polls caldav_url for today() and returns (summary, location) as (name, phonenumber) for first matching event.
  Looks first for part-day events; the first that matches now() will be parsed for (name, phonenumber).
  If there are no matching part-day events, look for all-day events; the first that matches today() will be parsed.
  If no events are on the calendar for today(), return (default_name, default_phone).
  '''

  contact = None
  client = caldav.DAVClient(url)
  principal = caldav.Principal(client, url)
  calendars = principal.calendars()
  calendar = calendars[0]
  today = date.today()
  now = pytz.UTC.localize(datetime.utcnow())
  events = { 'allday' : [], 'partday': [] }

  for event in calendar.date_search(today):
    event.load()
    if type(event.instance.vevent.dtstart.value) == datetime:
      start = event.instance.vevent.dtstart.value.astimezone(pytz.UTC)
      end = event.instance.vevent.dtend.value.astimezone(pytz.UTC)
    else:
      start = event.instance.vevent.dtstart.value
      end = event.instance.vevent.dtend.value
    eventdict = { 'start' : start, 'end': end, 'phone' : event.instance.vevent.location.value, 'name' : event.instance.vevent.summary.value }
    if type(eventdict['start']) == datetime:
      events['partday'].append(eventdict)          
    elif type(eventdict['start']) == date:
      events['allday'].append(eventdict)

  if len(events['partday']) > 0:
    for event in events['partday']:
      if event['start'] <= now and now < event['end']:
        contact = (event['name'], event['phone'])

  if contact == None and len(events['allday']) > 0:
    contact = (events['allday'][0]['name'], events['allday'][0]['phone'])

  if contact == None:
    contact = (default_name, default_phone)
   
  return contact
