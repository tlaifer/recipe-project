# UIUC CS-411 recipe-project

## Setup requirements:
### Install postgres.
Depending on the platform setup requirements differ. The UIUC VM is running Linux Red Hat (Cent OS), which you can find with
```bash
cat /etc/os-release
```
Link [here](https://www.postgresql.org/download/linux/redhat/)

### Install mongo-db.
Similar as above. Download [here](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-red-hat/)

### Install flask & python db dependencies.
1. [Flask](https://pypi.org/project/Flask/)
2. [psycopg](https://www.psycopg.org/install/)
3. [PyMongo](https://pymongo.readthedocs.io/en/stable/installation.html)

Add these to the requirements along the way with:
```
python3 -m pip freeze > requirements.txt
```

Now, just run
```
pip3 install -r requirements.txt
```

### Install NodeJs
https://tecadmin.net/install-latest-nodejs-and-npm-on-centos/
1. Enable node.js yum repository
```bash
yum install -y gcc-c++ make
curl -sL https://rpm.nodesource.com/setup_14.x | sudo -E bash -
```
2. Install node.js
```
sudo yum install nodejs
```

3. `cd` into the recipe-project/frontend folder and install npm requirements
```
npm install
```

## Troubleshooting

### MongoDB
- check status of mongo db
```bash
sudo systemctl status mongod
```
- restart mongo
```bash
sudo systemctl stop mongod
sudo systemctl start mongod
```
- if you can't figure out why mongo won't start try rebooting. the system:
```bash
sudo reboot
```

### Out of disk space? 
It's posible the VM runs out of space in certain directories. For example when trying to install node.js I saw:
```bash
Insufficient space in download directory /var/cache/yum/x86_64/7/centos-7-updates
    * free   768 k
    * needed 6.5 M
```

Investigating this I noticed the /var/spool directory was eating up memory
```bash
[tlaifer2@sp21-cs411-13 /]$ sudo du -h /var/* | sort -rh | head -10
3.2G    /var/spool/abrt/ccpp-2021-03-14-16:00:52-32698
3.2G    /var/spool/abrt
3.2G    /var/spool
518M    /var/lib
302M    /var/lib/mongo
300M    /var/lib/mongo/journal
286M    /var/cache
284M    /var/cache/yum/x86_64/7
284M    /var/cache/yum/x86_64
284M    /var/cache/yum
```

We can delete this with:
```bash
[tlaifer2@sp21-cs411-13 /]$ sudo abrt-cli rm /var/spool/abrt/ccpp-2021-03-14-16:00:52-32698
rm '/var/spool/abrt/ccpp-2021-03-14-16:00:52-32698'
```

## Helpful Links
- restful API with flask-restful https://blog.miguelgrinberg.com/post/designing-a-restful-api-using-flask-restful
- flask & react app - https://towardsdatascience.com/build-deploy-a-react-flask-app-47a89a5d17d9