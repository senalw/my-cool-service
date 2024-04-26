#!/bin/bash

set -e  # Exit immediately if a command fails

generate_certificates() {
    local dir="$1"

    # Create directory for certificates
    mkdir -p "../certs/$dir"
    echo "Created certs/$dir directory"

    # Generate certificates
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout "../certs/$dir/private.key" \
        -out "../certs/$dir/public.crt" \
        -subj "/CN=localhost" \
        -addext "subjectAltName = DNS:localhost"

    echo "Generated $dir certificates"
}

generate_certificates "opa" # generate certificates for OPA
generate_certificates "service" # generate certificates for service
