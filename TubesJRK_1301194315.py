# Nama  : Zaky Mahfudz Pasha
# NIM   : 1301194315
# Kelas : IF-44-02

#!/usr/bin/env python
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import Link,TCLink,Intf
from subprocess import Popen,PIPE
from mininet.log import setLogLevel
import time
import os

if '__main__' == __name__:
    os.system('mn -c')
    setLogLevel('info')
    net = Mininet(link=TCLink)
    key = "net.mptcp.mptcp_enable"
    value = 0 #if you want to activate mptcp, change the value to 1
    p = Popen("sysctl -w %s=%s" % (key,value), shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr=p.communicate()
    print("stdout=", stdout, "stderr=", stderr)
    
    #Topologi
    HostA = net.addHost('HostA')
    HostB = net.addHost('HostB')
    R1 = net.addHost('R1')
    R2 = net.addHost('R2')
    R3 = net.addHost('R3')
    R4 = net.addHost('R4')
    
    #Bandwidth (/Mbps)
    bwlink1={'bw':1}
    bwlink2={'bw':0.5}
    
    #Buat jaringan yang ada pada topologi
    net.addLink(HostA,R1,cls=TCLink, **bwlink1)
    net.addLink(HostA,R2,cls=TCLink, **bwlink1)
    net.addLink(HostB,R3,cls=TCLink, **bwlink1)
    net.addLink(HostB,R4,cls=TCLink, **bwlink1)
    net.addLink(R1,R3,cls=TCLink, **bwlink2)
    net.addLink(R1,R4,cls=TCLink, **bwlink1)
    net.addLink(R2,R3,cls=TCLink, **bwlink1)
    net.addLink(R2,R4,cls=TCLink, **bwlink2)

    #net.addLink(R1,HostA,cls=TCLink, **bwlink1) #R1-eth0 HostA-eth0
    #net.addLink(R1,R3,cls=TCLink, **bwlink2) #R1-eth1 R3-eth0
    #net.addLink(R1,R4,cls=TCLink, **bwlink1) #R1-eth2 R4-eth0
    
    #net.addLink(R2,R3,cls=TCLink, **bwlink1) #R2-eth0 R3-eth1
    #net.addLink(R2,R4,cls=TCLink, **bwlink2) #R2-eth1 R4-eth1
    #net.addLink(R2,HostA,cls=TCLink, **bwlink1) #R2-eth2 HostA-eth1
    
    #net.addLink(R3,HostB,cls=TCLink, **bwlink1) #R3-eth2 HostB-eth0
    #net.addLink(R4,HostB,cls=TCLink, **bwlink1) #R4-eth2 HostB-eth1
        
    net.build()

    #0 menandakan belum ada IP address
    HostA.cmd("ifconfig HostA-eth0 0")
    HostA.cmd("ifconfig HostA-eth1 0")
    
    HostB.cmd("ifconfig HostB-eth0 0")
    HostB.cmd("ifconfig HostB-eth1 0")
    
    R1.cmd("ifconfig R1-eth0 0")
    R1.cmd("ifconfig R1-eth1 0")
    R1.cmd("ifconfig R1-eth2 0")
    
    R2.cmd("ifconfig R2-eth0 0")
    R2.cmd("ifconfig R2-eth1 0")
    R2.cmd("ifconfig R2-eth2 0")
    
    R3.cmd("ifconfig R3-eth0 0")
    R3.cmd("ifconfig R3-eth1 0")
    R3.cmd("ifconfig R3-eth2 0")
    
    R4.cmd("ifconfig R4-eth0 0")
    R4.cmd("ifconfig R4-eth1 0")
    R4.cmd("ifconfig R4-eth2 0")
    
    #IP forwarding di setiap router, echo 1 menandakan enable, 0 disable
    R1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    R2.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    R3.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    R4.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    
    #IP adressing
    HostA.cmd("ifconfig HostA-eth0 192.168.1.1 netmask 255.255.255.0")
    HostA.cmd("ifconfig HostA-eth1 192.168.2.1 netmask 255.255.255.0")
    
    HostB.cmd("ifconfig HostB-eth0 192.168.3.1 netmask 255.255.255.0")
    HostB.cmd("ifconfig HostB-eth1 192.168.4.1 netmask 255.255.255.0")
    
    R1.cmd("ifconfig R1-eth0 192.168.1.2 netmask 255.255.255.0")
    R1.cmd("ifconfig R1-eth1 192.168.5.1 netmask 255.255.255.0")
    R1.cmd("ifconfig R1-eth2 192.168.7.1 netmask 255.255.255.0")
    
    R2.cmd("ifconfig R2-eth0 192.168.2.2 netmask 255.255.255.0")
    R2.cmd("ifconfig R2-eth1 192.168.8.1 netmask 255.255.255.0")
    R2.cmd("ifconfig R2-eth2 192.168.6.1 netmask 255.255.255.0")
    
    R3.cmd("ifconfig R3-eth0 192.168.3.2 netmask 255.255.255.0")
    R3.cmd("ifconfig R3-eth1 192.168.5.2 netmask 255.255.255.0")
    R3.cmd("ifconfig R3-eth2 192.168.8.2 netmask 255.255.255.0")
    
    R4.cmd("ifconfig R4-eth0 192.168.4.2 netmask 255.255.255.0")
    R4.cmd("ifconfig R4-eth1 192.168.7.2 netmask 255.255.255.0")
    R4.cmd("ifconfig R4-eth2 192.168.6.2 netmask 255.255.255.0")
    
    #Routing table HostA
    HostA.cmd("ip rule add from 192.168.1.1 table 1")
    HostA.cmd("ip rule add from 192.168.2.1 table 2")
    HostA.cmd("ip route add 192.168.1.0/24 dev HostA-eth0 scope link table 1")
    HostA.cmd("ip route add default via 192.168.1.2 dev HostA-eth0 table 1")
    HostA.cmd("ip route add 192.168.2.0/24 dev HostA-eth1 scope link table 2")
    HostA.cmd("ip route add default via 192.168.2.2 dev HostA-eth1 table 2")
    HostA.cmd("ip route add default scope global nexthop via 192.168.1.2 dev HostA-eth0")
    
    #Routing table HostB
    HostB.cmd("ip rule add from 192.168.3.1 table 1")
    HostB.cmd("ip rule add from 192.168.4.1 table 2")
    HostB.cmd("ip route add 192.168.3.0/24 dev HostB-eth0 scope link table 1")
    HostB.cmd("ip route add default via 192.168.3.2 dev HostB-eth0 table 1")
    HostB.cmd("ip route add 192.168.4.0/24 dev HostB-eth1 scope link table 2")
    HostB.cmd("ip route add default via 192.168.4.2 dev HostB-eth1 table 2")
    HostB.cmd("ip route add default scope global nexthop via 192.168.3.2 dev HostB-eth0")
    
    #Routing table R1
    R1.cmd("ip rule add from 192.168.1.2 table 1")
    R1.cmd("ip rule add from 192.168.5.1 table 2")
    R1.cmd("ip rule add from 192.168.7.1 table 3")
    R1.cmd("ip route add 192.168.1.0/24 dev R1-eth0 scope link table 1")
    R1.cmd("ip route add default via 192.168.1.1 dev R1-eth0 table 1")
    R1.cmd("ip route add 192.168.5.0/24 dev R1-eth1 scope link table 2")
    R1.cmd("ip route add default via 192.168.5.2 dev R1-eth1 table 2")
    R1.cmd("ip route add 192.168.7.0/24 dev R1-eth2 scope link table 3")
    R1.cmd("ip route add default via 192.168.7.2 dev R1-eth2 table 3")
    R1.cmd("ip route add default scope global nexthop via 192.168.1.1 dev R1-eth0")
    
    #Routing table R2
    R2.cmd("ip rule add from 192.168.2.2 table 1")
    R2.cmd("ip rule add from 192.168.8.1 table 2")
    R2.cmd("ip rule add from 192.168.6.1 table 3")
    R2.cmd("ip route add 192.168.2.0/24 dev R2-eth0 scope link table 1")
    R2.cmd("ip route add default via 192.168.2.1 dev R2-eth0 table 1")
    R2.cmd("ip route add 192.168.8.0/24 dev R2-eth1 scope link table 2")
    R2.cmd("ip route add default via 192.168.8.2 dev R2-eth1 table 2")
    R2.cmd("ip route add 192.168.6.0/24 dev R2-eth2 scope link table 3")
    R2.cmd("ip route add default via 192.168.6.2 dev R2-eth2 table 3")
    R2.cmd("ip route add default scope global nexthop via 192.168.2.2 dev R2-eth0")

    #Routing table R3
    R3.cmd("ip rule add from 192.168.3.2 table 1")
    R3.cmd("ip rule add from 192.168.5.2 table 2")
    R3.cmd("ip rule add from 192.168.8.2 table 3")
    R3.cmd("ip route add 192.168.3.0/24 dev R3-eth0 scope link table 1")
    R3.cmd("ip route add default via 192.168.3.1 dev R3-eth0 table 1")
    R3.cmd("ip route add 192.168.5.0/24 dev R3-eth1 scope link table 2")
    R3.cmd("ip route add default via 192.168.5.1 dev R3-eth1 table 2")
    R3.cmd("ip route add 192.168.8.0/24 dev R3-eth2 scope link table 3")
    R3.cmd("ip route add default via 192.168.8.1 dev R3-eth2 table 3")
    R3.cmd("ip route add default scope global nexthop via 192.168.3.1 dev R3-eth0")

    #Routing table R4
    R4.cmd("ip rule add from 192.168.4.2 table 1")
    R4.cmd("ip rule add from 192.168.7.2 table 2")
    R4.cmd("ip rule add from 192.168.6.2 table 3")
    R4.cmd("ip route add 192.168.4.0/24 dev R4-eth0 scope link table 1")
    R4.cmd("ip route add default via 192.168.4.1 dev R4-eth0 table 1")
    R4.cmd("ip route add 192.168.7.0/24 dev R4-eth1 scope link table 2")
    R4.cmd("ip route add default via 192.168.7.1 dev R4-eth1 table 2")
    R4.cmd("ip route add 192.168.6.0/24 dev R4-eth2 scope link table 3")
    R4.cmd("ip route add default via 192.168.6.1 dev R4-eth2 table 3")
    R4.cmd("ip route add default scope global nexthop via 192.168.4.1 dev R4-eth0")

    #Routing statis
    R1.cmd("route add -net 192.168.3.0/24 gw 192.168.5.2")
    R1.cmd("route add -net 192.168.4.0/24 gw 192.168.7.2")
    R1.cmd("route add -net 192.168.6.0/24 gw 192.168.7.2")
    R1.cmd("route add -net 192.168.8.0/24 gw 192.168.5.2")
    
    R2.cmd("route add -net 192.168.3.0/24 gw 192.168.8.2")
    R2.cmd("route add -net 192.168.4.0/24 gw 192.168.6.2")
    R2.cmd("route add -net 192.168.5.0/24 gw 192.168.8.2")
    R2.cmd("route add -net 192.168.7.0/24 gw 192.168.6.2")
    
    R3.cmd("route add -net 192.168.1.0/24 gw 192.168.5.1")
    R3.cmd("route add -net 192.168.2.0/24 gw 192.168.8.1")
    R3.cmd("route add -net 192.168.6.0/24 gw 192.168.8.1")
    R3.cmd("route add -net 192.168.7.0/24 gw 192.168.5.1")
    
    R4.cmd("route add -net 192.168.1.0/24 gw 192.168.7.1")
    R4.cmd("route add -net 192.168.2.0/24 gw 192.168.6.1")
    R4.cmd("route add -net 192.168.5.0/24 gw 192.168.7.1")
    R4.cmd("route add -net 192.168.8.0/24 gw 192.168.6.1")

    R1.cmdPrint("tc qdisc del dev R1-eth0 root")
    R1.cmdPrint("tc qdisc add dev R1-eth0 root netem delay 20ms")
    
    R2.cmdPrint("tc qdisc del dev R2-eth1 root")
    R2.cmdPrint("tc qdisc add dev R2-eth1 root netem loss 40ms")
	
    R3.cmdPrint("tc qdisc del dev R3-eth0 root")
    R3.cmdPrint("tc qdisc add dev R3-eth0 root netem delay 40ms")
	
    #R1.cmdPrint("tc qdisc del dev R1-eth0 root")
    #R1.cmdPrint("tc qdisc add dev R1-eth0 root netem delay 40ms")

    #R1.cmdPrint("tc qdisc del dev R1-eth0 root")
    #R1.cmdPrint("tc qdisc add dev R1-eth0 root netem delay 60ms")

    #R1.cmdPrint("tc qdisc del dev R1-eth0 root")
    #R1.cmdPrint("tc qdisc add dev R1-eth0 root netem delay 100ms")

    time.sleep(2)

    CLI(net)

    net.stop()
