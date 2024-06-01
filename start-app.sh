#!/bin/sh


pytest
TEST_EXIT_CODE=$?

if [ $TEST_EXIT_CODE -eq 0 ]; then
  echo "Tests passed. Building and starting the application."
  docker-compose up --build -d
else
  echo "Tests failed. Exiting."
  exit 1
fi
