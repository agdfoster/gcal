# https://developers.google.com/google-apps/calendar/quickstart/python
''' 1. do wizard etc.,
2. from apiclient import discovery << replace apiclient with googleapiclient as apiclient is the old name and they haven't updated it.





issues
 - multiple calendars
 - time zone - can return data in any timezone, need way to discover local TZ for user
 - 24h events
 - holidays (24h events)

input / output
input = time period request
output = list of time periods when free within that.

 goals
 1. create dumb list of 'busy' times
        get list of event start times for period
        ignore 24h events
        get end time for those events

        yep. '''
