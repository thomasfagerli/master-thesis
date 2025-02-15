import speedtest
from datetime import datetime
import time
from handle_sheet import append_row, get_service, create_sheet, json_to_csv


#This function runs a speedtest and returns the results
def run_speedtest(): 
    s = speedtest.Speedtest(secure=True)
    s.get_servers()
    s.get_best_server()
    s.download()
    s.upload()
    s.results.share()
    return s.results.dict()     



spreadsheet_id = "1mFNR6EdvY22x0fUlCELVniT_OYJgioKsR0TJSCOYino"



sheet_name = datetime.now().strftime("%Y.%m.%d %H:%M") 
create_sheet(sheet_name, get_service(spreadsheet_id), spreadsheet_id)
print(f"Creating new sheet: {sheet_name}")
header = "timestamp,download,upload,ping,server_lat,server_lon,server_name,server_country,server_sponsor,server_id,server_latency,share_url,client_lat,client_lon"
append_row(header, get_service(spreadsheet_id), spreadsheet_id, sheet_name)

#run the speedtest every 60 seconds
while True:
    try:
        results = json_to_csv(run_speedtest())
        if results:
            print(results)
            append_row(results, get_service(spreadsheet_id), spreadsheet_id, sheet_name)
        else:
            print("Skipping this iteration due to failed speedtest")
            
    except Exception as e:
        print(f"Error in main loop: {str(e)}")
        
    print("Waiting 60 seconds before next test...")
    time.sleep(60)


