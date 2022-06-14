#Zaky Mahfudz Pasha
#1301194315
#IF-44-02

#!/usr/bin/python
#!/usr/bin/env python
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import Link, TCLink,Intf
from subprocess import Popen, PIPE
from mininet.log import setLogLevel

if '__main__' == __name__:
	setLogLevel('info')
	net = Mininet(link=TCLink)
	key="net.mptcp.mptcp_enable"
	value=0
	p = Popen("sysctl -w %s=%s" % (key, value), shell=True, stdout=PIPE, stderr=PIPE)
	stdout, stderr= p.communicate()
	print("stdout=",stdout,"stderr=",stderr)
	
	#buat host dan router	
	h1=net.addHost('h1')
	h2=net.addHost('h2')
	r1=net.addHost('r1')
	r2=net.addHost('r2')
	r3=net.addHost('r3')
	r4=net.addHost('r4')
	
	#atur bandwidth
	bw1mbps={'bw':1}
	bw500={'bw':0.5}

	#hubungkan
	net.addLink(r1,h1,intfName1='r1-eth0',intfName2='h1-eth0',cls=TCLink, max_queue_size=100,use_tbf=True,**bw1mbps)
	net.addLink(r1,r3,intfName1='r1-eth1',intfName2='r3-eth0',cls=TCLink, max_queue_size=100,use_tbf=True,**bw500)
	net.addLink(r1,r4,intfName1='r1-eth2',intfName2='r4-eth2',cls=TCLink, max_queue_size=100,use_tbf=True,**bw1mbps)
	
	net.addLink(r2,h1,intfName1='r2-eth0',intfName2='h1-eth1',cls=TCLink, max_queue_size=100,use_tbf=True,**bw1mbps)
	net.addLink(r2,r4,intfName1='r2-eth1',intfName2='r4-eth0',cls=TCLink, max_queue_size=100,use_tbf=True,**bw500)
	net.addLink(r2,r3,intfName1='r2-eth2',intfName2='r3-eth2',cls=TCLink, max_queue_size=100,use_tbf=True,**bw1mbps)
	
	net.addLink(r3,h2,intfName1='r3-eth1',intfName2='h2-eth1',cls=TCLink, max_queue_size=100,use_tbf=True,**bw1mbps)
	net.addLink(r4,h2,intfName1='r4-eth1',intfName2='h2-eth0',cls=TCLink, max_queue_size=100,use_tbf=True,**bw1mbps)
	
	net.build()
	
	h1.cmd("ifconfig h1-eth0 0")
	h1.cmd("ifconfig h1-eth1 0")
	
	h2.cmd("ifconfig h2-eth0 0")
	h2.cmd("ifconfig h2-eth1 0")
	
	r1.cmd("ifconfig r1-eth0 0")
	r1.cmd("ifconfig r1-eth1 0")
	r1.cmd("ifconfig r1-eth2 0")
	
	r2.cmd("ifconfig r2-eth0 0")
	r2.cmd("ifconfig r2-eth1 0")
	r2.cmd("ifconfig r2-eth2 0")
	
	r3.cmd("ifconfig r3-eth0 0")
	r3.cmd("ifconfig r3-eth1 0")
	r3.cmd("ifconfig r3-eth2 0")
	
	r4.cmd("ifconfig r4-eth0 0")
	r4.cmd("ifconfig r4-eth1 0")
	r4.cmd("ifconfig r4-eth2 0")
	
	r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	r2.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	r3.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	r4.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	
	h1.cmd("ifconfig h1-eth0 10.0.40.1 netmask 255.255.255.0")
	h1.cmd("ifconfig h1-eth1 10.0.41.1 netmask 255.255.255.0")
	
	h2.cmd("ifconfig h2-eth1 10.0.43.1 netmask 255.255.255.0")
	h2.cmd("ifconfig h2-eth0 10.0.47.1 netmask 255.255.255.0")	
	
	r1.cmd("ifconfig r1-eth0 10.0.40.2 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth1 10.0.42.1 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth2 10.0.44.1 netmask 255.255.255.0")
	
	r2.cmd("ifconfig r2-eth0 10.0.41.2 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth1 10.0.46.1 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth2 10.0.45.1 netmask 255.255.255.0")
	
	r3.cmd("ifconfig r3-eth0 10.0.42.2 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth1 10.0.43.2 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth2 10.0.45.2 netmask 255.255.255.0")
	
	r4.cmd("ifconfig r4-eth0 10.0.46.2 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth1 10.0.47.2 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth2 10.0.44.2 netmask 255.255.255.0")
	
	#h1
	h1.cmd("ip rule add from 10.0.40.1 table 1")
	h1.cmd("ip rule add from 10.0.41.1 table 2")
	h1.cmd("ip route add 10.0.40.0/24 dev h1-eth0 scope link table 1")
	h1.cmd("ip route add default via 10.0.40.2 dev h1-eth0 table 1")
	h1.cmd("ip route add 10.0.41.0/24 dev h1-eth1 scope link table 2")
	h1.cmd("ip route add default via 10.0.41.2 dev h1-eth1 table 2")
	h1.cmd("ip route add default scope global nexthop via 10.0.40.2 dev h1-eth0")
	h1.cmd("ip route add default scope global nexthop via 10.0.41.2 dev h1-eth1")
	
	#h2
	h2.cmd("ip rule add from 10.0.43.1 table 1")
	h2.cmd("ip rule add from 10.0.47.1 table 2")
	h2.cmd("ip route add 10.0.43.0/24 dev h2-eth1 scope link table 1")
	h2.cmd("ip route add default via 10.0.43.2 dev h2-eth1 table 1")
	h2.cmd("ip route add 10.0.47.0/24 dev h2-eth0 scope link table 2")
	h2.cmd("ip route add default via 10.0.47.2 dev h2-eth0 table 2")
	h2.cmd("ip route add default scope global nexthop via 10.0.43.2 dev h2-eth1")
	h2.cmd("ip route add default scope global nexthop via 10.0.47.2 dev h2-eth0")
	#.....................
	#r1 routing
	r1.cmd('route add -net 10.0.41.0/24 gw 10.0.42.2')
	r1.cmd('route add -net 10.0.45.0/24 gw 10.0.42.2') 
	r1.cmd('route add -net 10.0.46.0/24 gw 10.0.44.2')
	r1.cmd('route add -net 10.0.43.0/24 gw 10.0.42.2') 
	r1.cmd('route add -net 10.0.47.0/24 gw 10.0.44.2')

	#r2 routing
	r2.cmd('route add -net 10.0.40.0/24 gw 10.0.45.2')
	r2.cmd('route add -net 10.0.42.0/24 gw 10.0.45.2') 
	r2.cmd('route add -net 10.0.44.0/24 gw 10.0.46.2')
	r2.cmd('route add -net 10.0.43.0/24 gw 10.0.45.2') 
	r2.cmd('route add -net 10.0.47.0/24 gw 10.0.46.2')

	#r3 routing
	r3.cmd('route add -net 10.0.44.0/24 gw 10.0.42.1')
	r3.cmd('route add -net 10.0.46.0/24 gw 10.0.45.1') 
	r3.cmd('route add -net 10.0.47.0/24 gw 10.0.45.1')
	r3.cmd('route add -net 10.0.40.0/24 gw 10.0.42.1') 
	r3.cmd('route add -net 10.0.41.0/24 gw 10.0.45.1')

	#r4 routing
	r4.cmd('route add -net 10.0.45.0/24 gw 10.0.46.1')
	r4.cmd('route add -net 10.0.42.0/24 gw 10.0.44.1') 
	r4.cmd('route add -net 10.0.43.0/24 gw 10.0.46.1')
	r4.cmd('route add -net 10.0.41.0/24 gw 10.0.46.1') 
	r4.cmd('route add -net 10.0.40.0/24 gw 10.0.44.1')
	
	CLI(net)
	
	net.stop()