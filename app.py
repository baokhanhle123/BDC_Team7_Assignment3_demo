from flask import Flask, render_template, Response, send_file
import base64
import pandas as pd
from io import BytesIO
from visualization import req_per_date, req_per_type, size_delay_relationship, percentage_province, percentage_isp

app = Flask(__name__)
df = pd.read_csv('data.csv')



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/visualization")
def visualization():
    return render_template('visualization.html')

    
@app.route("/database")
def database():
    return render_template('database.html')

@app.route("/model")
def model():
    return render_template('model.html')

@app.route('/map')
def map():
    return render_template('map.html')

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