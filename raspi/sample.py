import speedtest
from datetime import datetime
import time
from handle_sheet import append_row, get_service, create_sheet, json_to_csv
import socket
import sys


#This function runs a speedtest and returns the results
def run_speedtest(): 
    s = speedtest.Speedtest(secure=True)
    s.get_servers([64688])
    s.get_best_server()
    s.download()
    s.upload()
    s.results.share()
    return s.results.dict()     



def wait_for_internet():
    """Wait until internet connection is established"""
    print("Checking internet connection...", file=sys.stdout, flush=True)
    while True:
        try:
            # Try to connect to Google's DNS server
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            print("Internet connection established!", file=sys.stdout, flush=True)
            return
        except OSError:
            print("No internet connection. Waiting 5 seconds...", file=sys.stderr, flush=True)
            time.sleep(5)



# Main program
try:
    # Wait for internet connection before starting
    wait_for_internet()

    spreadsheet_id = "1mFNR6EdvY22x0fUlCELVniT_OYJgioKsR0TJSCOYino"

    sheet_name = datetime.now().strftime("%Y.%m.%d %H:%M") 
    create_sheet(sheet_name, get_service(spreadsheet_id), spreadsheet_id)
    print(f"Creating new sheet: {sheet_name}", file=sys.stdout, flush=True)
    header = "timestamp,download,upload,ping,server_lat,server_lon,server_name,server_country,server_sponsor,server_id,server_latency,share_url,client_lat,client_lon"
    append_row(header, get_service(spreadsheet_id), spreadsheet_id, sheet_name)

    # run the speedtest every 60 seconds
    while True:
        try:
            results = json_to_csv(run_speedtest())
            if results:
                print(results, file=sys.stdout, flush=True)
                append_row(results, get_service(spreadsheet_id), spreadsheet_id, sheet_name)
            else:
                print("Skipping this iteration due to failed speedtest", file=sys.stderr, flush=True)
                
        except Exception as e:
            print(f"Error in main loop: {str(e)}", file=sys.stderr, flush=True)
            
        print("Waiting 300 seconds before next test...", file=sys.stdout, flush=True)
        time.sleep(300)

except Exception as e:
    print(f"Fatal error: {str(e)}", file=sys.stderr, flush=True)

 



