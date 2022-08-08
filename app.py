from enum import auto
from flask import Flask, render_template
import utils

app = Flask(__name__)
columns = utils.get_column_names()


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/visualization")
def visualization():
    return render_template("visualization.html")


@app.route("/database")
def database():
    rows = utils.get_all("SELECT * FROM users LIMIT 1500")
    data = []
    for r in rows:
        rec = {columns[i]: r[i] for i in range(0, len(r))}
        data.append(rec)
    return render_template("database.html", users=data, colnames=columns)

@app.route("/model")
def model():
    return render_template("model.html")

@app.route('/map')
def map():
    return render_template('map.html')


if __name__ == "__main__":
    app.run(debug=True)
