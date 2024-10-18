#!/bin/bash
# Renewal script to renew TLS certificates

CERT_DIR="/etc/ssl/certs/tls"
KEY_DIR="/etc/ssl/private/tls"
RENEWAL_COMMAND="certbot renew --cert-path $CERT_DIR --key-path $KEY_DIR"

echo "Starting certificate renewal..."
$RENEWAL_COMMAND

if [ $? -eq 0 ]; then
    echo "Certificate renewal completed successfully."
else
    echo "Certificate renewal failed."
fi
