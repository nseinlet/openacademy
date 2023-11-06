#!/bin/bash
locust -f lt_crm.py --headless --users 5 --spawn-rate 5 --run-time 1m
