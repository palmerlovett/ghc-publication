#!/bin/bash

sudo systemctl start nginx

cd /root/ghc-publication || exit
/root/.local/bin/uv run gunicorn django_project.wsgi:application --bind 127.0.0.1:8000