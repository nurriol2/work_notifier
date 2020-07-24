#!/usr/bin/env python3

import pandas as pd

class Schedule:

    def __init__(self, source=r"~/Desktop/projects/tutoring/Foo Schedule Online - 7.20.csv"):
        self.source = source 
        self.content = self.process_schedule_from_csv()
        return 

    def process_schedule_from_csv(self):
        df = pd.read_csv(self.source)
        df = df.fillna(0)
        df = df.rename(columns={'Unnamed: 0':"Instructors"})
        return df

    def get_scheduled_instructors(self):
        df = self.content
        return list(df[df["Instructors"]!=0]["Instructors"])