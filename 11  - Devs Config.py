Project 11  - Secure Healthcare Information Network - Device Configurations

### ROUTERS ###

## All Routers ##

En
Conf t
Banner motd **UNAUTHORIZED ACCESS IS PUNISHABLE**
Enable password cisco
Line console 0
Password cisco
No ip domain-lookup
Service password-encryption
Ip domain-name cisco.com
Username cisco password cisco
Crypto key generate rsa general-keys modulus 1024
Ip ssh version 2

## WLAN R1 ##

En
Conf t
Hostname WLAN-R1

Int fa1/0
No shut
Ip address 10.30.10.6 255.255.255.252
Exit

Int fa1/1
No shut
Ip address 10.30.10.10 255.255.255.252
Exit

Int fa0/0
No shut
Ip address 10.30.10.2 255.255.255.252
Exit

//OSPF
Router ospf 10
Router id 3.3.3.3
Auto-cost reference-bandwidth 1000000
Network 10.30.10.0 0.0.0.3 area 0
Network 10.30.10.4 0.0.0.3 area 0
Network 10.30.10.8 0.0.0.3 area 0
Exit
Do wr

## VoIP-Router ##

En
Conf t
Hostname VoIP-Router

//Router on a stick is needed to provide IPs to the phones

Int fa0/0
No shut
Int fa0/0.99
Encapsulation dot1q 99
Ip address 172.16.0.1 255.255.240.0
Exit

//DHCP

Ip dhcp pool VoIP
Network 172.16.0.0 255.255.240.0
Default-router 172.16.0.1
Option 150 ip 172.16.0.1
Exit

Telephony-service
Max-dn 20
Max-ephones 20
Auto assign 1 to 20
Ip source-address 172.16.0.1 port 2000
Exit

Ephone-dn 1
Number 3001
Exit

Ephone-dn 2
Number 3002
Exit

Ephone-dn 3
Number 3003
Exit

Ephone-dn 3
Number 3004
Exit

Ephone-dn 3
Number 3005
Exit

Ephone-dn 3
Number 3006
Exit

Ephone-dn 3
Number 3007
Exit

Ephone-dn 3
Number 3008
Exit

Ephone-dn 3
Number 3009
Exit

Ephone-dn 3
Number 3010
Exit

Do wr

## Perimeter-FW ##

En

Conf t
Hostname Perimeter-FW
Domain-name cisco.com

//Security config to WAN-R1
Int gi1/1
No shut
Ip address 10.30.10.1 255.255.255.252
Nameif INSIDE
Security-level 100
Exit

//Security config to DMZ
Int g1/2
No shut
Ip address 10.20.10.1 255.255.255.192
Nameif DMZ
Security-level 70
Exit

//Security config to
Int gi1/3
No shut
Ip address 197.200.100.2 255.255.255.252
Nameif OUTSIDE
Security-level 0
Exit

//OSPF
Router ospf 25
Route-id 4.4.4.4
Auto-cost reference-bandwidth 1000000
Network 10.20.10.0 255.255.255.192 area 0
Network 10.30.10.0 255.255.255.252 area 0
Network 197.200.100.0 255.255.255.252 area 0
Exit

//Route going OUTSIDE interface – permit any ip with any mask should go to ISP-router 197.200.100.1
Route OUTSIDE 0.0.0.0 0.0.0.0 197.200.100.1

// NAT equivalence format: Object network NAME – Subnet to do NAT – NAT ( From IFName, To IFName)

Object network LAN-INTERNET
Subnet 192.168.0.0 255.255.240.0
Nat (INSIDE,OUTSIDE) dynamic interface
Exit
Conf t

Object network WLAN-INTERNET
Subnet 10.10.0.0 255.255.0.0
Nat (INSIDE,OUTSIDE) dynamic interface
Exit
Conf t

Object network DMZ-INTERNET
Subnet 10.20.10.0 255.255.255.192
Nat (DMZ,OUTSIDE) dynamic interface
Exit
Conf t

//FW Policies. Ports: 80: HTTP – 67,68: DHCP - 63: DNS - 53

Access-list INSIDE-DMZ extended permit icmp any any
Access-list INSIDE-DMZ extended permit tcp any any eq 80
Access-list INSIDE-DMZ extended permit udp any any eq 67
Access-list INSIDE-DMZ extended permit udp any any eq 68
Access-list INSIDE-DMZ extended permit udp any any eq 53
Access-list INSIDE-DMZ extended permit tcp any any eq 53
Access-group INSIDE-DMZ in interface DMZ

Access-list INSIDE-OUTSIDE extended permit icmp any any
Access-list INSIDE-OUTSIDE extended permit tcp any any eq 80
Access-group INSIDE-OUTSIDE in interface OUTSIDE

Wr mem

### L3-SWITCHES ###

##All L3-Switches##

En
Conf t
Banner motd **UNAUTHORIZED ACCESS IS PUNISHABLE**
Enable password cisco
Line console 0
Password cisco
No ip domain-lookup
Service password-encryption
Ip domain-name cisco.com
Username cisco password cisco
Crypto key generate rsa general-keys modulus 1024
Ip ssh version 2

Vlan 10
Name LAN
Vlan 50
Name WLAN
Vlan 99
Name Voice
Vlan 100
Name native
Exit

Int ran gi1/0/21-24
No shut
Channel-group 1 mode active
Exit
Int port-channel 1
Switchport mode trunk
Switchport trunk native vlan 100
Exit

Int ran gi1/0/2-8
No shut
Switchport mode trunk
Switchport trun native vlan 100
Exit

## CoreL3-SW1 ##

En
Conf t
Hostname CoreL3-SW13

Int gi1/0/1
No shut
No switchport
Ip address 10.30.10.5 255.255.255.252
Ip routing
Exit

// HSRP Config through SVIs except vlan 99 (voice) which is managed by VoIP-Router. Group standby numbers must match on both sides.

Int vlan 10
ip address 192.168.0.3 255.255.240.0
Ip helper-address 10.20.10.10
Standby 10 priority 150
Standby 10 ip 192.168.0.1
Exit

Int vlan 50
Ip address 10.10.10.3 255.255.0.0
ip helper-address 10.20.10.10
Standby 50 priority 150
Standby 50 ip 10.10.0.1
Exit

//OSPF

Router ospf 10
Auto-cost reference-bandwidth 1000000
Router-id 1.1.1.1
Network 10.30.10.4 0.0.0.3 area 0
Network 10.10.0.0 0.0.255.255 area 0
Network 192.168.0.0 0.0.15.255 area 0
Network 172.16.0.0 0.0.15.255 area 0
Do wr

## CoreL3-SW2 ##

En
Conf t
Hostname CoreL3-SW2

Int gi1/0/1
No shut
No switchport
Ip address 10.30.10.9 255.255.255.252
Ip routing

// HSRP Config through SVIs except vlan 99 (voice) which is managed by VoIP-Router. 
// Group standby numbers must match on both sides.

Int vlan 10
Ip address 192.168.0.2 255.255.240.0
Ip helper-address 10.20.10.10
Standby 10 priority 100
Standby 10 192.168.0.1
Exit

Int vlan 50
Ip address 10.10.0.2 255.255.0.0
Ip helper-address 10.20.10.10
Standby 50 priority 100
Standby 50 ip 10.10.0.1
Exit

Int vlan 99
Ip address 172.16.0.2 255.255.240.0
Ip helper-address 10.20.10.10
Standby 99 priority 100
Standby 99 ip 172.16.0.1
Exit
Do wr

// OSPF

Router ospf 10
Auto-cost reference-bandwidth 1000000
Router-id 2.2.2.2
Network 10.30.10.8 0.0.0.3 area 0
Network 10.10.0.0 0.0.255.255 area 0
Network 192.168.0.0 0.0.15.255 area 0
Network 172.16.0.0 0.0.15.255 area 0
Exit
Do wr

## Airtel-ISP ##

En
Conf t
Hostname Airtel-ISP

Int gi0/0/0
No shut
Ip address 197.200.100.1 255.255.255.252
Exit

Int gi0/0/1
No shut
Ip address 20.20.20.2 255.255.255.252
Exit

//OSPF

Router ospf 10
Router-id 5.5.5.5
Auto-cost reference-bandwidth 1000000
Network 20.20.20.0 0.0.0.3 area 0
Network 197.200.100.0 0.0.0.3 area 0
Exit
Do wr

## AWS-Cloud ##

En
Conf t
Hostname AWS-Cloud

Int gi0/0/0
No shut
Ip address 20.20.20.1 255.255.255.252
Exit

Int gi0/0/1
No shut
Ip address 30.0.0.1 255.0.0.0
Exit

//OSPF

Router ospf 10
Router-id 6.6.6.6
Auto-cost reference-bandwidth 1000000
Network 30.0.0.0 0.255.255.255 area 0
Network 20.20.20.0 0.0.0.3 area 0
Exit

Do wr

### SWITCHES ###

## All Switches – except DMZ and WLC-SW ##

En
Conf t
Banner motd **UNAUTHORIZED ACCESS IS PUNISHABLE**
Enable password cisco
Line console 0
Password cisco
No ip domain-lookup
Service password-encryption
Ip domain-name cisco.com
Username cisco password cisco
Crypto key generate rsa general-keys modulus 1024
Ip ssh version 2

Vlan 10
Name LAN
Vlan 50
Name WLAN
Vlan 99
Name Voice
Vlan 100
Name Native
Exit

Int ran gi0/1-2
No shut
Switchport mode trunk
Switchport trunk native vlan 100
Exit

Int ran fa0/1-20
Switchport mode access
Switchport access vlan 10
Switchport voice vlan 99
Exit

Int ran fa0/21-24
Switchport mode access
Switchport access vlan 50
Exit

Int ran fa0/1-24
Spanning-tree portfast
Spanning-tree bpduguard enable
Exit

Do wr

## Pharm&Med-SW ##

En
Conf t
Hostname Pharm&Med-SW

## Rec&Guest-SW ##

En
Conf t
Hostname Rec&Host-SW

## Doc&Cons-SW ##

En
Conf t
Hostname Doc&Cons-SW

## PR-HR-FIN-SW ##

En
Conf t
Hostname PH-HR-FIN-SW

## IA&Corp-SW ##

En
Conf t
Hostname IA&Corp-SW

## IT-SW ##

En
Conf t
Hostname IT-SW

## WLC-SW ##

En
Conf t
Hostname WLC-SW

En
Conf t
Banner motd **UNAUTHORIZED ACCESS IS PUNISHABLE**
Enable password cisco
Line console 0
Password cisco
No ip domain-lookup
Service password-encryption
Ip domain-name cisco.com
Username cisco password cisco
Crypto key generate rsa general-keys modulus 1024
Ip ssh version 2

Vlan 10
Name LAN
Vlan 50
Name WLAN
Vlan 99
Name Voice
Vlan 100
Name Native
Exit

//VoIP-Router in Fa0/1 must be trunk to give Ips to phones

Int fa0/1
No shut
Switchport mode trunk
Switchport trunk native vlan 100
Exit

Int ran gi0/1-2
No shut
Switchport mode trunk
Switchport trunk native vlan 100
Exit

Int ran fa0/2-20
No shut
Switchport mode access
Switchport access vlan 10
Switchport voice vlan 99
Exit

Int ran fa0/21-24
No shut
Switchport mode access
Switchport access vlan 50
Switchport voice vlan 99
Exit

Int ran fa0/4-24
No shut
Spanning-tree portfast
Spanning-tree bpduguard enable
Exit

## DMZ-SW ##

En
Conf t
Hostname DMZ-SW

En
Conf t
Banner motd **UNAUTHORIZED ACCESS IS PUNISHABLE**
Enable password cisco
Line console 0
Password cisco
No ip domain-lookup
Service password-encryption
Ip domain-name cisco.com
Username cisco password cisco
Crypto key generate rsa general-keys modulus 1024
Ip ssh version 2




