import speedtest
from datetime import datetime
import time
from handle_sheet import append_row, get_service, create_sheet, json_to_csv
import socket
import sys
import serial
import re

#This function runs a speedtest and returns the results
def run_speedtest(): 
    s = speedtest.Speedtest(secure=True)
    s.get_servers()
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

#Retrieves LTE and NR5G-NSA cell information from a modem using AT commands.
def get_cell_info(port="/dev/ttyUSB2", baudrate=115200, timeout=1): 
    try:
        # Open serial connection
        ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)

        # Send AT command
        ser.write(b'AT+QENG="servingcell"\r')

        # Wait for response
        time.sleep(1)

        # Read response
        response = ser.read_all().decode(errors='ignore')
        print(response)
        # Close the serial connection
        ser.close()

        # Extract LTE and NR5G-NSA information using regex
        lte_match = re.search(r'\+QENG:\s*"LTE".*', response)
        nr5g_match = re.search(r'\+QENG:\s*"NR5G-NSA".*', response)
        nr5g_sa_match = re.search(r'\+QENG:\s*"servingcell",.*"NR5G-SA".*', response)


        # Format the output string
        lte_info = lte_match.group(0) if lte_match else ",,,,,,,,,,,,,,,,,"
        nr5g_info = nr5g_match.group(0) if nr5g_match else ",,,,,,,,,,"
        nr5g_sa_info = nr5g_sa_match.group(0) if nr5g_sa_match else ",,,,,,,,,,"

        return f"{lte_info},{nr5g_info},{nr5g_sa_info}"
    
    except Exception as e:
        return f"Error: {str(e)}"

# Main program
try:
    # Wait for internet connection before starting
    wait_for_internet()

    spreadsheet_id = "1mFNR6EdvY22x0fUlCELVniT_OYJgioKsR0TJSCOYino"

    sheet_name = datetime.now().strftime("%Y.%m.%d %H:%M") 
    create_sheet(sheet_name, get_service(spreadsheet_id), spreadsheet_id)
    print(f"Creating new sheet: {sheet_name}", file=sys.stdout, flush=True)
    header = "timestamp,download,upload,ping,server_lat,server_lon,server_name,server_country,server_sponsor,server_id,server_latency,share_url,client_lat,client_lon,servingcell,is_tdd,LTE_MCC,LTE_MNC,LTE_cellID,LTE_PCID,LTE_ARFCN,freq_band_ind,UL_bandwidth,DL_bandwidth,LTE_TAC,LTE_RSRP,LTE_RSRQ,LTE_RSSI,LTE_SINR,LTE_CQI,LTE_tx_power,srxlev,5G cell,5G_MCC,5G_MNC,5G_PCID,5G_RSRP,5G_SINR,5G_RSRQ,5G_ARFCN,5G_band,,,5GSA_cellinfo"
    append_row(header, get_service(spreadsheet_id), spreadsheet_id, sheet_name)

    #write to local file with sheet_name in /measurements folder
    with open(f"measurements/{sheet_name}.csv", "w") as f:
        f.write(header) 


    # run the speedtest loops
    while True:
        try:
            wait_for_internet()

            results = json_to_csv(run_speedtest())
            #Try to add get_cell_info() to results
            try:
                cell_info = get_cell_info()
                if cell_info:  
                    results += "," + cell_info
            except Exception as e:
                print(f"Error in get_cell_info: {str(e)}", file=sys.stderr, flush=True)
                
            if results:
                print(results, file=sys.stdout, flush=True)
                with open(f"measurements/{sheet_name}.csv", "a") as f:
                    f.write(results)
                append_row(results, get_service(spreadsheet_id), spreadsheet_id, sheet_name)
            else:
                print("Skipping this iteration due to failed speedtest", file=sys.stderr, flush=True)
                
        except Exception as e:
            print(f"Error in main loop: {str(e)}", file=sys.stderr, flush=True)
            
            
        print("Waiting seconds before next test...", file=sys.stdout, flush=True)
        time.sleep(5)

except Exception as e:
    print(f"Fatal error: {str(e)}", file=sys.stderr, flush=True)

 



