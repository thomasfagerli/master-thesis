from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def get_service(spreadsheet_id):
    credentials = service_account.Credentials.from_service_account_file("key.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
    service = build("sheets", "v4", credentials=credentials)
    return service


#append a row to the sheet from a csv string
def append_row(csv_string, service, spreadsheet_id, sheet_name): 

    # Split the CSV string and strip whitespace from each value
    values = [value.strip() for value in csv_string.split(',')]
    
    body = {
        'values': [values]  # Wrap values in a list to create a row
    }


    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=sheet_name,  
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()
    
    return result

#create a new sheet in existing spreadsheet
def create_sheet(title, service, spreadsheet_id):
    try:
        request_body = {
            "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": title,
                        }
                    }
                }
            ]
        }

        response = (
            service.spreadsheets()
            .batchUpdate(spreadsheetId=spreadsheet_id, body=request_body)
            .execute()
        )

        sheet_id = response["replies"][0]["addSheet"]["properties"]["sheetId"]
        print(f"Sheet '{title}' created with ID: {sheet_id}")
        return sheet_id

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None
    