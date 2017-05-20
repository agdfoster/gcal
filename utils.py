
import datetime
from pprint import pprint

# from googleapiclient import discovery
# import httplib2

from _credentials import service
from iso_to_python_converter import iso_to_python_converter as i_to_py

NOW = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

def get_events(start=NOW, end=None, max_results=2500):
    '''  returns list of events for given start & end time  '''
    events_result = service.events().list(
        # REF: https://developers.google.com/google-apps/calendar/v3/reference/events/list
        calendarId='primary', # use 'primary' to get their primary cal
        timeMin=start,
        timeMax=end,
        maxResults=max_results,
        singleEvents=True, # True returns recurring events as series of events, not recurring event object. Required for order by start date
        orderBy='startTime',
        timeZone='UTC'
        ).execute()

    events = events_result.get('items', [])
    print('Getting upcoming %d events' %len(events))
    return events #[{event_obj},{event_obj},{event_obj}]
#

def get_things_from_event(event):
    """ given a gcal event, will return various nice things
    DONT ACTUALLY USE THIS, FOR REFERENCE ONLY"""
    # get event date-time, if None get event date (24h events)
    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['end'].get('date'))
    duration = i_to_py(end) - i_to_py(start)
    # metadata
    summary = event.get('summary', '')
    desc = event.get('description', '')
    location = event.get('location', '')
    email_creator = event.get('creator', {}).get('email', '')

    print("start: %s end: %s " %(start, end))
    print('duration: %s' %duration)
    print("summary: %s " %summary) 
    print("descr: %s" %desc)
    print('location: %s' %location) 
    print(email_creator)



if __name__ == '__main__':
    events = get_events(max_results=250)
    
    output = [get_things_from_event(event) for event in events]
    