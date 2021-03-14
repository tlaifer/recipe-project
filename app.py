from flask import Flask
import pgconnection
import mongoconnection

app = Flask(__name__)

sample_mongodb_doc = mongoconnection.return_one()
sample_pg = pgconnection.return_pg()

@app.route('/')
def hello():
    return str(sample_mongodb_doc) + "\n" + str(sample_pg)

if __name__ == '__main__':
    app.run(host='0.0.0.0')