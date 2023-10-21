#!/bin/bash
set -e

git -C /home/chatdokku/apps/chat-dokku-plugin pull origin main
git -C /home/chatdokku/apps/chat-dokku-plugin push dokku main
