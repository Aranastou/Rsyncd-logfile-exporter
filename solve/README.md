# Rsyncd logfile exporter

The purpose of this program is to read and tail `rsyncd` log file and export various statistics about the work
`rsyncd` is doing in a way that can be scraped by Prometheus.

## Metrics:
* Connections made to rsync daemon
* Executions of rsync
* Total Data received in bytes
* Total Data sent in bytes

## Usage
```sh
python3 app.py logfile.log 
```
