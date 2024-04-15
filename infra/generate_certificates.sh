#!/bin/bash

set -e  # Exit immediately if a command fails

# Create directory for certificates
mkdir -p ../certs/opa
echo "Created certs directory"

# Generate certificates
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout ../certs/opa/private.key \
    -out ../certs/opa/public.crt \
    -subj "/CN=localhost" \
    -addext "subjectAltName = DNS:localhost"

echo "Generated certificates"
