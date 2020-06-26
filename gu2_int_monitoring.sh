#!/bin/bash

pkill firefox

WWW_DIR=/var/www/html
SCRIPT_DIR=/home/zxnak37/PycharmProjects/gu2_maintenance_scripts
PATH=$SCRIPT_DIR/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin

cd $SCRIPT_DIR
source $SCRIPT_DIR/venv/bin/activate
$SCRIPT_DIR/venv/bin/python gu2_int_monitoring.py

cp monitoring.html $WWW_DIR
cp css.css $WWW_DIR
cp -R styles $WWW_DIR

