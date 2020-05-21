#!/bin/bash

IP="$(curl icanhazip.com)"

echo "MASTER_IP=localhost
AGENT_PI=203.221.166.146
BROKER_PORT=1883" > .env
