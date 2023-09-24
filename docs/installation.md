# Installation

# Prerequisite

1. Python 3.10
2. Packages required (requirements.txt) 

# Steps to install:

1. Python 3.10

```console
sudo apt install python3.10
```

2. Python3-pip
```console
sudo apt install python3-pip
```

3. Python3-venv
```console
sudo apt install python3-venv
```

4. Exec below command to create venv and install requirements.txt 
```console
source setupExecEnv.sh
```

# Cloning the Code repo:

```console
git clone https://github.com/ganeshiva/deviceAnalytics.git
# or
# Download with out git 
wget https://github.com/ganeshiva/deviceAnalytics/archive/refs/heads/main.zip -O deviceAnalytics.zip
unzip deviceAnalytics.zip
```

# Installing Code dependencies:

cd deviceAnalytics
source ./setupExecEnv.sh


# Steps to Create 'deviceAnalytics' Service:

Create a new systemd config file 
```console
sudo nano /lib/systemd/system/deviceAnalytics.service
```

### Content of "/lib/systemd/system/deviceAnalytics.service"

change path to suite your folder

```console

[Unit]
 Description=DeviceAnalytics 
 After=network.target victoriametrics.service

[Service]
 Type=simple
 StartLimitBurst=5
 StartLimitInterval=0
 Restart=on-failure
 RestartSec=5
 WorkingDirectory=/home/user/deviceAnalytics/
 ExecStart=/bin/bash -c  '/home/user/deviceAnalytics/start.sh'
 ExecStop=/bin/kill -s SIGTERM $MAINPID
 
[Install]
 WantedBy=multi-user.target

```

### Enable deviceAnalytics service
```console
sudo systemctl daemon-reload
sudo systemctl enable deviceAnalytics.service
```


### Check deviceAnalytics service status 
```console
sudo systemctl daemon-reload
sudo systemctl status deviceAnalytics
```
