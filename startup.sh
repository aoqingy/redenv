#!/bin/bash

# start up supervisord, all daemons should launched by supervisord.
/usr/bin/supervisord -c /etc/supervisor.conf -l /var/log/supervisor.log -j /run/supervisor.pid

# start a shell
/bin/bash
