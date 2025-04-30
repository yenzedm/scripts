SERVER=<domen>
PORT=443
CERTIFICATE=/etc/gitlab-runner/certs/${SERVER}.crt

# Create the certificates hierarchy expected by gitlab
sudo mkdir -p $(dirname "$CERTIFICATE")

# Get the certificate in PEM format and store it
openssl s_client -connect ${SERVER}:${PORT} -showcerts </dev/null 2>/dev/null | sed -e '/-----BEGIN/,/-----END/!d' | sudo tee "$CERTIFICATE" >/dev/null

# Register your runner
#gitlab-runner register --tls-ca-file="$CERTIFICATE" [your other options]
