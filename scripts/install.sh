#!/bin/bash
set -e



# Create necessary files and directories
printf "Creating Necessary Files and Folders: "
if [ ! -d logs ]; then
  mkdir logs/
fi

if [ ! -f resource/radio_sources.sqlite ]; then
  sqlite3 resource/radio_sources.sqlite <resource/schema.sql
fi

printf "Done\n\n"

# move to installation directory and set up
# symbolic link to add to $PATH
printf "Moving to Installation Directory: "

# prevent overwriting the important files and copying unnecesary files
if [ -f /opt/terminal_radio/resource/radio_sources.sqlite ]; then
  EXCLUDE_DIRS=(
    --exclude='resource/radio_sources.sqlite'
    --exclude='logs/'
    --exclude='resource/config.yaml'
  )

  sudo rsync -qav "${EXCLUDE_DIRS[@]}" . /opt/terminal_radio
else
  sudo rsync -qav . /opt/terminal_radio
fi

if [ ! -L /usr/local/bin/terminal_radio ]; then
  sudo ln -s /opt/terminal_radio/terminal_radio /usr/local/bin/terminal_radio
fi

sudo chown $USER /opt/terminal_radio/
sudo cp ./scripts/autocompletions/autocomplete.sh /usr/share/bash-completion/completions/_terminal_radio
printf "Done\n\n\n\n"

final_output=$(
  cat <<"EOF"
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
