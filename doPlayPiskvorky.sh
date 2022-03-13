#!/bin/bash

# robot-honza: 97fcaf02-ebd8-4a93-9252-cad52f9a8a1f
while true
do
	instances=$(cat "$( dirname "$( realpath "${0}" )" )/AUTO-INSTANCES" 2>/dev/null)
	if [[ ! -f "$( dirname "$( realpath "${0}" )" )/AUTO-INSTANCES" || $( pgrep -cf "piskvorky.*/main.py" ) -ge ${instances} ]]
	then
		echo "Playing too much games in same time, waiting..."
		if [[ ${instances} -eq 0 ]]
		then
			sleep 120
		else
			sleep 30
		fi
		continue
	fi

	
	r=$( sqlite3 "$( dirname "$( realpath "${0}" )" )/centralDB.db" "SELECT * FROM games WHERE status = '97fcaf02-ebd8-4a93-9252-cad52f9a8a1f' OR status = 'waiting'" )
	if [[ -n "${r}" ]]
	then
		echo "Already waiting or playing with robot-honza..."
		sleep 30
		continue
	fi
	python3 "$( dirname "$( realpath "${0}" )" )/main.py" 1>"/tmp/piskv_game_${RANDOM}.log" 2>&1 &
	sleep 30
done
