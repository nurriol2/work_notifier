#!/usr/bin/env python3

from google_sheet import GoogleSheet
import pandas as pd

class Schedule:

    def __init__(self, date):
        self.date = date
        self.content = self.process_schedule()
        return 

    def process_schedule(self):
        """Prepare a DataFrame to represent the online schedule

        Returns:
            pandas.DataFrame: Fully processed DataFrame representing the online schedule
        """
        df = GoogleSheet(self.date).sheet_to_dataframe()
        df = df.fillna(0)
        #set the columns as timeslots 
        df.columns = df.iloc[0]
        #one of the empty string cells needs to be renamed
        df = df.rename(columns={'':"Instructors"})
        #the remaining empty string cells being replaced
        df[df==''] = 0      
        return df

    def get_scheduled_instructors(self):
        """The instructors scheduled to work on today's online schedule

        Returns:
            list: Names of the instructors in the instructor column of the online schedule. 
                  Not robust to repeated names.
        """
        df = self.content
        return list(df[df["Instructors"]!=0]["Instructors"])