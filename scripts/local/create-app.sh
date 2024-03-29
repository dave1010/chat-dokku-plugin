#!/bin/bash
set -e

APP_NAME=$1

if dokku apps:exists $APP_NAME > /dev/null; then
  echo "Error: App $APP_NAME already exists." >&2
  exit 1
fi

dokku apps:create $1
mkdir /home/chatdokku/apps/$1

cd /home/chatdokku/apps/$1
git init
git remote add dokku dokku@localhost:$APP_NAME

echo "App $APP_NAME has been created. Add and commit files, then run 'git push dokku main' to deploy"
echo "Dokku buildpacks needs a .static, requiremnts.txt, package.json, composer.json, etc."
echo "Or use .buildpacks or Dockerfile to customise."
echo "The first push may time out"