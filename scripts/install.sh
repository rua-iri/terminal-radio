#!/bin/bash
set -e

# Install required packages
printf "Installing Packages: "
if [ -f /etc/debian_version ]; then
    sudo apt install mpv sqlite3 python3-venv python3-pip libsixel-bin
elif [ -f /etc/fedora-release ]; then
    sudo dnf install mpv sqlite3 python3-pip libsixel libsixel-utils
elif [ -f /etc/arch-release ]; then
    sudo pacman -Syu gcc python3 python-pipenv mpv libsixel rsync
else
    echo "OS not currently supported"
    exit 1
fi
printf "Done\n\n"



# Set up Python virtual environment
VENV='.venv'
PYTHON=$VENV/bin/python3
PIP=$VENV/bin/pip3

printf "Installing Python Requirements: "
python3 -m venv $VENV
$PIP install -r requirements.txt 1> /dev/null
printf "Done\n\n"




# Create necessary files and directories
printf "Creating Necessary Files and Folders: "
if [ ! -d logs ]; then
    mkdir logs/
fi

if [ ! -f resource/radio_sources.sqlite ]; then
    sqlite3 resource/radio_sources.sqlite < resource/schema.sql
fi

printf "Done\n\n"




# move to installation directory and set up
# symbolic link to add to $PATH
printf "Moving to Installation Directory: "

# prevent overwriting the database
if [ -f /opt/terminal_radio/resource/radio_sources.sqlite ]; then 
    sudo rsync -av --exclude='resource/radio_sources.sqlite' . /opt/terminal_radio
else
    sudo rsync -av . /opt/terminal_radio
fi


if [ ! -L /usr/local/bin/terminal_radio ]; then 
    sudo ln -s /opt/terminal_radio/scripts/run.sh /usr/local/bin/terminal_radio
fi

sudo chown $USER /opt/terminal_radio/
sudo cp ./scripts/autocomplete.sh /usr/share/bash-completion/completions/_terminal_radio
printf "Done\n\n\n\n"



final_output=$(cat << "EOF"
\e[32m
 _                      _             _                 _ _       
| |                    (_)           | |               | (_)      
| |_ ___ _ __ _ __ ___  _ _ __   __ _| |  _ __ __ _  __| |_  ___  
| __/ _ | '__| '_ ` _ \| | '_ \ / _` | | | '__/ _` |/ _` | |/ _ \ 
| ||  __| |  | | | | | | | | | | (_| | | | | | (_| | (_| | | (_) |
 \__\___|_|  |_| |_| |_|_|_| |_|\__,_|_| |_|  \__,_|\__,_|_|\___/ 
                                     ______                       
                                    |______|                      
\e[0m


Setup Complete!


\e[32mterminal_radio\e[0m - start the application
\e[32mterminal_radio update\e[0m - Manage radio sources
\e[32mterminal_radio logs\e[0m - View the application logs
\e[32mterminal_radio show\e[0m - View the list of sources
\e[32mterminal_radio stats\e[0m - View the most listened to stations
\e[32mterminal_radio help\e[0m - View the help menu\n
EOF
)

echo -e "$final_output"





