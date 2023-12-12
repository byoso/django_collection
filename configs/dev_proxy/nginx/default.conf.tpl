server {
    listen 80;

    server_name ${DOMAIN} www.${DOMAIN};

    location /static {
        alias /vol/static/static;
    }

    location /cdn {
        alias /vol/static/media/cdn;
    }

    location /site {
        alias /vol/static/media/sitefiles;
    }

    location / {
        uwsgi_pass                  ${APP_HOST}:${APP_PORT};
        include                     /etc/nginx/uwsgi_params;
        client_max_body_size        ${MAX_UPLOAD_SIZE}M;
    }
}
