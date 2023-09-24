# Installation of Visualization
Steps to install Grafana OSS

## Installing Grafana OSS release:

```console
sudo apt-get install -y apt-transport-https software-properties-common wget

sudo mkdir -p /etc/apt/keyrings/
wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null
echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
```
Installation CLI

```console
sudo apt-get update

sudo apt-get install grafana
```


## Enable Grafana status:

enable and start service
```console
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
```
Check Status

```console
sudo systemctl status grafana-server
```


## Reference

https://grafana.com/docs/grafana/latest/setup-grafana/installation/