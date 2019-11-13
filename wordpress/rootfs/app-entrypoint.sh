#!/bin/bash -e

echo "waiting for ${MARIADB_HOST}..."

while ! nc -z "${MARIADB_HOST}" "3306"; do
    sleep 0.5
done

. /opt/bitnami/base/functions
. /opt/bitnami/base/helpers

print_welcome_page

if [[ "$1" == "nami" && "$2" == "start" ]] || [[ "$1" == "/init.sh" ]]; then
    . /apache-init.sh
    . /wordpress-init.sh
    nami_initialize apache php mysql-client wordpress
    info "Starting wordpress... "
    . /post-init.sh
fi

exec tini -- "$@"
