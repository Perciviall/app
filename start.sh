#!/bin/bash

# Set a default port if PORT is not set
PORT=${PORT:-5000}

waitress-serve --port=$PORT app:app
