#! /bin/sh
perl -ane '{ if(m/[[:^ascii:]]/) { print  } }' "$1"

