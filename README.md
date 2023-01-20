# financial shit
A fantasy baseball mode with real lineups and bullpen configurations that replays plate appearances from the week in random order to synthesize results.


### How to run the webapp server
```commandline
anvil-app-server --app FinancialShitApp
```

There is even a cool webapp which can run in a docker container. Be sure to change the origin setting in the Dockerfile if you host it somewhere else.

# Local docker commands to build image
```commandline
docker build -f Dockerfile.dev -t 720291373173.dkr.ecr.us-east-1.amazonaws.com/financial-shit-dev:latest .
docker push 720291373173.dkr.ecr.us-east-1.amazonaws.com/financial-shit-dev:latest

docker build -t 720291373173.dkr.ecr.us-east-1.amazonaws.com/financial-shit:latest .
docker push 720291373173.dkr.ecr.us-east-1.amazonaws.com/financial-shit:latest
```

# Docker commands for admin
Saves containerid for anything below.
```commandline

Note: not working yet in set-eid.sh
sudo su -
cd /home/ec2-user

eid=$(docker ps --filter name=financial-shit-dev | tail -n 1 | awk '{print $1;}')
eid=$(docker ps --filter name=financial-shit-prod | tail -n 1 | awk '{print $1;}')
```

Takes a backup to the vm
```commandline
docker cp $eid:/apps/leagues /home/ec2-user/backups/leagues_backup$(date +'%d-%m-%Y-%H-%M')
```

Restores a backup
```commandline
docker exec -it $eid rm -rf /apps/leagues
sudo cp /home/ec2-user/backups/leagues_backup04-09-2022-04-52 /home/ec2-user/backups/leagues -r
sudo chown -R root leagues
sudo chmod -R 777 leagues
sudo docker cp /home/ec2-user/backups/leagues/ $eid:/apps
```

Updates the league week prior to an execution
```bash
sudo docker cp $eid:/apps/config.py config.py
sudo cp config.py config.py.backup
sudo echo 'leagueWeek = 0'> config.py
sudo cat config.py.backup |tail -n+2>> config.py
sudo docker cp config.py $eid:/apps/config.py
```

Runs the league week, publishing results logs etc
```commandline
sudo docker exec -it $eid python simulateLeagueWeek.py
```

To lock in rosters (normally a week will already do this)
```commandline
sudo docker exec -it $eid python commitNewRosters.py
```

For any further debugging
```commandline
sudo docker exec -it $eid /bin/sh
```


### some math on handedness

Handedness advantage with pitchers and batters. We want to keep the principle of rolling to determine the outcome in place while favoring R/L and L/R batters.
Needs a factor proportional to number of teams for this too. 30 teams would nullify the handedness advantage since avg pitcher and batter would be same as league avg,
but less (8 for example) means the best 25% of lineups are competing day to day. Instead of .708 league avg OPS, we can look at how the top .25 of that pool would do.

There are more righty PA's (3500) than lefty PA's in any given year, so it makes sense that we need to punish LHB vs LHP more than RHB vs RHP to arrive at the right numbers (see data this intuition was right)
https://www.fangraphs.com/leaders/splits-leaderboards?splitArr=1,3&splitArrPitch=&position=B&autoPt=false&splitTeams=false&statType=mlb&statgroup=2&startDate=2022-3-1&endDate=2022-11-1&players=&filter=&groupBy=season&wxTemperature=&wxPressure=&wxAirDensity=&wxElevation=&wxWindSpeed=&sort=10,1&pg=0

example. in a 8 team league, having "your" outcome selected instead of the typical pitchers outcome confers a 15% advantage. Double that for the advantage against a "fantasy pitcher"s outcome (30%)
We can manipulate the odds of the coin flip based on handedness, and arrive at the right OPS for the matchup through some algebra.

solve the equations
x+y=1, .815x+.601y=.739 for example (8 team, LHP vs RHB)

Luckily, all of the 4 platoon splits seem to be almost within the bounds of what we can construct by manipulating these coin tosses a little bit. Even the 16 team league gives us a range of .772 to .644 which we can just use .644 for.

Full league
            HL          HR
   PL      .643        .739
   PR      .709        .703
   OVR(batter - pitcher)     .708

in the table the solved results are (batter coin %) rest is pitcher coin %

16 team league
            HL               HR
   PL     .737(0.0)          .849(.742)
   PR     .796(.508)          .776(.461)
   OVR(+18%) .772-.644


8 team league
             HL           HR
   PL       .788(.196)         .928(.644)
   PR       .861(.505)          .818(.476)
   OVR(+30%) .815-.601

4 team league
             HL           HR
   PL       .837(.274)         .982(.607)
   PR       .918(.503)         .851(.483)
   OVR(+40%) .852-.564


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

don't think this part is needed anymore
```commandline
sudo -u postgres createuser --interactive
alice
sudo -u postgres createdb alice
```