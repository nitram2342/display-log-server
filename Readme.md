The display-log-server receives text lines via TCP and forwards them via HTTP GET request to the [Magic Mirror syslog](https://github.com/paviro/MMM-syslog) interface on a Raspberry Pi. The text messages are than shown on the [Magic Mirror](https://magicmirror.builders/) display. This service is used as a wrapper to prevent binding Magic Mirror to an exposed network port.

# Installation

Install required python modules:

> apt install python-requests

Clone the code to your Raspberry Pi and install the service by executing:

> sudo ./install_service.sh


# Usage


> echo helium error oh shit something failed | nc 10.0.0.23 9999

The first word refers to a hostname, the second string is either "info", "warning" or "error" and refers to the message type. The rest of the line is the message to log.
