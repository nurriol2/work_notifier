#!/usr/bin/env python3 

from google_sheet import GoogleSheet
from instructor import Instructor
from schedule import Schedule
from text_message import TextMessage

def main():

    #the online schedule for today's date
    today = Schedule("7.25")

    #the content being sent to instructors
    group_text = TextMessage()

    people = today.get_scheduled_instructors()
    for person in people:
        to_add = Instructor(person, todays_schedule=today).get_human_time()
        group_text.append_to_msg_content(to_add)

    #replace with group_text.send_text() after testing
    print(group_text.msg_content)
    #group_text.send_text()
    return 

if __name__=="__main__":
    main()

