nmcli connection show
sudo nmcli connection modify "Wired connection 1" ipv4.addresses 192.168.1.100/24
sudo nmcli connection modify "Wired connection 1" ipv4.gateway 192.168.1.1
sudo nmcli connection modify "Wired connection 1" ipv4.dns 8.8.8.8
sudo nmcli connection modify "Wired connection 1" ipv4.method manual
sudo nmcli connection up "Wired connection 1"
sudo hostnamectl set-hostname mephi-2026.domain.local


ip route | grep default > /tmp/network_check.txt
ping -c 3 192.168.1.1 >> /tmp/network_check.txt
ping -c 3 8.8.8.8 >> /tmp/network_check.txt
cat /tmp/network_check.txt

sudo dnf install -y nginx tcpdump libcap-ng-utils


cd /tmp
dnf download tcpdump
sudo rpm -ivh --replacepkgs tcpdump-*.rpm


(echo n; echo p; echo 1; echo ""; echo ""; echo w) | sudo fdisk /dev/sdb
sudo mkfs.ext4 -L MEPHI_DATA /dev/sdb1
sudo mkdir -p /data/mephi-web
echo "LABEL=MEPHI_DATA /data/mephi-web ext4 defaults 0 2" | sudo tee -a /etc/fstab
sudo mount -a
df -h | grep mephi-web



sudo systemctl start nginx
sudo systemctl enable nginx
sudo journalctl -u nginx --since "5 minutes ago" > /tmp/nginx_recent_logs.txt
cat /tmp/nginx_recent_logs.txt

sudo groupadd mephi-devs
sudo useradd -m -s /bin/bash mephi-admin
echo "mephi-admin:P@ssw0rd2026" | sudo chpasswd

--- ЗАКОНЧИЛИ НА ЭТОМ МОМЕНТЕ ---

sudo chmod -s /usr/sbin/tcpdump
sudo setcap 'cap_net_raw,cap_net_admin=+ep' /usr/sbin/tcpdump
getcap /usr/sbin/tcpdump
sudo -u mephi-admin tcpdump --help


-- 5 задание
# 1. Записываем root в файл ограничений
echo "root" | sudo tee /etc/ssh/denied_users

# 2. Ограничиваем права (читать и писать может только root)
sudo chmod 600 /etc/ssh/denied_users
sudo nano /etc/pam.d/login
auth       required     pam_listfile.so onerr=succeed item=user sense=deny file=/etc/ssh/denied_users
sudo nano /etc/pam.d/sshd
auth       required     pam_listfile.so onerr=succeed item=user sense=deny file=/etc/ssh/denied_users


sudo su - mephi-admin
echo "Hello from Student: 368655" | tee /home/mephi-admin/index.html

curl http://localhost
curl http://192.168.1.100
