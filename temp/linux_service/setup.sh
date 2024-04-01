# Notes
# View logs: journalctl -u myservice.service


sudo cp /local/repository/temp/linux_service/myservice.service /etc/systemd/system/myservice.service
sudo systemctl enable myservice.service
sudo systemctl start myservice.service