#!/bin/bash

apt-get install bluetooth -y
apt-get install bluez -y
apt-get install pi-bluetooth -y
apt-get install python-bluez -y

cp ./dbus-org.bluez.service /etc/systemd/system/dbus-org.bluez.service


apt-get install python-picamera python3-picamera -y
sudo apt-get install python-pip libglib2.0-dev
apt-get install python-imaging -y
pip install bluepy
pip install pexpect
pip install requests
apt-get install -y  rng-tools