#!/bin/bash
systemctl start nginx

cd /root/ghc-publication || exit
uv run gunicorn django_project.wsgi:application --bind 0.0.0.0:80