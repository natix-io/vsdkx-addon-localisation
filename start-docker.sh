#!/bin/bash
sudo service docker start;
sudo xhost +;
xhost +;
sudo docker-compose down;


findArg() {
# function that will find text in file arguments
#	format:
#		findArg myArg $@
#	where:
#		myArg - (string) text that we are looking in arguments
# 		$@ - (bash default string) text that we ar looking word in -
#			$@ means arguments passed to file

	local count=0;
	local target=$(echo $1 | tr '[:upper:]' '[:lower:]');

	# loop throught all arguments, passed to function
	for i in $*; do

		# store first passed argument as target
		#	that we are looking in string
		((count++))
		if ((count==1)); then
			continue;
		fi

		# compare file arguments to selected argument
		#	all in lowercase
		i=$(echo $i | tr '[:upper:]' '[:lower:]');
		if [[ $i == $target ]]; then

			# return 1 and exit
			echo 1;
			return;
		fi

	done
	# return 0 if not found
	echo 0;
}

if [[ -f /getSecrets ]]; then
	echo $(/getSecrets --root echo init);
else
	echo "\e[31m|No secret manager found on device, you might be asked for sudo password\e[39m";
fi

if [[ $(sudo service --status-all | grep docker | awk {'print $2'}) == "-" ]]; then
	echo -e "|\e[33mStarting docker\e[39m"

	# stop redis server
	sudo service docker start;

	# check if service ws stopped successfully
	if [[ $(sudo service --status-all | grep docker | awk {'print $2'}) == "+" ]]; then
		echo -e "\e[32m|--docker started successfully\e[39m";
	else
		echo -e "\e[31m|--could not start docker\e[39m";
	fi
else
	echo "\e[32m|docker is running\e[39m"
fi


# enable display output from container
if [[ $(uname) == Darwin ]]; then
    path=$(pwd);
    kill -9 $(lsof -n -i | grep 6000 | awk {'print $2'});
    osascript -e 'tell application "Terminal" to do script "TMOUT=1; socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:\\\"$DISPLAY\\\""'
    sleep 2;
    echo please input this in docker-compose as -DISPLAY:$(ifconfig en0 | grep 192 | awk {'print $2'}):0
    sleep 3;
else
    sudo xhost +;
fi

# clean up leftovers from last execution
sudo docker-compose down;

# clen up networks from last run
if (($(sudo docker network ls | grep car | awk {'print $1'} | wc -w) != 0)); then
	sudo docker network rm $(sudo docker network ls | grep car | awk {'print $1'});
	echo "Cleaned up depreciated sensitive area detection networks";
else
	echo "no sensitive area detection network was up";
fi;

if [[ $(findArg BUILD $@) == 1 ]]; then
	sudo aws ecr get-login-password --region eu-central-1 | sudo docker login --username AWS --password-stdin 212730513262.dkr.ecr.eu-central-1.amazonaws.com;
	sudo docker-compose build;
fi

sudo docker-compose up;
