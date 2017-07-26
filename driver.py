from flask import Flask
from flask import Response
import sqlite3
import json

app = Flask(__name__)
app.config["DBPATH"] = "/root/Documents/HackingTools/fuzzapi/db/development.sqlite3"


@app.route("/scans/all", methods=["GET"])
def get_all_scans():
    conn = sqlite3.connect(app.config["DBPATH"])

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM SCANS")

    response = Response(json.dumps(cursor.fetchall()))

    response.headers['Content-type'] = "application/json"

    return response


if __name__ == "__main__":
    app.run("0.0.0.0", port="80")
