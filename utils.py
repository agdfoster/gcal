
import datetime

from googleapiclient import discovery
import httplib2

from _credentials import get_credentials

NOW = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

def get_events(start=NOW, end=None, max_results=2500):
    '''  returns list of events for given start & end time  '''
    # TODO - END TIME
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    events_result = service.events().list(
        # REF: https://developers.google.com/google-apps/calendar/v3/reference/events/list
        calendarId='primary',
        timeMin=start,
        timeMax=end,
        maxResults=max_results,
        singleEvents=True, # True returns recurring events as series of events, not recurring event object. Required for order by start date
        orderBy='startTime',
        timeZone='UTC'
        ).execute()

    events = events_result.get('items', [])
    print('Getting the upcoming %d events' %len(events))
    return events #[{event_obj},{event_obj},{event_obj}]
#

def get_things_from_event(event):
    """ given a gcal event, will return various nice things
    DONT ACTUALLY USE THIS, FOR REFERENCE ONLY"""
    # get event date-time, if None get event date (24h events)
    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['end'].get('date'))
    # metadata
    summary = event['summary']
    desc = event['description']
    location = event['location']
    email_creator = event['creator']['email']

    print(start, end)
    print(summary, desc)
    print(location)
    print(email_creator)



if __name__ == '__main__':
    A = get_events(max_results=10)
    get_things_from_event(A[0])
    