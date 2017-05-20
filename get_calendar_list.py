# get user's calendar list and filter it to one's we want to pay attention to.
# keep in mind user may want to change this if 
# e.g., they have their wife's calendar FULL shared
# Annoyingly, people often share their work calendar to their personal calendar as read-only
# Also, need a setting later for if they are like AF and use their personal calendar as their main calendar.

import datetime
from pprint import pprint
import re

import pandas as pd
pd.set_option('display.width', 1000) # increase Pandas output width

from _credentials import service


#const
NOW = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
if __name__ == '__main__':
    TEST = True
else: TEST = False

def example_cal():
    """get example calendar"""
    calendars = service.calendarList().list(maxResults=100).execute()
    if TEST:
        pprint(calendars['items'][2])
example_cal()

def print_all_cals():
    """prints all calendars"""
    # ref: master: https://goo.gl/z0Lnev and specfic docs: https://goo.gl/4lbxid
    calendars = service.calendarList().list(maxResults=100).execute()
    li = [(item['summary'], item['id'], item['accessRole']) for item in calendars.get('items')]
    df = pd.DataFrame(li, columns=['name', 'id', 'access']).sort_values(by='access')
    if TEST:
        print('- - - - - FULL CALS LIST - - - - -')
        print(df)
print_all_cals()

def filtered_cals_by_access_role():
    """ returns filtered calendar list based on access role
    this doesn't catch calendars you use but have not set as owner :( """
    # ref: master: https://goo.gl/z0Lnev and specfic docs: https://goo.gl/4lbxid
    # get calendars object
    calendars = service.calendarList().list(maxResults=100).execute()
    li = [
        (item['summary'], item['id'], item['accessRole'])
        for item in calendars.get('items')
        if item['accessRole'] in ['owner', 'writer']
        ]
    df = pd.DataFrame(li, columns=['name', 'id', 'access']).sort_values(by='access')
    if TEST:
        print('- - - - - FILTERED CALS LIST - - - - -')
        print(df)
filtered_cals_by_access_role()

def filtered_cals_by_name_rules(user_name):
    """ returns filtered calendar list based on calendar name
    ASSUMPTIONS:    1. summary could be name OR email, use id
                    2. Won't need to use summary e.g., if someone uses a group or something as a main calendar
                    3. your fName or sName or f.?s@ will be in id"""
    # get calendars object
    calendars = service.calendarList().list(maxResults=100).execute()
    # get fName & sName
    f_name = re.findall(r'^\S+', user_name.strip())[0].lower()
    s_name = re.findall(r'\S+$', user_name.strip())[0].lower()
    print(f_name)
    # filter calendars list, keep ones containing first name or second name
    passed_filter = [
        item for item in calendars.get('items')
        if f_name in item['id'] or s_name in item['id']]
    failed_filter = [
        item for item in calendars.get('items')
        if item not in passed_filter]
    # print it
    if TEST:
        printable_list = [(item['summary'], item['id']) for item in passed_filter]
        printable_list2 = [(item['summary'], item['id']) for item in failed_filter]
        print('- - - - - OUTPUT PASSED LIST - - - - - ')
        print(pd.DataFrame(printable_list))
        print('- - - - - OUTPUT FAILED LIST - - - - - ')
        print(pd.DataFrame(printable_list2))
    return passed_filter
#todo ^^^ the above can probably just return a list of calendar ID's to check against but I'm not sure if they're in the calendar objects
filtered_cals_by_name_rules('Alex Foster') #name needs passing in somewhere
