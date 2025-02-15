from google.oauth2 import service_account
from googleapiclient.discovery import build

spreadsheet_id = "1mFNR6EdvY22x0fUlCELVniT_OYJgioKsR0TJSCOYino"
# For example:
# spreadsheet_id = "8VaaiCuZ2q09IVndzU54s1RtxQreAxgFNaUPf9su5hK0"

credentials = service_account.Credentials.from_service_account_file("key.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
service = build("sheets", "v4", credentials=credentials)

request = service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=[], includeGridData=False)
sheet_props = request.execute()

print(sheet_props["properties"]["title"])