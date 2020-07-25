#!/usr/bin/env python3 

import numpy as np 
from schedule import Schedule
from exceptions import *

class Instructor:
        
    def __init__(self, name, todays_schedule=None, local_df=None, schedule_vector=None, area=None):
        """A data type for instructors

        Args:
            name (string): The name that is seen on the online schedule
            todays_schedule (default None): A preprocessed version of the online schedule
            local_df (default None): Sub-dataframe of online schedule with client information for only 1 instructor  
            schedule_vector (default None): Binary numpy array encoding timeslots where instructor is scheduled
            area (default None): Tuple of ordered integers representing the numbered rowIDs for 1 instructor
        """
        self.name = name 
        self.local_df = local_df
        self.schedule_vector = schedule_vector
        self.area = area
        self.todays_schedule = todays_schedule

        self._finish_initializing()
        return 

    #TODO:  make `todays_schedule` assignment robust to incorrect datatypes
    def _finish_initializing(self):
        """Data verification and calling setters for instance attributes

        Raises:
            ScheduleError: If `todays_schedule` is not given
            NameNotFoundError: If `name` is not an element of the list of scheduled instructors
        """
        #check for an instance of `Schedule()`
        if self.todays_schedule==None:
            raise ScheduleError("Cannot find DataFrame for `todays_schedule`")
        
        #check that the name appears as an instructor
        if not self.check_if_scheduled():
            raise NameNotFoundError("{} could not be found in the schedule. Please check spelling.".format(self.name)) 
        else:
            #setting remaining instance attributes
            self.area = self._get_area(self.todays_schedule.content)
            self.local_df = self._get_local_df(self.todays_schedule.content)
            self.schedule_vector = self._populate_schedule_vector()
        
        return 
        
    def check_if_scheduled(self):
        """Determine if an instance of instructor is scheduled for today

        Returns:
            bool: True if instructor name appears in list of scheduled instructors. False otherwise.
        """
        result = False
        working_instructors = self.todays_schedule.get_scheduled_instructors()
        if self.name in working_instructors:
            result = True
        return result 
    
    def _get_area(self, df):
        """Determine the numbered rowIDs that encompass the instructor's client list

        Args:
            df (pandas.DataFrame): The online schedule represented by a DataFrame

        Returns:
            tuple: Assigned rowIDs ordered from smallest to largest 
        """
        loc = int(df[df["Instructors"]==self.name].index.values)
        return (loc-1, loc, loc+1)


    def _get_local_df(self, df):
        """Tabular representation of a single instructor's daily client schedule

        Returns:
            pandas.DataFrame: A prospective table of a single instructor's daily schedule
        """
        return df[list(df.columns)][self.area[0]:self.area[2]+1]
    
    def _populate_schedule_vector(self):
        """Encode the timeslots an instructor is scheduled as a binary vector

        Returns:
            list: Value of 1 at the i-th index indicates that the instructor is scheduled for the i-th timeslot
        """
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
        """Mapping between indices of a vector and timeslots on a schedule

        Returns:
            dict: Keys are ints spanning the length of a vector. Values are 15 minute timeslots as strings.
        """
        forward_mapping = {}
        for i in range(0, len(self.schedule_vector)):
            forward_mapping[i] = self.local_df.columns[1:][i]
        return forward_mapping
    
    def generate_target_splits(self):
        """Find start-end indices for all non-zero subarrays within a vector

        Returns:
            list: Elements are tuples of ints representing the start-end indices of a non-zero subarray
        """
        
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
        """Create the content for a text message notifying one instructor of their hours

        Returns:
            string: The instructor's name and the time range they are working
        """
        mapping = self._forward_mapping()
        splits = self.generate_target_splits()

        message = "{} is scheduled for... ".format(self.name)
        """
        for pair in splits:
            earliest = mapping[pair[0]]
            latest = mapping[pair[-1]]

            start_time = earliest.split('-')[0]
            end_time = latest.split('-')[-1]
            message += "{} to {}\n".format(start_time, end_time)
        """
        if len(splits)>1:
            first_pair = splits[0]
            last_pair = splits[-1]

            earliest = mapping[first_pair[0]]
            latest = mapping[first_pair[-1]]
            start_time = earliest.split('-')[0]
            end_time = latest.split('-')[-1]
            message += "{} to {}".format(start_time, end_time)

            for pair in splits[1:-1]:
                earliest = mapping[pair[0]]
                latest = mapping[pair[-1]]

                start_time = earliest.split('-')[0]
                end_time = latest.split('-')[-1]
                message += ", {} to {}".format(start_time, end_time)
            
            earliest = mapping[last_pair[0]]
            latest = mapping[last_pair[-1]]
            start_time = earliest.split('-')[0]
            end_time = latest.split('-')[-1]
            message += ", and {} to {}".format(start_time, end_time)
            
        else:
            pair = splits[0]
            earliest = mapping[pair[0]]
            latest = mapping[pair[-1]]

            start_time = earliest.split('-')[0]
            end_time = latest.split('-')[-1]
            message += "{} to {}\n".format(start_time, end_time)
        return message