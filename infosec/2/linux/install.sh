#!/bin/bash
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi
apt install libuser -y &&
touch /etc/libuser.conf && 
g++ -std=c++11 -o createproject prog.cpp &&
chown root createproject &&
chmod u+s createproject &&
chmod +x createproject
