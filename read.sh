#!/usr/bin/bash

uj_to_j=1000000
start_time=`date +%s`
start_pwr=`sudo cat /sys/devices/virtual/powercap/intel-rapl/intel-rapl\:0/energy_uj`

while true; do
	date=`date +"%T.%3N"`
	pwr_uj=`sudo cat /sys/devices/virtual/powercap/intel-rapl/intel-rapl\:0/energy_uj`
	pwr_since_start=$(($pwr_uj - $start_pwr))
	echo "${date}: ${pwr_since_start} since start; ${pwr_uj} since boot"
	pwr_j=$(($pwr_since_start / $uj_to_j))
	echo "joules: ${pwr_j}"
	now=`date +%s`
	sample_time=$(($now - $start_time))
	if [ $sample_time -gt 0 ]; then
		watts=$(($pwr_j / $sample_time))
		echo "watts: ${watts}"
	fi
	sleep 1
done
