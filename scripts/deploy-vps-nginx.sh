# Code Journey — VPS nginx + TLS setup for codejourney.shop (incl. www).
# Runs ON the VPS as a sudo-capable user (ubuntu). Idempotent; aborts on any
# failed check. Only ADDS one nginx site; existing sites are not touched.
# Certificate covers BOTH codejourney.shop and www.codejourney.shop;
# www redirects (HTTP+HTTPS) to the apex.
set -euo pipefail

DOMAIN="codejourney.shop"
CONF="/etc/nginx/sites-available/${DOMAIN}"
ENABLED="/etc/nginx/sites-enabled/${DOMAIN}"
SEC_CONF="/etc/nginx/conf.d/codejourney-security.conf"
WEBROOT="/var/www/html"

echo "== 1. HTTP-only server block (for the ACME challenge) =="
sudo mkdir -p "$WEBROOT"
sudo tee "$CONF" > /dev/null <<'NGINX'
server {
    listen 80;
    listen [::]:80;
    server_name codejourney.shop www.codejourney.shop;

    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}
NGINX
echo "== 1b. Shared rate-limit zones (http level) =="
# Zones back limit_req in the site config (see repo:
# deploy/nginx-codejourney-security.conf). Installing at conf.d level keeps
# the zones available to ALL server blocks regardless of include order.
sudo tee "$SEC_CONF" > /dev/null <<'NGINX'
limit_req_zone $binary_remote_addr zone=cj_auth:1m rate=10r/s;
limit_req_zone $binary_remote_addr zone=cj_general:1m rate=30r/s;
NGINX

sudo ln -sf "$CONF" "$ENABLED"
sudo nginx -t
sudo systemctl reload nginx
echo "nginx reloaded (HTTP block active)"

echo "== 2. Issue the Let's Encrypt certificate (nginx plugin) =="
if sudo certbot certificates 2>/dev/null | grep -A8 "Certificate Name: ${DOMAIN}" | grep -q "Domains:.*www.${DOMAIN}"; then
  echo "certificate already covers both names — attempting renew if due"
  sudo certbot renew --cert-name "$DOMAIN" --nginx --non-interactive
elif sudo certbot certificates 2>/dev/null | grep -q "Certificate Name: ${DOMAIN}"; then
  echo "certificate exists for apex only — EXPANDING to include www"
  sudo certbot certonly --nginx -d "$DOMAIN" -d "www.${DOMAIN}" \
    --expand --non-interactive --agree-tos --register-unsafely-without-email
else
  sudo certbot certonly --nginx -d "$DOMAIN" -d "www.${DOMAIN}" \
    --non-interactive --agree-tos --register-unsafely-without-email
fi

echo "== 3. Full HTTPS config (TLS + proxy to 127.0.0.1:3010, www redirect) =="
sudo tee "$CONF" > /dev/null <<'NGINX'
server {
    listen 80;
    listen [::]:80;
    server_name codejourney.shop www.codejourney.shop;

    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    http2 on;
    server_name codejourney.shop;

    client_max_body_size 20M;

    ssl_certificate     /etc/letsencrypt/live/codejourney.shop/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/codejourney.shop/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;

    # Credential-stuffing guard: nginx-level burst limit on the NextAuth
    # credentials callback, before bcrypt CPU is spent. Zones come from
    # /etc/nginx/conf.d/codejourney-security.conf (installed in step 1b).
    location = /api/auth/callback/credentials {
        limit_req zone=cj_auth burst=5 nodelay;
        limit_req_status 429;
        proxy_pass http://127.0.0.1:3010;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header X-Forwarded-Proto https;
    }

    location /_next/static/ {
        # Immutable build assets: exempt from rate limiting (cacheable, no
        # server-side computation per request).
        proxy_pass http://127.0.0.1:3010;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header X-Forwarded-Proto https;
    }

    location / {
        # Site-wide flood brake (zone in conf.d/codejourney-security.conf).
        limit_req zone=cj_general burst=60 nodelay;
        limit_req_status 429;
        proxy_pass http://127.0.0.1:3010;
        proxy_http_version 1.1;
        # SECURITY: OVERWRITE, never append, X-Forwarded-For. The app's rate
        # limiter trusts the FIRST XFF entry; appending would let any client
        # spoof a fresh IP per request and bypass every per-IP limit. Clients
        # connect directly to nginx (no CDN), so $remote_addr IS the client.
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 120s;
    }
}

# www over HTTPS: terminate with the same cert, redirect to the apex.
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    http2 on;
    server_name www.codejourney.shop;

    ssl_certificate     /etc/letsencrypt/live/codejourney.shop/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/codejourney.shop/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    return 301 https://codejourney.shop$request_uri;
}
NGINX
sudo nginx -t
sudo systemctl reload nginx
echo "nginx reloaded (HTTPS active, www redirecting)"

echo "== 4. Verify renewal timer =="
systemctl is-active certbot.timer

echo "DONE — https://codejourney.shop (and www → apex) now serve the app"
