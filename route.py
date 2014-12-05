import os
import subprocess
import shutil

# Detect current IP address.
cmd = "/sbin/ifconfig | grep \'inet addr\'"
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print cmd
print p.wait()
(output, error) = p.communicate()
print (output, error), "\n"
rawIPList = output.split()
modIPList = []
myIP = ""

for ip in rawIPList:
    if 'addr:' in ip:
        modIPList.append(ip[5:])

for ip in modIPList:
    if ip != '127.0.0.1':
        myIP = ip

print "IP is " + myIP + "\n"

# Add Listener to apache2 service for IP.
virtHost = "NameVirtualHost *:80"
listener = "Listen " + myIP + ":80"
portConf = "# If you just change the port or add more ports here, you will likely also\n# have to change the VirtualHost statement in\n# /etc/apache2/sites-enabled/000-default\n# This is also true if you have upgraded from before 2.2.9-3 (i.e. from\n# Debian etch). See /usr/share/doc/apache2.2-common/NEWS.Debian.gz and\n# README.Debian.gz\n\n" + virtHost + "\n" + listener + "\n\n<IfModule mod_ssl.c>\n# If you add NameVirtualHost *:443 here, you will also have to change\n# the VirtualHost statement in /etc/apache2/sites-available/default-ssl\n# to <VirtualHost *:443>\n# Server Name Indication for SSL named virtual hosts is currently not\n# supported by MSIE on Windows XP.\nListen 443\n</IfModule>\n\n<IfModule mod_gnutls.c>\nListen 443\n</IfModule>\n\n"
path = "/etc/apache2/ports.conf"
bak = "/etc/apache2/ports.conf.bak"

if os.path.isfile(path):
    if not os.path.isfile(bak):
        shutil.copyfile(path, bak)
    f = open(path, "w")
    f.write(portConf)
    f.close()
    del f

# Restart apache service.
cmd = "service apache2 restart"
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print cmd
print p.wait()
print p.communicate(), "\n"

# Enable iprouting.
cmd = "echo 1 > /proc/sys/net/ipv4/ip_forward"
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print cmd
print p.wait()
print p.communicate(), "\n"

# Configure routing table for the first domain IP.
cmd = "iptables -t nat -A PREROUTING -d 31.13.69.1/24 -j DNAT --to-destination " + myIP
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print cmd
print p.wait()
print p.communicate(), "\n"

# Configure routing table for the second domain IP.
cmd = "iptables -t nat -A PREROUTING -d 31.13.70.1/24 -j DNAT --to-destination " + myIP
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print cmd
print p.wait()
print p.communicate(), "\n"

# Configure routing table for the third domain IP.
cmd = "iptables -t nat -A PREROUTING -d 31.13.71.1/24 -j DNAT --to-destination " + myIP
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print cmd
print p.wait()
print p.communicate(), "\n"

# Configure the routing table to accept incoming traffic on port 80.
cmd = "iptables -A INPUT -p tcp --dport 80 -j ACCEPT"
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print cmd
print p.wait()
print p.communicate(), "\n"

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