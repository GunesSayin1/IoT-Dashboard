from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
import datetime
import time
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///12312.db'
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)
class IoT(db.Model):
    __table__ = db.Model.metadata.tables['sensors_data']
    def __repr__(self):
        return '<Task %r>' % self.id

def getRecent():
    temperature = IoT.query.filter_by(topic="iot/temperature").order_by(
        IoT.rasptstamp.desc()).first().payload
    humidity = IoT.query.filter_by(topic="iot/humidity").order_by(
        IoT.rasptstamp.desc()).first().payload
    pressure = IoT.query.filter_by(topic="iot/pressure").order_by(
        IoT.rasptstamp.desc()).first().payload
    values = [temperature,humidity,pressure]
    return values


@app.route('/')
def index():
    return render_template('index.html',values=getRecent())
@app.route('/temperature')
def temperature():
    return render_template('temperature.html',value=getRecent(),dial=getRecent()[0])
@app.route('/humidity')
def humidity():
    return render_template('humidity.html',value=getRecent(),dial=getRecent()[1])
@app.route('/pressure')
def pressure():
    return render_template('pressure.html',value=getRecent(),dial=getRecent()[2])

@app.route("/temperature.json")
def temp_data():
    result= IoT.query.filter_by(topic="iot/temperature").order_by(IoT.rasptstamp.asc()).all()
    el = []
    for n in result:
        raw = {}
        raw["x"] = int(time.mktime(datetime.datetime.strptime(n.rasptstamp,"%Y-%m-%d %H:%M:%S").timetuple()))*1000
        raw["y"] = float(n.payload)
        el.append(raw)
    return jsonify(el)

@app.route("/humidity.json")
def humidity_data():
    xs= IoT.query.filter_by(topic="iot/humidity").order_by(IoT.rasptstamp.asc()).all()
    el = []
    for n in xs:
        raw = {}
        raw["x"] = int(time.mktime(datetime.datetime.strptime(n.rasptstamp,"%Y-%m-%d %H:%M:%S").timetuple()))*1000
        raw["y"] = float(n.payload)
        el.append(raw)
    return jsonify(el)

@app.route("/pressure.json")
def pressure_data():
    xs= IoT.query.filter_by(topic="iot/pressure").order_by(IoT.rasptstamp.asc()).all()
    el = []
    for n in xs:
        raw = {}
        raw["x"] = int(time.mktime(datetime.datetime.strptime(n.rasptstamp,"%Y-%m-%d %H:%M:%S").timetuple()))*1000
        raw["y"] = float(n.payload)
        el.append(raw)
    return jsonify(el)





if __name__ == '__main__':
    app.run(host="0.0.0.0")
