About: route.py

USAGE:
- Run/include route.py to configure apache2 to Listen on port 80 and configure iprouting to redirect traffic going to the specified IP to instead go to the host machine’s IP. 
- On the target, browse to the domain of the redirected IP.

Note: The target and router must be arpspoofed for this to work!


REQUIREMENT:
- You MUST ARP-SPOOF your machine with the target and network router. This redirects the target’s traffic through your machine.


ARPSPOOF:
Included is the arpspoof script from Kali Linux. You will need to run (and persist) two running instances of arpspoof. Run the arpspoof instances using the following params:
1. arpspoof -t A.B.C.D W.X.Y.Z
2. arpspoof -t W.X.Y.Z A.B.C.D

Note: A.B.C.D and W.X.Y.Z are different IP addresses. One is the IP of the router, the other is the IP of the target.


NOTES:
- The route.py script contains three IP ranges for the domain to redirect. In the event the domain uses other IPs they will need to be added.
- Tested on Kali Linux.