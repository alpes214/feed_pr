#!/bin/bash

pytest --cov=app -s -v ./tests 
coverage report -m
