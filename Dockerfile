FROM ubuntu:22.04

# Install Extras
RUN apt-get update && apt-get install -y curl vim
# Install locales
RUN apt-get install -y unzip wget locales cron lynx

RUN locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8
ENV LANG es_CO.UTF-8

ENV LC_ALL C

# Install python aux libs

RUN apt-get update
RUN apt-get install -y gcc cmake make tar curl
RUN apt-get update
RUN apt-get install -y python3.10 swig3.0
RUN apt-get update
RUN apt-get install -y python3-pip
RUN apt-get update
RUN apt-get install -y unzip wget locales cron lynx

# Install Python dependencies
RUN apt-get update
RUN apt-get install libsasl2-dev
RUN apt-get install libssl-dev
RUN pip install Django==3.2.8
RUN pip install simplejson
RUN pip install pandas
RUN pip install requests
RUN pip install DateTime
RUN pip install django-tinymce
RUN pip install PyMySQL
#RUN pip install mysqlclient
RUN pip install Pillow
RUN pip install jamspell
RUN pip install timeloop
RUN pip install beautifulsoup4
RUN pip install lxml
RUN pip install minio
RUN pip install jproperties
RUN pip install kubernetes
RUN pip install django-environ

# Install inotify-tools
RUN apt-get update && apt-get install -y inotify-tools

# Install Nginx
RUN apt-get update && apt-get install -y nginx

COPY nginx_conf/locations/locations /usr/local/nginx/locations/
COPY nginx_conf/locations/reload_nginx.sh /usr/local/nginx/locations/
COPY nginx_conf/default /etc/nginx/sites-available/
COPY spellchecker /opt/spellchecker/
COPY start_services.sh /home/

RUN ["chmod", "+x", "/usr/local/nginx/locations/reload_nginx.sh"]
RUN ["chmod", "+x", "/home/start_services.sh"]
RUN ["python3", "/opt/spellchecker/manage.py", "collectstatic", "--noinput"]

CMD ["/home/start_services.sh"]

