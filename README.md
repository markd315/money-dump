# money dump
digestible financial advice that goes down easy and comes out in one smooth snake of painless profit


### How to run the webapp server
```commandline
anvil-app-server --app FinancialShitApp --google-client-id 993595845237-q5llasdn2l27h6rk1p18rancmpf8gdhm.apps.googleusercontent.com --google-client-secret $GOOGLE_SECRET
```

There is even a cool webapp which can run in a docker container. Be sure to change the origin setting in the Dockerfile if you host it somewhere else.

# Local docker commands to build image
```commandline
#for aws
docker build -f Dockerfile -t 720291373173.dkr.ecr.us-east-1.amazonaws.com/financial-shit-:latest .
docker push 720291373173.dkr.ecr.us-east-1.amazonaws.com/financial-shit-:latest

#for gcp

docker build -f Dockerfile -t gcr.io/precise-machine-249019/financial-shit:latest .
docker push gcr.io/precise-machine-249019/financial-shit:latest

sudo docker pull gcr.io/precise-machine-249019/financial-shit:latest
sudo docker run -p 6061:6061 gcr.io/precise-machine-249019/financial-shit:latest
```


### Cookbook for serving an Anvil app from a public Linux server
If you have a fresh, internet-accessible Linux server running Ubuntu or Rasbian, and an Anvil app ready to serve, the following sequence of commands will set up and serve your app:

With some custom setup because the embedded postgres was not working on my ubuntu 20.04 instances in GCP
```
$ sudo su
\# apt update
\# apt install openjdk-8-jdk python3.7 virtualenv
\# echo 'net.ipv4.ip_unprivileged_port_start=0' > /etc/sysctl.d/50-unprivileged-ports.conf
\# sysctl --system
\# exit
virtualenv -p python3 venv
. venv/bin/activate
source env/bin/activate
git clone this repo
cd into this repo
pip install anvil-app-server
sudo chmod 0700 .anvil-data/db
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql.service
sudo -u postgres createdb my_database
anvil-app-server --app LineupApp --auto-migrate --config-file LineupApp/anvil.yaml
```