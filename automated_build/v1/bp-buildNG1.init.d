#!/bin/bash

EXE=/usr/bin/python3
EXEARGS="/root/build.py --url http://buspirate.com/api/build --apikey 7fdb43d3e5657b92e2ca23d51b1b5dd9d7a9bad7 --workdir /root/armdev/bus_pirate_ng/source --bin buspirateNG.bin --hardware NG1 --firmware 8 --make 'make bin'" 
PIDFILE=/var/run/bp-buildNG1.pid
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
