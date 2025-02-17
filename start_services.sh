#! /bin/bash
nohup /usr/local/nginx/locations/reload_nginx.sh >> /usr/local/nginx/locations/nginx_reload.log &
service nginx reload
service nginx restart
python3 /opt/spellchecker/manage.py makemigrations
python3 /opt/spellchecker/manage.py migrate

python3 /opt/spellchecker/manage.py runserver 0.0.0.0:8000 >> /opt/spellchecker/$(date +"%F").log