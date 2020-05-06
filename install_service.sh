#!/bin/sh

SERVICE=display-log-server
cp ${SERVICE}.service /lib/systemd/system/
systemctl start ${SERVICE}
systemctl status ${SERVICE}
systemctl enable ${SERVICE}
