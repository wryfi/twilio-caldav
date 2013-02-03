import caldav
from datetime import date, datetime, timedelta
import pytz
from settings import caldav_url as url, default_phone, default_name, timezone

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
  tomorrow = today + timedelta(hours=24)
  now = pytz.timezone(timezone).localize(datetime.now())
  events = { 'allday' : [], 'partday': [] }

  for event in calendar.date_search(today, tomorrow):
    event.load()
    eventdict = { 'start' : event.instance.vevent.dtstart.value, 'end': event.instance.vevent.dtend.value, \
		  'phone' : event.instance.vevent.location.value, 'name' : event.instance.vevent.summary.value }
    if type(eventdict['start']) == datetime:
      events['partday'].append(eventdict)          
    elif type(eventdict['start']) == date:
      events['allday'].append(eventdict)

  if len(events['partday']) > 0:
    for event in events['partday']:
      if event['start'] <= now and now < event['end']:
        return (event['name'], event['phone'])

  if len(events['allday']) > 0:
    return (events['allday'][0]['name'], events['allday'][0]['phone'])

  return (default_name, default_phone)
