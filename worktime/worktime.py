from caldav import DAVClient
from caldav import dav
from tabulate import tabulate
from datetime import datetime, timedelta


def login(server: str, secret_file: str):

    username = password = None
    # Login to the server
    with open(secret_file) as sf:
        username, password = sf.read().split(':')

    # Create an caldav client object
    client = DAVClient(server, username=username, password=password)
    return client


def print_work_times(client, calendar_name: str='worktime'):
    principal = client.principal()
    calendar = principal.calendar(calendar_name)
       

    # Get the calendar times
    time_list = []
    calendar_events = calendar.events()
    for calendar_event in calendar_events:
        vevent = calendar_event.vobject_instance.vevent
        project = '(unknown)'
        summary = vevent.summary.value.strip()
        if summary.startswith('['):
            project = summary.split(']')[0][1:]
            summary = summary[len(project)+2:].strip()
        
        start_date = vevent.dtstart.value
        end_date = vevent.dtend.value

        time_list.append([project, summary, end_date - start_date])

    # sort list by project
    sorted_time_list = sorted(time_list, key=lambda row: row[0])


    # Print the list of times as a table
    print(tabulate(sorted_time_list, headers=['Project', 'Name', 'Duration']))

    # TODO: show only for current week and how many hours are still needed to do
    # TODO: calculate over and underhours
    # TODO: generate excel-sheet