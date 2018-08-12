#!/bin/bash

service="couchdb"

if (( $(ps -ef | grep -v grep | grep $service | wc -l) > 0 ))
then
	exit
else
	echo "$(date) - acorda, djabo!!!" >> status_couchdb
	sudo service $service restart
fi