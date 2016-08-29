import os
import pandas as pd

from flask import Flask
from flask import render_template
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/test")
def test():
    return "HUHUHU"
    

@app.route("/data")
def data():
    # Use cleaned data from jupyter notebook
    a = os.getcwd()
    path = a + '\\data\\dashboard_data.json'
    df = pd.read_json(path)
    return df.to_json(date_unit='ns', orient='records')

    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)