#!/bin/bash
flock /var/lock/bot.lock python /home/nlpuser/ATM-Bot/main.py