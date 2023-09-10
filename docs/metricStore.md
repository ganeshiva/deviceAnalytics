# Installation 

## Victoria Metric via docker images
hostMountPath="/home/victoria-metrics-data"
hostPort=8428
sudo docker run -it --rm -v ${hostMountPath}:/victoria-metrics-data -p ${hostPort}:8428 victoriametrics/victoria-metrics