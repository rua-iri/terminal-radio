#!/usr/bin/env bash

# lsix: like ls, but for images.
# Shows thumbnails of images with titles directly in terminal.

# Requirements: just ImageMagick (and a Sixel terminal, of course)

# Version 1.9.1
# B9 June 2024

# See end of file for USAGE.


# The following defaults may be overridden if autodetection succeeds.
numcolors=16     # Default number of colors in the palette.
background=white # Default montage background.
foreground=black # Default text color.
width=800	 # Default width of screen in pixels.

# Feel free to edit these defaults to your liking.
tilesize=120	       # Width and height of each tile in the montage.
tilewidth=$tilesize    # (or specify separately, if you prefer)
tileheight=$tilesize

# If you get questionmarks for Unicode filenames, try using a different font.
# You can list fonts available using `convert -list font`.
#fontfamily=Droid-Sans-Fallback		# Great Asian font coverage
#fontfamily=Dejavu-Sans			# Wide coverage, comes with GNU/Linux
#fontfamily=Mincho			# Wide coverage, comes with MS Windows

# Default font size is based on width of each tile in montage.
fontsize=$((tilewidth/10))
#fontsize=16		     # (or set the point size directly, if you prefer)

timeout=0.25		    # How long to wait for terminal to respond
			    # to a control sequence (in seconds).


autodetect() {
    # Various terminal automatic configuration routines.

    # Don't show escape sequences the terminal doesn't understand.
    stty -echo			# Hush-a Mandara Ni Pari

    # IS TERMINAL SIXEL CAPABLE?		# Send Device Attributes
    IFS=";?c" read -a REPLY -s -t 1 -d "c" -p $'\e[c' >&2
    for code in "${REPLY[@]}"; do
	if [[ $code == "4" ]]; then
	    hassixel=yup
	    break
	fi
    done

    # YAFT is vt102 compatible, cannot respond to vt220 escape sequence.
    if [[ "$TERM" == yaft* ]]; then hassixel=yeah; fi

    if [[ -z "$hassixel" && -z "$LSIX_FORCE_SIXEL_SUPPORT" ]]; then
	cat <<-EOF >&2
	Error: Your terminal does not report having sixel graphics support.

	Please use a sixel capable terminal, such as xterm -ti vt340, or
	ask your terminal manufacturer to add sixel support.

	You may test your terminal by viewing a single image, like so:

		convert foo.jpg  -geometry 800x480  sixel:-

	If your terminal actually does support sixel, please file a bug
	report at http://github.com/hackerb9/lsix/issues
	EOF
	read -s -t 1 -d "c" -p $'\e[c' >&2
	if [[ "$REPLY" ]]; then
	    echo
	    cat -v <<< "Please mention device attribute codes: ${REPLY}c"
	fi

	exit 1
    fi

    # SIXEL SCROLLING (~DECSDM) is now presumed to be enabled.
    # See https://github.com/hackerb9/lsix/issues/41 for details.

    # TERMINAL COLOR AUTODETECTION.
    # Find out how many color registers the terminal has
    IFS=";"  read -a REPLY -s -t ${timeout} -d "S" -p $'\e[?1;1;0S' >&2
    [[ ${REPLY[1]} == "0" ]] && numcolors=${REPLY[2]}

    # YAFT is vt102 compatible, cannot respond to vt220 escape sequence.
    if [[ "$TERM" == yaft* ]]; then numcolors=256; fi

    # Increase colors, if needed
    if [[ $numcolors -lt 256 ]]; then
	# Attempt to set the number of colors to 256.
	# This will work for xterm, but fail on a real vt340.
	IFS=";"  read -a REPLY -s -t ${timeout} -d "S" -p $'\e[?1;3;256S' >&2
	[[ ${REPLY[1]} == "0" ]] && numcolors=${REPLY[2]}
    fi

    # Query the terminal background and foreground colors.
    IFS=";:/"  read -a REPLY -r -s -t ${timeout} -d "\\" -p $'\e]11;?\e\\' >&2
    if [[ ${REPLY[1]} =~ ^rgb ]]; then
	# Return value format: $'\e]11;rgb:ffff/0000/ffff\e\\'.
	# ImageMagick wants colors formatted as #ffff0000ffff.
	background='#'${REPLY[2]}${REPLY[3]}${REPLY[4]%%$'\e'*}
	IFS=";:/"  read -a REPLY -r -s -t ${timeout} -d "\\" -p $'\e]10;?\e\\' >&2
	if [[ ${REPLY[1]} =~ ^rgb ]]; then
	    foreground='#'${REPLY[2]}${REPLY[3]}${REPLY[4]%%$'\e'*}
	    # Check for "Reverse Video" (DECSCNM screen mode).
	    IFS=";?$"  read -a REPLY -s -t ${timeout} -d "y" -p $'\e[?5$p'
	    if [[ ${REPLY[2]} == 1 || ${REPLY[2]} == 3 ]]; then
		temp=$foreground
		foreground=$background
		background=$temp
	    fi
	fi
    fi
    # YAFT is vt102 compatible, cannot respond to vt220 escape sequence.
    if [[ "$TERM" == yaft* ]]; then background=black; foreground=white; fi

    # Send control sequence to query the sixel graphics geometry to
    # find out how large of a sixel image can be shown.
    IFS=";"  read -a REPLY -s -t ${timeout} -d "S" -p $'\e[?2;1;0S' >&2
    if [[ ${REPLY[2]} -gt 0 ]]; then
	width=${REPLY[2]}
    else
	# Nope. Fall back to dtterm WindowOps to approximate sixel geometry.
	IFS=";" read -a REPLY -s -t ${timeout} -d "t" -p $'\e[14t' >&2
	if [[ $? == 0  &&  ${REPLY[2]} -gt 0 ]]; then
	    width=${REPLY[2]}
	fi
    fi

    # BUG WORKAROUND: XTerm cannot show images wider than 1000px.
    # Remove this hack once XTerm gets fixed. Last checked: XTerm(344)
    if [[ $TERM =~ xterm && $width -ge 1000 ]]; then  width=1000; fi

    # Space on either side of each tile is less than 0.5% of total screen width
    tilexspace=$((width/201))
    tileyspace=$((tilexspace/2))
    # Figure out how many tiles we can fit per row. ("+ 1" is for -shadow).
    numtiles=$((width/(tilewidth + 2*tilexspace + 1)))
}

autodetect