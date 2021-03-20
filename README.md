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

## Helpful Links
- restful API with flask-restful https://blog.miguelgrinberg.com/post/designing-a-restful-api-using-flask-restful
- flask & react app - https://towardsdatascience.com/build-deploy-a-react-flask-app-47a89a5d17d9