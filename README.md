
# Askme service

### Centrifugo (app/centrifugo)
```
.centrifugo --config=confug.json
```

### Настройки nginx
```
upstream askme {
    server 127.0.0.1:8000;
}

server {
    listen 80 default_server;
    server_name askme.com;

    access_log /var/log/nginx/askme.access.log;
    error_log /var/log/nginx/askme.error.log;

    location / {
        proxy_pass http://askme;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_cache mycache;
        proxy_cache_valid 200 302 10m;
        proxy_cache_valid 404      1m;
    }

    location ^~ /upload/ {
        root /home/user/projects/vk/web_task1/;
        add_header Cache-Control "public, max-age=2592000";
        gzip on;
    }

    location ^~ /static/ {
        root /home/user/projects/vk/web_task1/;
        add_header Cache-Control "public, max-age=2592000";
        gzip on;
    }

    location ~* \.(js|css|png|jpg)$ {
        root /home/user/projects/vk/web_task1/static/;
        add_header Cache-Control "public, max-age=2592000";
        gzip on;
    }
}
```

### Настройки cron
```
* * * * * cd /home/user/projects/vk/web_task1 && source venv/bin/activate && python manage.py generate_popular_tags
* * * * * cd /home/user/projects/vk/web_task1 && source venv/bin/activate && python manage.py generate_best_members
```

### Запуск через gunicorn
```
gunicorn askme.wsgi
```
