#!/usr/bin/env python3 

from Google import create_service
from credentials import credentials
import pandas as pd

#download secret file after authorizing O2Auth from console.cloud.google.com
#must be in the same directory as this file
CLIENT_SECRET_FILE = credentials["Google Secret File"] #can rename this file
API_SERVICE_NAME = "sheets"
API_VERSION = "v4"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
gsheetId = credentials["gsheetId"]

s = create_service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)
gs = s.spreadsheets()
rows = gs.values().get(spreadsheetId=gsheetId,range="7.20").execute()
data = rows.get("values")
df = pd.DataFrame(data)
print(df)
