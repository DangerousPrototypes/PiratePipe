#!/bin/bash

EXE=/usr/bin/python3
EXEARGS="{path_to_build.py}/build.py --url http://{upload_API_url} --apikey {api_key} --workdir {path_to_source}/bus_pirate_ng/source --bin buspirateNG.bin" 
PIDFILE=/var/run/bp-build.pid
case "$1" in
  start)
    echo -n "Starting server: Bus Pirate auto build"
    /sbin/start-stop-daemon --start --quiet --pidfile $PIDFILE --make-pidfile --background --exec $EXE -- $EXEARGS
    echo "."
    ;;
  stop)
    echo -n "Stopping server: Bus Pirate auto build"
    /sbin/start-stop-daemon --stop --quiet --pidfile $PIDFILE
    echo "."
    ;;
  restart)
    $0 stop
    $0 start
    ;;
  *)
  echo "Usage: /etc/init.d/bp-build {start|stop|restart}"
  exit 1
esac
exit 0
