#!/usr/bin/env bash

power_status=$(ddcutil --display 1 getvcp D6 | cut -d "," -f 1 | awk '{print $NF}')

if [[ $power_status == "Off" ]]; then
	ddcutil display 1 setvcp D6 01
else
	echo "Monitor HDMI-A-1 power status is already On."
fi
