#!/usr/bin/env python3 

import pandas as pd 
import numpy as np 

class Instructor:

    def process_schedule_from_csv(source=r"~/Desktop/projects/tutoring/Foo Schedule Online - 7.20.csv"):
        df = pd.read_csv(source)
        df = df.fillna(0)
        df = df.rename(columns={'Unnamed: 0':"Instructors"})
        return df
    
    #class attributes
    todays_schedule = process_schedule_from_csv()
    
    def __init__(self, name, local_df=None, schedule_vector=None, area=None):
        """A data type for instructors

        Args:
            name (string): The name that is seen on the online schedule
            local_df (default None): Sub-dataframe of online schedule with client information for only 1 instructor  
            schedule_vector (default None): Binary numpy array encoding timeslots where instructor is scheduled
            area (default None): Tuple of ordered integers representing the numbered rowIDs for 1 instructor
        """
        self.name = name 
        self.local_df = local_df
        self.schedule_vector = schedule_vector
        self.area = area

        self._finish_initializing()
        return 

    def _finish_initializing(self):
        if self.check_if_scheduled():
            self.area = self._get_area(self.todays_schedule)
            self.local_df = self._get_local_df(self.todays_schedule)
            self.schedule_vector = self._populate_schedule_vector()
        else:
            #TODO:  add exceptions for names not scheduled 
            print("Name not found in schedule")
            raise KeyboardInterrupt
        return 
        
    def check_if_scheduled(self):
        """Determine if an instance of instructor is scheduled for today

        Returns:
            bool: True if instructor name appears in list of scheduled instructors. False otherwise.
        """
        result = False
        scheduled_for_today = self._get_scheduled_instructors(self.todays_schedule)
        if self.name in scheduled_for_today:
            result = True
        return result 

    def _get_scheduled_instructors(self, df):
        """Names of instructors who are scheduled for the day

        Args:
            df (pandas.DataFrame): Processed version of the daily online schedule

        Returns:
            list: List of strings. The names of the instructors scheduled on the daily online schedule
        """
        return list(df[df["Instructors"]!=0]["Instructors"])
    
    def _get_area(self, df):
        loc = int(df[df["Instructors"]==self.name].index.values)
        return (loc-1, loc, loc+1)


    def _get_local_df(self, df):
        """Tabular representation of a single instructor's daily client schedule

        Returns:
            pandas.DataFrame: A prospective table of a single instructor's daily schedule
        """
        return df[list(df.columns)][self.area[0]:self.area[2]+1]
    
    def _populate_schedule_vector(self):
        timeslots = self.local_df.columns[1:]
        #the number of 15 minute intervals on the schedule 
        ntimeslots = len(timeslots)
        self.schedule_vector = np.zeros((ntimeslots))

        for i, timeslot in enumerate(timeslots):
            for record in self.area:
                if self.local_df[timeslot][record]!=0:
                    self.schedule_vector[i]=1
        return self.schedule_vector

    def _forward_mapping(self):
        forward_mapping = {}
        for i in range(0, len(self.schedule_vector)):
            forward_mapping[i] = self.local_df.columns[1:][i]
        return forward_mapping
    
    def generate_target_splits(self):
        
        index_vector = []
        for i, v in enumerate(self.schedule_vector):
            if v==1:
                index_vector.append(i)              

        fast, slow = 0, 0
        split_ons = []
        for i in range(1, len(index_vector)):
            if index_vector[i]-index_vector[i-1]==1:
                fast += 1
            else:
                split_ons.append((slow, fast))
                fast = i
                slow = i 
        split_ons.append((slow, fast))

        target_indices = []
        for pair in split_ons:
            target_indices.append((index_vector[pair[0]], index_vector[pair[1]]))
        return target_indices

    

    def get_human_time(self):
        mapping = self._forward_mapping()
        splits = self.generate_target_splits()

        message = "{} is scheduled for...".format(self.name)
        for pair in splits:
            earliest = mapping[pair[0]]
            latest = mapping[pair[-1]]

            start_time = earliest.split('-')[0]
            end_time = latest.split('-')[-1]
            message += "\n{} to {}".format(start_time, end_time)
        
        return message