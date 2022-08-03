from flask import Flask, render_template

app = Flask(__name__)


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


if  __name__ == '__main__':
    app.run(debug=True)