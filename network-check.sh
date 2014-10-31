#!/bin/bash

while true ; do
   if ifconfig wlan0 | grep -q "inet addr:" ; then
      sleep 300 #300 secondes
   else
      ifup --force wlan0
      sleep 20
   fi
done
