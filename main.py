#!/usr/bin/env python3 

import datetime
from google_sheet import GoogleSheet
from instructor import Instructor
from schedule import Schedule
from text_message import TextMessage

def get_tomorrows_date():
    date = datetime.date.today() + datetime.timedelta(days=1)
    _, mo, dd = str(date).split('-')
    mo = mo.strip('0')
    return mo + '.' + dd

def main():

    #Title of the online schedule (a Google Sheet)
    workday = get_tomorrows_date()

    #the online schedule for the next day
    schedule = Schedule(workday)

    #the content being sent to instructors
    group_text = TextMessage()

    people = schedule.get_scheduled_instructors()
    for person in people:
        to_add = Instructor(person, todays_schedule=schedule).get_human_time()
        group_text.append_to_msg_content(to_add)

    #replace with group_text.send_text() after testing
    print(group_text.msg_content)
    #group_text.send_text()
    return 

if __name__=="__main__":
    main()

