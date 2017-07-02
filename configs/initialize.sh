#!/bin/bash
apt-get update
apt-get install -y tar git curl wget dialog net-tools build-essential vim
apt-get install -y nginx
apt-get install -y build-essential python python-dev
apt-get install -y python3-setuptools
apt-get install -y python3-venv
apt-get install -y virtualenv
apt-get install -y uwsgi uwsgi-plugin-python3 nginx-full python-setuptools python-pip


git clone https://MosesSymeonidis:%40Moses2113@github.com/nekkon/agenda_back.git
cp agenda_back/configs/nginx.conf /etc/nginx/conf.d/
export LC_ALL="en_US.UTF-8"
locale-gen en_US en_US.UTF-8
pip install virtualenv

python3 -m venv venv
source venv/bin/activate
pip3 install -r agenda_back/requirements.txt


mkdir -p /var/log/uwsgi
mkdir /var/www/agenda_back/
mkdir /etc/uwsgi
mkdir /etc/uwsgi/vassals
cp agenda_back/configs/uwsgi.ini /etc/uwsgi/vassals
cp agenda_back/configs/uwsgi.conf /etc/init/

chown -R www-data:www-data agenda_back/
chown -R www-data:www-data /var/log/uwsgi/

#uwsgi --ini agenda_back/configs/uwsgi.ini
rm /etc/nginx/sites-enabled/default
start uwsgi
/etc/init.d/nginx restart
