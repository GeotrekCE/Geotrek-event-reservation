#!/usr/bin/env bash

set -e

# Activate venv
. /opt/venv/bin/activate

# Defaults POSTGRES_HOST to Docker host IP
export GEOTREK_DB_HOST=${GEOTREK_DB_HOST:-`ip route | grep default | sed 's/.* \([0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+\) .*/\1/'`}

cd /opt/png-resa

# Execute COMMAND argument or CMD instruction
exec $@
