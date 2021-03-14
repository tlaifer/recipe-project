from flask import Flask
import pgconnection
import mongoconnection

app = Flask(__name__)

sample_mongodb_doc = mongoconnection.return_one()

@app.route('/')
def hello():
    return str(sample_mongodb_doc)

if __name__ == '__main__':
    app.run(host='0.0.0.0')