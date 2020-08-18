15th Aug 2020
==============

Test web-hook 18th Aug 9:15am

Do the following after spinning a new droplet

1. Create a new user (jenkins) 
2. Install Docker / Docker-Compose
3. Create a directory and environment files
4. Download docker images from Docker Hub ($docker-compose build -u)
5. Pull app files from github
6. rename to app file (mv gammatrades-app app)

1. Create a new user (jenkins)
------------------------------

ssh root@XXX
adduser jenkins
usermod -aG sudo jenkins
su - jenkins
cd /home/jenkins
mkdir .ssh
cd .ssh
cp -r /root/.ssh/authorized_keys /home/jenkins
chown 1000:1000 authorized_keys

sudo groupadd docker
sudo usermod -aG docker jenkins
(logout and login)

2. Install Docker / Docker-Compose
------------------------------------

After successful login into a brand new DO droplet (ssh jenkins@XXX).. run the following


apt-get update
apt-get upgrade

curl -fsSL get.docker.com -o get-docker.sh
sudo sh get-docker.sh

sudo curl -L "https://github.com/docker/compose/releases/download/1.23.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose
sudo cp /usr/share/zoneinfo/Asia/Singapore /etc/localtime

docker -v
docker-compose -v


3. Create a directory and environment files

 3.1 docker-compose.yml (see below)
 3.2  jenkins_home (empty) 
 3.3 postgres-data (empty)  
 3.4 ssh-keys (create ssh keys with ssh-keygen command)
 3.5 docker-volumes/etc/letsencrypt (see lets encrypt documents)

##################################################################
version: '3.7'
services:
  jenkins:
    container_name: jenkins_docker
    image: stratmaster/gammatrades-jenkins:1.00
    ports:
      - 8080:8080
      - 22:22
    volumes:
      - ./jenkins_home:/var/jenkins_home
    networks:
      - net
  web:
    container_name: web_docker
    image: stratmaster/gammatrades-app:1.01
    networks:
      - net
    ports:
      - 22:22
    volumes:
      - ./app:/usr/src/app
      - ./ssh-keys/remote-key.pub:/home/remote_user/.ssh/authorized_keys
    depends_on:
      - db
    command: gunicorn try_django.wsgi:application --bind 0.0.0.0:8000
  db:
    container_name: db_docker
    image: postgres:12.0-alpine
    networks:
      - net
    ports:
      - 5432:5432
    tty: true
    environment:
      POSTGRES_PASSWORD: password1234
    volumes:
      - ./postgres-data:/var/lib/postgresql/data
  nginx:
    container_name: nginx_docker
    image: stratmaster/gammatrades-nginx
    ports:
      - 80:80
      - 443:443
    volumes:
      - /docker-volumes/etc/letsencrypt/live/gammatrades.com/dhparam-2048.pem:/etc/ssl/certs/dhparam-2048.pem
      - /docker-volumes/etc/letsencrypt/live/gammatrades.com/fullchain.pem:/etc/letsencrypt/live/gammatrades.com/fullchain.pem
      - /docker-volumes/etc/letsencrypt/live/gammatrades.com/privkey.pem:/etc/letsencrypt/live/gammatrades.com/privkey.pem
      - ./app/nginx/nginx.conf:/etc/nginx/conf.d/nginx.conf
    networks:
      - net
    depends_on:
      - web

networks:
  net:

########################################################################################################################################

4. Clone App files from GitHub
------------------------------

git clone https://github.com/<name>


1. create .env file
2. change the white-list for domain-name at settings
3. change the domain name at java-script inside js directory

docker-compose up -d --build

Create database with following:

docker exec -it db_docker /bin/bash
psql -h localhost -p 5432 -U postgres
CREATE DATABASE btre_prod;
CREATE USER dbadmin WITH PASSWORD 'Romans12:1';
ALTER ROLE dbadmin SET client_encoding TO 'utf8';
ALTER ROLE dbadmin SET default_transaction_isolation TO 'read committed';
ALTER ROLE dbadmin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE btre_prod TO dbadmin;
\q


docker exec -it web_docker /bin/bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic
python3 manage.py createsuperuser
