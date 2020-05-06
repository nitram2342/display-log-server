The display-log-server receives text lines via TCP and forwards them via HTTP GET request to the [Magic Mirror syslog](https://github.com/paviro/MMM-syslog) interface on a Raspberry Pi. The text messages are than shown on the [Magic Mirror](https://magicmirror.builders/) display. This service is used as a wrapper to prevent binding Magic Mirror to an exposed network port.

# Installation

Clone the code to your Raspberry Pi and install the service by executing:

> sudo ./install_service.sh


