# Installation of Storage
Steps to installation Victoria Metrics

## Docker Installation 
```console
hostMountPath="/home/victoria-metrics-data"
hostPort=8428
sudo docker run -it --rm -v ${hostMountPath}:/victoria-metrics-data -p ${hostPort}:8428 victoriametrics/victoria-metrics
```

## Binary installation
Download and extract appropriate build for your platform 
https://github.com/VictoriaMetrics/VictoriaMetrics/releases

### Steps to Create 'victoriametrics' Service:

Create a new systemd config file 
```console
sudo nano /lib/systemd/system/victoriametrics.service
```

### Content of "/lib/systemd/system/victoriametrics.service"

change path to suite your folder

```console

[Unit]
Description=VictoriaMetrics
After=network.target

[Service]
Type=simple
StartLimitBurst=5
StartLimitInterval=0
Restart=on-failure
RestartSec=1
PIDFile=/run/victoriametrics/victoriametrics.pid
ExecStart=/usr/local/bin/victoriametrics -storageDataPath //victoriaMetric/victoria-metrics-data -retentionPeriod 12
ExecStop=/bin/kill -s SIGTERM $MAINPID

[Install]
WantedBy=multi-user.target

Set the file limits for the service:
mkdir /etc/systemd/system/victoriametrics.service.d
In this folder create a file ulimit.conf with the following:

[Service]
LimitNOFILE=32000
LimitNPROC=32000
```

### Enable deviceAnalytics service
```console
sudo systemctl daemon-reload
sudo systemctl enable victoriametrics.service
sudo systemctl start victoriametrics.service
```


### Check deviceAnalytics service status 
```console
sudo systemctl status victoriametrics
```

## Reference

https://docs.victoriametrics.com/Quick-Start.html

