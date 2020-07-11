#!/usr/bin/env bash

gunicorn -c config/gun.py wsgi_gunicorn:app
