#!/usr/bin/env python3

from Google import create_service
from credentials import credentials
import pandas as pd 

class GoogleSheet:

    #class attributes
    
    #download secret file after authorizing O2Auth from console.cloud.google.com
    #must be in the same directory as this file
    CLIENT_SECRET_FILE = credentials["Google Secret File"] #can rename this file
    #enable Google Drive and Google Sheets APIs at console.cloud.google.com 
    API_SERVICE_NAME = "sheets"
    API_VERSION = "v4"
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

    def __init__(self, sheet_range):
        self.sheet_range = sheet_range
        self.gsheetId = credentials["gsheetId"]
        return 
    
    def sheet_to_dataframe(self, verbose=False):
        
        s = create_service(self.CLIENT_SECRET_FILE, self.API_SERVICE_NAME, self.API_VERSION, self.SCOPES)
        gs = s.spreadsheets()
        rows = gs.values().get(spreadsheetId=self.gsheetId, range=self.sheet_range).execute()
        data = rows.get("values")
        df = pd.DataFrame(data)

        if verbose:
            print(df)

        return df 