import speedtest
from datetime import datetime
import time

#This function runs a speedtest and returns the results
def run_speedtest(): 
    s = speedtest.Speedtest()
    s.get_servers()
    s.get_best_server()
    s.download()
    s.upload()
    s.results.share()
    return s.results.csv()  #returns a csv string of the results    


#run the speedtest every 5 minutes
while True:
    results = run_speedtest()
    print(results)

    #store result of speedtest in a file with timestamp
    with open("speedtest_results.txt", "a") as f:
        f.write(f"{datetime.now()},{results}\n")
    
    time.sleep(60)


