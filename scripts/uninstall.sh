#!/bin/bash

OPT_DIR=/opt/terminal_radio/
SYM_LINK=/usr/local/bin/terminal_radio

# remove the code from /opt/
if [ -d $OPT_DIR ]; then
    sudo rm $OPT_DIR -rfi
else
    printf "$OPT_DIR does not exist\n"
fi


sudo rm -i /usr/share/bash-completion/completions/_terminal_radio


# remove the symbolic link
if [ -L $SYM_LINK ]; then
    sudo rm -i $SYM_LINK
else
    printf "$SYM_LINK does not exist\n"
fi

printf "\n\n\n"
printf "Uninstall Complete\n\n"