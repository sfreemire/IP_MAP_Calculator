# IP_MAP_Calculator

IP Networking MAP-T Addressing Calculator

MAP-T is 'Mapping of Address and Port using Translation.' It is used to conserve IPv4 address inventory by enabling assignment of the same IPv4 address to multiple (MAP-T capable) routers. It is primarily used by Internet service providers (ISPs) for assigning Internet-routable IPv4 addresses to customer gateway routers. One possible MAP-T configuration allows 64 devices to share the same IP address. This sharing ratio allows 16,384 user devices to be connected to the Internet using only 256 unique IPv4 addresses.

IP_MAP_Calculator calculates IPv4 sharing and port allocations for stateless "Mapping of Address and Port" (MAP) rules, as described in RFC7599 (MAP-T) and RFC7597 (MAP-E). It also shows how these values are calculated using the MAP-T rules and assigned address prefixes at the bit level.

## Dependencies

* Python 3.10+. Testing was done on Python 3.11
* tkinter framework python-tk@3.11+
* PySimpleGUI 4.60.4+ Python package

## MAP-T Function and Rules Explanation

The ability to share the same IPv4 address between multiple devices is accomplished by assigning unique sets of IP source port numbers to each device. Using this strategy, a device can be identified using the IPv4 source address and source port number of the packets it sends.

Employing this method requires the use of a Border Relay (BR) router. It acts as a NAT gateway between the internal network where the devices reside, and an external network. For incoming, external packets, it identifies the destination device using the device's IPv4 address and port number. On the internal network, forwarding packets to the correct devices requires an additional step - the "translation" part of MAP-T. Because there is no way to route packets to individual devices that are using duplicate IP addresses within a broadcast domain, all IPv4 traffic sent between the devices and the Border Relay router uses IPv6.

With large numbers of devices, doing 4-in-6 using a stateful method that requires tables to record IP/port/device relationships would create significant memory and compute overhead for the MAP-T BR routers. Alternately, encapsulation of IPv4 traffic into IPv6 brings with it all of the well-known issues with tunneling in general. Translation of IPv4 into IPv6 by embedding the IPv4 addresses directly into IPv6 addresses is stateless, and greatly reduces the additional overhead required. It also enables multiple BR routers to handle traffic for the same MAP-T endpoints without the use of synchronization or failover protocols. For these reasons, MAP-T is increasingly being seen as the protocol of choice when an IPv4 conservation strategy is needed.

MAP-T provides a method for not only translating a device's IPv4 address into IPv6, but also for enabling BR routers to identify the device in a "stateless" manner from its IPv4 address and source port. This allow the BRs to forward incoming, external IPv4 traffic to the correct IPv6 device address.

This is accomplished by:
* Configuring the MAP-T Base Mapping Rule (BMR) on the BR
* Providing all MAP-T devices in the local domain with the BMR (normally via DHCPv6)
* Providing all devices with unique End-user IPv6 prefixes (normally via DHCPv6). These prefixes, together with the BMR, are used by each device to calculate their source IPv4 addresses and available source ports
* Devices embedding their IPv4 source address in their translated IPv6 source addresses, and using source ports from their assigned (calculated) range

## Executables

Executable files are located in the executables folder.
They _might_ only run on the OS or hardware they were built on.

v0.7.0:
* IPMCv0-7-0_macOS_Ventura13-4_M1
* IPMCv0-7-0_macOS_Ventura13-6_Intel

v0.8.0:
Window is scrollable for use on smaller displays.
* IPMCv0-8-0_macOS_Ventura13-4_M1
* IPMCv0-8-0_macOS_Ventura13-6_Intel

## License

IP_MAP_Calculator is released under the "MIT License Agreement".

See LICENSE file for details.
