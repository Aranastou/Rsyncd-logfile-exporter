# Rsyncd logfile exporter


## Overview

The goal of this program is to read and tail an `rsyncd` log file and export various statistics about the work
`rsyncd` is doing in a way that can be scraped by Prometheus. By "tail" we mean
opening the file and continually reading (and analyzing) it, like `tail -f`
does.

## Input and expected output

`rsyncd` has a standardized log file format:

```
2017/09/04 09:55:40 [1012] connect from localhost (::1)
2017/09/04 09:55:40 [1012] rsync on exercise/ from localhost (::1)
2017/09/04 09:55:40 [1012] building file list
2017/09/04 09:55:40 [1012] sent 512 bytes  received 1052 bytes  total size 0
```

The only non-obvious field is the third one, which is the PID of the `rsyncd`
worker that handles the connection. Note that there are other log lines in the
file, but the ones above are those of a typical connection.

## Prometheus

Prometheus is a monitoring tool that consists of a time series database and a
scraping daemon.To export the metrics we need Prometheus language bindings.

- https://github.com/prometheus/client_python

A quick guide on how to instrument an application can be found here:

- https://prometheus.io/docs/instrumenting/clientlibs/
- https://prometheus.io/docs/instrumenting/writing_exporters/

Testing the code can be done by just looking at the web page the client
libraries export with a web browser (it's plain text, so even `wget` would
work).

## Example log file

There is an example log file included in this repo (`rsync_example.log`). It
contains a sampling of what log lines the exporter will need to handle, like a
mix of v4 and v6 addresses.

## Running rsyncd

In order to test the program against a living log file, you can
run rsyncd and generate some logging from it. Typically, rsyncd is configured
using `rsyncd.conf`. For this purpose, this would be enough:

```
log file=rsync.log
port=8737
[exercise]
   path = exercise_root
   use chroot = false

```

This config is also in `rsyncd_example.conf`, so you can run the server like this:

`$ rsync --daemon --no-detach -v --config rsyncd_example.conf`

Log lines should appear in `rsync.log`. To use the server with a client (and
generate more log lines to experiment with):

`$ rsync -rav rsync://localhost:8737/exercise/ tmp/`


The metrics i decided to export is:
* Connections made to rsync daemon
* Executions of rsync
* Total Data received in bytes
* Total Data sent in bytes

## Usage

```sh
python3 app.py logfile.log 
```
