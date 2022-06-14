#Zaky Mahfudz Pasha
#1301194315
#IF-44-02

#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import CPULimitedHost
import time
import os

class MyTopo(Topo):
  def __init__(self, **opts):
     Topo.__init__(self, **opts)
     
     #Membuat objek Host
     H1 = self.addHost('H1')
     H2 = self.addHost('H2')
     
     R1 = self.addHost('R1')
     R2 = self.addHost('R2')
     R3 = self.addHost('R3')
     R4 = self.addHost('R4')
     
     #Setting bandwith(20,40,60)
     MaxSize = 20
     delay = 1
     linkopts0 = dict(bw=0.5, delay='{}ms'.format(delay), loss=0, max_queue_size=MaxSize, use_tbf=True)
     linkopts1 = dict(bw=1, delay='{}ms'.format(delay), loss=0, max_queue_size=MaxSize, use_tbf=True)
     
     #Membuat link router ke router
     self.addLink(R1, R3, cls=TCLink, **linkopts0, intfName1 = 'R1-eth1', intfName2 = 'R3-eth0')
     self.addLink(R1, R4, cls=TCLink, **linkopts1, intfName1 = 'R1-eth2', intfName2 = 'R4-eth2')
     self.addLink(R2, R3, cls=TCLink, **linkopts0, intfName1 = 'R2-eth2', intfName2 = 'R3-eth2')
     self.addLink(R2, R4, cls=TCLink, **linkopts1,  intfName1 = 'R2-eth1', intfName2 = 'R4-eth1')
     
     #Membuat link router ke host
     self.addLink(H1, R1, cls=TCLink, **linkopts0, intfName1 = 'H1-eth0', intfName2 = 'R1-eth0')
     self.addLink(H1, R2, cls=TCLink, **linkopts1, intfName1 = 'H1-eth1', intfName2 = 'R2-eth1')
     self.addLink(H2, R3, cls=TCLink, **linkopts0, intfName1 = 'H2-eth0', intfName2 = 'R2-eth1')
     
     def runTopo():
     
     #Membangun topologi
     topo = MyTopo()
     net = Mininet(topo=topo, host=CPUlimitedHost, link=TCLink)
     net.start():
     
     #Memasukkan objek host pada variabel
     H1,H2,R1,R2,R3,R4 = net.get('H1','H2','R1','R2','R3','R4')

	#Konfigurasi IP
	H1.cmd('ifconfig H1-eth0 0')
	H1.cmd('ifconfig H1-eth1 0')
	H1.cmd('ifconfig H1-eth0 192.40.3.7 netmask 255.255.255.252')
	H1.cmd('ifconfig H1-eth1 192.40.3.11 netmask 255.255.255.252')

	H2.cmd('ifconfig H2-eth0 0')
	H2.cmd('ifconfig H2-eth1 0')
	H2.cmd('ifconfig H2-eth0 192.40.3.24 netmask 255.255.255.252')
	H2.cmd('ifconfig H2-eth1 192.40.3.28 netmask 255.255.255.252')

	R1.cmd('ifconfig R1-eth0 0')
	R1.cmd('ifconfig R1-eth1 0')
	R1.cmd('ifconfig R1-eth2 0')
	R1.cmd('ifconfig R1-eth0 192.40.3.8 netmask 255.255.255.252')
	R1.cmd('ifconfig R1-eth1 192.40.3.15 netmask 255.255.255.252')
	R1.cmd('ifconfig R1-eth2 192.40.3.31 netmask 255.255.255.252') 

	R2.cmd('ifconfig R1-eth0 0')
	R2.cmd('ifconfig R1-eth1 0')
	R2.cmd('ifconfig R1-eth2 0')
	R2.cmd('ifconfig R1-eth0 192.40.3.12 netmask 255.255.255.252')
	R2.cmd('ifconfig R1-eth1 192.40.3.19 netmask 255.255.255.252')
	R2.cmd('ifconfig R1-eth2 192.40.3.35 netmask 255.255.255.252')
  
	R3.cmd('ifconfig R1-eth0 0')
	R3.cmd('ifconfig R1-eth1 0')
	R3.cmd('ifconfig R1-eth2 0')
	R3.cmd('ifconfig R1-eth0 192.40.3.13 netmask 255.255.255.252')
	R3.cmd('ifconfig R1-eth1 192.40.3.16 netmask 255.255.255.252')
	R3.cmd('ifconfig R1-eth2 192.40.3.36 netmask 255.255.255.252')

	R4.cmd('ifconfig R4-eth0 0')
	R4.cmd('ifconfig R4-eth1 0')
	R4.cmd('ifconfig R4-eth2 0')
	R4.cmd('ifconfig R4-eth0 192.40.3.27 netmask 255.255.255.252')
	R4.cmd('ifconfig R4-eth1 192.40.3.20 netmask 255.255.255.252')
	R4.cmd('ifconfig R4-eth2 192.40.3.32 netmask 255.255.255.252')


	#enabling ip forward for all router
	R1.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
	R2.cmd('echo 2 > /proc/sys/net/ipv4/ip_forward')
	R3.cmd('echo 3 > /proc/sys/net/ipv4/ip_forward')
	R4.cmd('echo 4 > /proc/sys/net/ipv4/ip_forward')
	
if __name__ == '__main__':
	run()
	setLogLevel('info')

topos = { 'mytopo': ( lambda: MyTopo() ) }
	
	
	
