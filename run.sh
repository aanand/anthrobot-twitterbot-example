#!/bin/bash

set -e

if [ -e ".env" ]; then
  export `cat .env`
fi

python bot.py
