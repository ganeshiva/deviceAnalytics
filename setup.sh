#!/bin/bash

envId="analytics"
echo "Setting up Python Virtual Environent: ${envId}"
python3 -m venv ${envId}
source ${envId}/bin/activate
python3 -m pip install -r requirements.txt
