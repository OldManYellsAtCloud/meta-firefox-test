#!/bin/sh
export DISPLAY=:0

# Disable screen blanking and screensaver
# do this before anything else. Should do no harm,
# even if the rest fails.
xset s off
xset s noblank
xset -dpms

if [ $? -ne 1 ]; then
  echo Missing test folder argument!
  exit 1
fi

# the tests should be in the home folder
cd ~

pytest --junitxml=./$1.xml $1/

