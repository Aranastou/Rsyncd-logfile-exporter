# Programming exercise: Rsyncd logfile exporter

## Overview

This repository contains several files that are needed to complete the
programming exercise.

The goal of the exercise is to write a program in Python or Go that will read
and tail an `rsyncd` log file and export various statistics about the work
`rsyncd` is doing in a way that can be scraped by Prometheus. By "tail" we mean
opening the file and continually reading (and analyzing) it, like `tail -f`
does.

## Input and expected output

`rsyncd` has a standardized log file format:

```
2017/09/04 09:55:40 [1012] connect from localhost (::1)
2017/09/04 09:55:40 [1012] rsync on exercise/ from localhost (::1)
2017/09/04 09:55:40 [1012] building file list
2017/09/04 09:55:40 [1012] sent 87 bytes  received 32 bytes  total size 0
```

The only non-obvious field is the third one, which is the PID of the `rsyncd`
worker that handles the connection. Note that there are other log lines in the
file, but the ones above are those of a typical connection.

## Prometheus

Prometheus is a monitoring tool that consists of a time series database and a
scraping daemon. For the purposes of this exercise, you do not need to set up
Prometheus. You do need the Prometheus language bindings for the language of
your choice:

- https://github.com/prometheus/client_golang
- https://github.com/prometheus/client_python

A quick guide on how to instrument an application can be found here:

- https://prometheus.io/docs/instrumenting/clientlibs/
- https://prometheus.io/docs/instrumenting/writing_exporters/

Testing your code can be done by just looking at the web page the client
libraries export with a web browser (it's plain text, so even `wget` would
work).

Note that we do not tell you *what* metrics to export. Part of the exercise is
you picking the ones that make sense.

## Example log file

There is an example log file included in this repo (`rsync_example.log`). It
contains a sampling of what log lines the exporter will need to handle, like a
mix of v4 and v6 addresses.

## Running rsyncd

In order to test your solution against a living log file, here's how you can
run rsyncd and generate some logging from it. Typically, rsyncd is configured
using `rsyncd.conf`. For our purposes, this would be enough:

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

## Turning in your solution

We prefer you turn in your solution as a secret GitHub gist. That is, make a
secret gist, clone it, commit your solution there and push it to Github, then
send us the URL to the gist.

The solution should contain everything you wrote and a `run` script that takes
the log file to analyze as the first argument. Your program should not need
anything beyond what Go1.X and Python 3.X ship with and the Prometheus
bindings for those two languages (the latter will be available in the
environment we test your program in).

We highly recommend including a README with your solution where you outline your thoughts,
solution finding process, and anything that is not immediately visible from
the code. It will help us when we evaluate your solution. Especially interesting are things you
considered but did not implement for various reasons.
