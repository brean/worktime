import datetime
import operator
from functools import reduce

# these need installation
from caldav import DAVClient
from caldav import dav
from tabulate import tabulate


def login(server: str, secret_file: str):
    """Login to the server."""

    username = password = None
    # Login to the server
    with open(secret_file) as sf:
        username, password = sf.read().split(':')

    # Create an caldav client object
    client = DAVClient(server, username=username, password=password)
    return client


def get_work_entries(
    client, start: datetime, end: datetime, calendar_name: str = 'worktime'):
    """Get list of all work entries in between given date."""
    principal = client.principal()
    calendar = principal.calendar(calendar_name)

    # Get the calendar times
    work_entries = []
    calendar_events = calendar.search(
        start=start, end=end, event=True, expand=True
    )
    for calendar_event in calendar_events:
        vevent = calendar_event.vobject_instance.vevent
        project = '(unknown)'
        summary = vevent.summary.value.strip()
        if summary.startswith('['):
            project = summary.split(']')[0][1:]
            summary = summary[len(project)+2:].strip()
        
        start_date = vevent.dtstart.value
        end_date = vevent.dtend.value

        work_entries.append([project, summary, end_date, start_date])

    return work_entries


def monday():
    today = datetime.date.today()
    return today - datetime.timedelta(days=today.weekday())


def tomorrow():
    return datetime.date.today() + datetime.timedelta(days=1)


def hours_num(delta: datetime.timedelta):
    # get hours as number (float)
    return (delta.days * 24) + (delta.seconds / 3600)


def work_this_week(client, calendar_name: str = 'worktime'):
    """Get all work entries from this week"""
    end_date = tomorrow()
    start_date = monday()
    return get_work_entries(client, start_date, end_date)


def work_last_week(client, calendar_name: str = 'worktime'):
    """Get all work entries from previous week"""
    end_date = monday()
    start_date = end_date - datetime.timedelta(days=7)
    return get_work_entries(client, start_date, end_date)


def print_work_time(client, calendar_name: str='worktime', hours: int = 40):
    # show last weeks table
    prev_week = work_last_week(client)
    print(tabulate(
        [(p[0], p[1], p[2] - p[3]) for p in prev_week],
        headers=['Project', 'Name', 'Duration']))

    # calculate if we have over or undertime from last week.
    prev_week_times = [e[2] - e[3] for e in prev_week]
    prev_week_hours = hours_num(reduce(operator.add, prev_week_times))
    prev_diff = hours - prev_week_hours
    if prev_diff > 0:
        print(f'💪 You still owe {prev_diff} hours from last week')
    elif prev_diff < 0:
        print(f'🎉 Last week you worked {-prev_diff} hours '
            'more than you should.')

    # show this weeks table
    this_week = work_this_week(client, calendar_name)
    print(tabulate(
        [(p[0], p[1], p[2] - p[3]) for p in this_week],
        headers=['Project', 'Name', 'Duration']))

    # Show how many hours you need to work for the current week
    this_week_times = [e[2] - e[3] for e in this_week]
    this_time = hours_num(reduce(operator.add, this_week_times)) - prev_diff
    this_diff = hours - this_time
    if this_diff > 0:
        print(f'💪 You still have {this_diff} hours to go this week')
    elif this_diff < 0:
        print(
            f'🎉 You are already {-this_diff} hours over for the week!'
            'Get some rest.')
    else:
        print(
            '🎉You worked exactly as much as your contract says you should.')


    # TODO: create table by day + pauses:
    # date (day), start, end    break  (ist) (soll) (type)
    # 2022-01-01   9:00  18:00   1:00
    # types: 
    #   work in the office
    #   mobile work
    #   business trip
    #   vacation
    #   sickness
    #   training
    #   overtime compensation
    #   core time withdrawal
    #   telework
    #   (other)

    # TODO: fill excel-sheet
