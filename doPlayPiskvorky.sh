#!/bin/bash

# robot-honza: 97fcaf02-ebd8-4a93-9252-cad52f9a8a1f
while true
do
	if [[ -f "$( dirname "$( realpath "${0}" )" )/STOP" ]]
	then
		echo "Stopped, waiting..."
		sleep 300
		continue
	fi
	
	if [[ $( ps aux | grep "python3 /home/kaspy/scripts/piskvorky_python/main.py" | grep -v "grep" | wc -l ) -gt 1 ]]
	then
		echo "Playing too much games in same time, waiting..."
		sleep 30
		continue
	fi

	
	r=$( sqlite3 "$( dirname "$( realpath "${0}" )" )/centralDB.db" "SELECT * FROM games WHERE status = '97fcaf02-ebd8-4a93-9252-cad52f9a8a1f' OR status = 'waiting'" )
	if [[ -n "${r}" ]]
	then
		echo "Already waiting or playing with robot-honza..."
		sleep 30
		continue
	fi
	python3 "$( dirname "$( realpath "${0}" )" )/main.py" & 2>&1 1>"/tmp/${RANDOM}"
	sleep 30
done
