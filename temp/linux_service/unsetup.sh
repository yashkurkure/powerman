sudo systemctl stop myservice.service
sudo systemctl disable myservice.service
sudo rm /etc/systemd/system/myservice.service
sudo systemctl daemon-reload