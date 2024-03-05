# IP_MAP_Calculator

IP Networking MAP-T Addressing Calculator

MAP-T, the 'Mapping of Address and Port using Translation,' is a stateless NAT64 solution that enables sharing of IPv4 addresses between multiple end user gateway devices. It is primarily used by Internet service providers (ISPs) to reduce the number of Internet-routable IPv4 addresses used when configuring a group of customer gateway routers. For example, one MAP-T configuration allows 64 devices to share the same IP address. This sharing ratio allows 16,384 customer gateways to be connected to the Internet using only 256 unique IPv4 addresses.

IP_MAP_Calculator calculates IPv4 address sharing and port allocations for "Mapping of Address and Port" (MAP) rules, as described in RFC7599 (MAP-T) and RFC7597 (MAP-E). It also displays binary translations, to show how these values are calculated using MAP-T rules and the assigned IPv6 address prefixes at the bit level.

## Dependencies

* Python 3.10+. Testing was done on Python 3.11
* tkinter framework python-tk@3.11+
* PySimpleGUI 4.60.4+ Python package

## MAP-T Function and Rules Explanation

The ability to share the same IPv4 address between multiple devices is accomplished by allocating unique sets of IP source port numbers to each device sharing a particular IPv4 address. Using this strategy, a device can be identified using its source address and port number. The allocation of ports is part of the MAP-T algorithms, and only requires that each device be assigned a unique, MAP-T IPv6 prefix as part of their configuration. Once configured, MAP-T devices begin translating their outbound IPv4 packets into IPv6 packets. The source ports used are taken from their unique allocation of IP port numbers. Translated packets are forwarded to a MAP-T Border Relay (BR) router, which acts as a NAT64 gateway to external networks.

Having large numbers of devices doing 4-in-6 encapsulation, which is stateful and requires tables to record IP/port/device relationships, would create significant memory and compute overhead for MAP-T BR routers. Additionally, encapsulation of IPv4 traffic into IPv6 brings with it all of the well-known issues with tunneling in general. Translation of IPv4 into IPv6 by embedding IPv4 addresses directly into IPv6 addresses is stateless, and greatly reduces the additional overhead required. It also enables redundant or load-balanced BR routers to handle traffic for the same MAP-T endpoints without the use of synchronization or failover protocols. For these reasons, MAP-T is increasingly being seen as the protocol of choice when an IPv4 conservation strategy is needed.

MAP-T "Rules" enables customer gateways to translate their IPv4 source addresses into unique IPv6 addresses for sending outbound packets across the internal network. It also enables the BRs to re-calculate the same IPv6 addresses for forwarding reply packets to those gateways across the internal network. The ability to calculate the required addresses instead of having to do stateful table lookups greatly reduces the hardware requirements for the BRs. It also allows for the use of redundant and load-balanced BRs, without the need for failover or other state-sharing protocols.

The MAP-T solution is enabled by:
* Configuring the MAP-T Base Mapping Rule (BMR) on the BR
* Providing all devices in the local MAP-T domain with the BMR (normally via DHCPv6)
* Providing all devices with unique End-user IPv6 prefixes (normally via DHCPv6). This prefix, together with the BMR, are used by each device to calculate their source IPv4 address and allocation of source ports
* Adding the BMR and BR Gateway IPv6 prefixes to the internal network routing tables.
* Devices calculating their translated IPv6 source addresses, embedded with their shared IPv4 addresses, and using ports from their allocated range
* Devices embedding IPv4 destination addresses in IPv6 destination addresses (BR Default Mapping Rule (DMR) prefixes)
* Devices using a BR as the default route for outbound MAP-T translated traffic

## Native IPv6

Native IPv6 traffic does not participate in MAP-T translation. Any native IPv6 packets transmitted by devices in a MAP-T domain are not modified in any way, and bypass the BR gateways when transiting to external networks.

## Executables

Executable files are located in the executables folder.
They _might_ only run on the OS or hardware they were built on.

v0.7.0:
* IPMCv0-7-0_macOS_Ventura13-4_M1
* IPMCv0-7-0_macOS_Ventura13-6_Intel

v0.8.1:
Window is scrollable for use on smaller displays.
* IPMCv0-8-1_macOS_Ventura13-4_M1
* IPMCv0-8-1_macOS_Ventura13-6_Intel
* IPMCv0-8-1_Win11_Intel

v0-9-1:
Added User IPv6 hex & binary Source Address display field
* IPMCv0-9-1_macOS_Ventura13-4_M1

v0-10-4:
Added active highlighting to Source Address display field
Added "Excluded Ports" number to "Results" display
"Rule String" entry field now automatically strips off comments
* IPMCv0-10-4_macOS_Ventura13-4_M1
* IPMCv0-10-4_macOS_Ventura13-6_Intel

## License

IP_MAP_Calculator is released under the "MIT License Agreement".

See LICENSE file for details.
