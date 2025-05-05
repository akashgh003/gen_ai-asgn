#!/bin/bash
echo "Starting Gunicorn server..."
gunicorn --bind 0.0.0.0:8080 wsgi:app