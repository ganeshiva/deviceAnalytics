#!/bin/bash

envId="dev"
echo "Setting up Python Virtual Environment: '${envId}'"
python3 -m venv ${envId}
echo "Activating Environment: '${envId}'"
source ${envId}/bin/activate
echo "Installing pip packages from 'requirementsDev.txt'"
python3 -m pip install -r requirementsDev.txt