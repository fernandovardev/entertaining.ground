#!/bin/bash
TIMEOUT=60
DELAY=5

while ! nc -z $1 $2; do
  echo "Waiting for $1:$2 to be available..."
  sleep $DELAY
  if [ $SECONDS -ge $TIMEOUT ]; then
    echo "Timed out waiting for $1:$2"
    exit 1
  fi
done

echo "$1:$2 is available"
shift 2
exec "$@"
