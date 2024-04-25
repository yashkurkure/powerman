sudo apt install -y python3-pip
pip3 install matplotlib
sudo apt install -y cmake stress
sudo modprobe intel_rapl_msr
cd /local && git clone https://github.com/powercap/powercap.git
cd /local/powercap && mkdir _build && cd _build && cmake .. && make && sudo make install