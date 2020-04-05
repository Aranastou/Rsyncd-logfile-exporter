from prometheus_client import start_http_server,Summary,Counter
import time
import os,sys
#from subprocess import call


###Metrics to scrap from log file###
connections = Counter("Connections","Total number of connections made to rsync daemon")
executions = Counter("Executions","Total number of rsync executions made")
data_recv = Counter("Data_Received","Bytes of data received from rsync")
data_send = Counter("Data_Send","Bytes of data send from rsync")


def prometheus_server(port):
	    start_http_server(port)

def tail_file():
	try:
		#fd = call("tail -f "+ sys.argv[1],shell=True) First thought was to call tail -f command
		with open(sys.argv[1]) as logFile:
			logFile.seek(0,os.SEEK_END)
			while True:
				new_log = logFile.readline()
				if new_log:
					print(new_log)
					log_data = new_log.split(" ")
					find_metrics(new_log)
					if "sent" in new_log:
						data_send.inc(float(log_data[4]))
						data_recv.inc(float(log_data[8]))

				else:
					time.sleep(0.1)

	except IndexError:
		print("[+]Please give file to read as first argument")
		print("[+]Example: python3 app.py 'logfile'")
		sys.exit(1)
	except KeyboardInterrupt:
		print("\n[+]Exiting...")
		time.sleep(1)
		sys.exit(1)

def find_metrics(metric):
	if "connect" in metric:
		connections.inc()
	elif "rsync" in metric:
		executions.inc()

if __name__ == '__main__':
	prometheus_server(8080)
	print("[+]Starting server...\n[+]Serving on port 8080\n[+]Visit http://localhost:8080 to see metrics")
	print("[+]Log file analysis started")	
	tail_file()
