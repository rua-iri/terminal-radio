#!/bin/bash

OPT_DIR=/opt/terminal_radio/
SYM_LINK=/usr/local/bin/terminal_radio

# remove the code from /opt/
if [ -d $OPT_DIR ]; then
    sudo rm $OPT_DIR -rf
else
    echo "$OPT_DIR does not exist"
fi


sudo rm /usr/share/bash-completion/completions/_terminal_radio


# remove the symbolic link
if [ -L $SYM_LINK ]; then
    sudo rm $SYM_LINK
else
    echo "$SYM_LINK does not exist"
fi

echo "\n\n\n"
echo "Uninstal Complete"