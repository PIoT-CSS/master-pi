#!/bin/bash

# installing system dependencies
echo "Installing system dependencies for MySQL..."
sudo apt install default-libmysqlclient-dev
sudo apt install mysql-client

# install MasterCSS app
echo "Installing MasterCSS app with pip3..."
pip3 install -e .

echo "It's done! Run 'MasterCSS' to start the application. See README.md for more details."
