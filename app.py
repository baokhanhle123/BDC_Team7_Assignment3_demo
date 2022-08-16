from flask import Flask, render_template, Response, send_file
import base64
from enum import auto

from ipaddress import ip_address
from flask import Flask, render_template, request
import utils
import pandas as pd
import os
from io import BytesIO
from visualization import req_per_date, req_per_type, size_delay_relationship, percentage_province, percentage_isp
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
df = pd.read_csv('data.csv')
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
    return render_template("model.html")


@app.route("/map")
def map():
    return render_template("map.html")

@app.route('/req_per_date')
def vsl_bar1():
    fig = req_per_date(df)
    buf = BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/req_per_type')
def vsl_bar2():
    fig = req_per_type(df)
    buf = BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/size_delay_relationship')
def vsl_scatter():
    fig = size_delay_relationship(df)
    buf = BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/percentage_province')
def vsl_pie1():
    fig = percentage_province(df)
    buf = BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/percentage_isp')
def vsl_pie2():
    fig = percentage_isp(df)
    buf = BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

if  __name__ == '__main__':
    app.run(debug=True)
