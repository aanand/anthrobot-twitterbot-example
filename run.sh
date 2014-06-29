#!/bin/bash

set -e

if [ -e ".env" ]; then
  export `cat .env`
fi

if [ -n "$DB_1_PORT" ]; then
  export DATABASE_URL="postgres://$DB_USER:$DB_PASSWORD@$DB_1_PORT_5432_TCP_ADDR:$DB_1_PORT_5432_TCP_PORT/$DB_NAME"
fi

python bot.py
