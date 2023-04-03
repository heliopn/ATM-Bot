#!/bin/bash
flock /var/lock/bot.lock conda init bash & conda activate nlp & python /home/iskandar/Documents/Insper/9_semestre/ATM-Bot/main.py