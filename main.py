#!/usr/bin/env python3 

from instructor import Instructor
from schedule import Schedule

def main():

    today = Schedule(source=r"/Users/nikourriola/Desktop/projects/tutoring/Mathnasium Schedule Online! - 7.21.csv")

    people = today.get_scheduled_instructors()
    for person in people:
        print(Instructor(person, todays_schedule=today).get_human_time())

    return 

if __name__=="__main__":
    main()

