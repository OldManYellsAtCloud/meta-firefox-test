#!/bin/sh
export DISPLAY=:0
export WAYLAND_DISPLAY=/run/wayland-0

# Disable screen blanking and screensaver
# do this before anything else. Should do no harm,
# even if the rest fails. This is only for x11.
# For weston this is done in /etc/xdg/weston/weston.ini
xset s off
xset s noblank
xset -dpms

if [ $# -ne 1 ]; then
  echo Missing test folder argument!
  exit 1
fi

# the tests should be in the home folder
cd /home/root

pytest --junitxml=./$1.xml $1/

