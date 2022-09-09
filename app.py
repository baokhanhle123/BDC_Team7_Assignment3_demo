from flask import Flask, render_template, Response, send_file
import base64
from enum import auto

from ipaddress import ip_address
from flask import Flask, render_template, request
import utils
import pandas as pd
import os
import pickle
import numpy as np
from io import BytesIO
from visualization import (
    req_per_date,
    req_per_type,
    size_delay_relationship,
    percentage_province,
    percentage_isp,
)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
df = pd.read_csv("data.csv")
columns = utils.get_column_names()


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "data/data.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app.config.from_object(Config)
db = SQLAlchemy(app)

columns = [
    "id",
    "delay",
    "content_name",
    "ip_address",
    "file_size",
    "latitude",
    "longitude",
    "ISP",
    "region",
    "req_date",
    "req_time",
    "hit_status",
    "country",
    "file_type",
]


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delay = db.Column(db.Float, index=True)
    hit_status = db.Column(db.String(120), index=True)
    ip_address = db.Column(db.String(64), index=True)
    content_name = db.Column(db.String(256))
    file_size = db.Column(db.Integer)
    latitude = db.Column(db.Float, index=True)
    longitude = db.Column(db.Float, index=True)
    ISP = db.Column(db.String(120), index=True)
    region = db.Column(db.String(120), index=True)
    file_type = db.Column(db.String(120), index=True)
    country = db.Column(db.String(120), index=True)
    req_date = db.Column(db.String(120), index=True)
    req_time = db.Column(db.Time, index=True)

    def __repr__(self):
        return f"User: {self.name}"

    def to_dict(self):
        return {
            "id": self.id,
            "delay": self.delay,
            "content_name": self.content_name,
            "ip_address": self.ip_address,
            "file_size": self.file_size,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "ISP": self.ISP,
            "region": self.region,
            "req_date": self.req_date,
            "req_time": self.req_time.isoformat(),
            "hit_status": self.hit_status,
            "country": self.country,
            "file_type": self.file_type,
        }


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/visualization")
def visualization():
    return render_template("visualization.html")


@app.route("/database")
def database():
    return render_template("database.html")


@app.route("/server-side-table-data")
def server_side_table_data():
    """
    Add search, sort and pagination functionalities
    in the server
    """
    query = Users.query

    # Search filter
    search = request.args.get("search")
    if search:
        query = query.filter(
            db.or_(
                Users.id.like(f"%{search}%"),
                Users.delay.like(f"{search}%"),
                Users.content_name.like(f"{search}%"),
                Users.ISP.like(f"{search}%"),
                Users.ip_address.like(f"{search}%"),
                Users.file_size.like(f"{search}%"),
                Users.latitude.like(f"{search}%"),
                Users.longitude.like(f"{search}%"),
                Users.region.like(f"{search}%"),
                Users.req_date.like(f"{search}%"),
                Users.req_time.like(f"{search}%"),
                Users.country.like(f"{search}%"),
                Users.file_type.like(f"{search}%"),
            )
        )
    total = query.count()

    # Sorting
    sort = request.args.get("sort")
    if sort:
        order = []
        for s in sort.split(","):
            direction = s[0]
            name = s[1:]
            if name not in columns:  # default state
                name = "id"
            col = getattr(Users, name)
            if direction == "-":
                col = col.desc()
            order.append(col)
        if order:
            query = query.order_by(*order)

    # Pagination
    start = request.args.get("start", type=int, default=-1)
    length = request.args.get("length", type=int, default=-1)
    if start != -1 and length != -1:
        query = query.offset(start).limit(length)

    # Response
    return {"data": [user.to_dict() for user in query], "total": total}


@app.route("/model")
def model():
    # Params
    delay_model = request.args.get("delay-model")
    delay_hour = request.args.get("delay-hour")
    delay_size = request.args.get("delay-size")

    req_model = request.args.get("req-model")
    req_hour = request.args.get("req-hour")
    req_date = request.args.get("req-date")

    # Predictions
    delay, req = None, None

    if delay_model:
        delay = get_predict_delay(delay_model, delay_hour, delay_size)
        delay = [delay, delay_hour, delay_size]
    if req_model:
        req = get_predict_req(req_model, req_hour, req_date)

    return render_template("model.html", delay=delay, popularity=req)


def get_predict_delay(model, req_time, file_size):
    mu = np.array([9.96573284e04, 1.36867375e01])
    sigma = np.array([2.88700422e05, 5.69302505e00])
    price = None
    normalize_test_data = (np.array([int(file_size), int(req_time)]) - mu) / sigma
    normalize_test_data = np.hstack((np.ones(1), normalize_test_data))
    if model == "theta-1":
        file = open("models/theta_1.pkl", "rb")
        theta_1 = pickle.load(file)
        price = normalize_test_data.dot(theta_1)
    elif model == "theta-2":
        file = open("models/theta_2.pkl", "rb")
        theta_2 = pickle.load(file)
        price = normalize_test_data.dot(theta_2)
    elif model == "theta-3":
        file = open("models/theta_3.pkl", "rb")
        theta_3 = pickle.load(file)
        price = normalize_test_data.dot(theta_3)
    elif model == "theta-4":
        file = open("models/theta_4.pkl", "rb")
        theta_4 = pickle.load(file)
        price = normalize_test_data.dot(theta_4)
    elif model == "theta-5":
        file = open("models/theta_5.pkl", "rb")
        theta_5 = pickle.load(file)
        price = normalize_test_data.dot(theta_5)
    return round(price, 4)


def get_predict_req(model, hour, date):
    import tensorflow as tf

    def model_forecast(model, series, window_size):
        ds = tf.data.Dataset.from_tensor_slices(series)
        ds = ds.window(window_size, shift=1, drop_remainder=True)
        ds = ds.flat_map(lambda w: w.batch(window_size))
        ds = ds.batch(32).prefetch(1)
        forecast = model.predict(ds)
        return forecast

    window_size = 30
    if model == "rnn":
        file = open("models/rnn.pkl", "rb")
        rnn = pickle.load(file)

    elif model == "cnn":
        file = open("models/cnn.pkl", "rb")
        cnn = pickle.load(file)

    elif model == "lstm":
        file = open("models/lstm.pkl", "rb")
        lstm = pickle.load(file)

    elif model == "arima":
        file = open("models/arima.pkl", "rb")
        arima = pickle.load(file)
    return


@app.route("/map")
def map():
    return render_template("map.html")


@app.route("/req_per_date")
def vsl_bar1():
    fig = req_per_date(df)
    buf = BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


@app.route("/req_per_type")
def vsl_bar2():
    fig = req_per_type(df)
    buf = BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


@app.route("/size_delay_relationship")
def vsl_scatter():
    fig = size_delay_relationship(df)
    buf = BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


@app.route("/percentage_province")
def vsl_pie1():
    fig = percentage_province(df)
    buf = BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


@app.route("/percentage_isp")
def vsl_pie2():
    fig = percentage_isp(df)
    buf = BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True)
