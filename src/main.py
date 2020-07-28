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

    #title of the online schedule (a Google Sheet)
    sheet_title = get_tomorrows_date()

    #the online schedule for the next day
    schedule = Schedule(sheet_title)

    #the content being sent to instructors
    group_text = TextMessage()

    people = schedule.get_scheduled_instructors()
    for person in people:
        to_add = Instructor(person, todays_schedule=schedule).get_human_time()
        group_text.append_to_msg_content(to_add)

    group_text.send_text()
    return 

if __name__=="__main__":
    main()

