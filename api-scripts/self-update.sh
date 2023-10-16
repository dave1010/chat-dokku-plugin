#!/bin/bash
set -e

ssh chatdokku@172.17.0.1 "git -C /home/chatdokku/apps/chat-dokku-plugin pull origin main"

ssh chatdokku@172.17.0.1 "git -C /home/chatdokku/apps/chat-dokku-plugin push dokku main"
