from flask import Flask
from db import run_db_query

app = Flask(__name__)
app.config["DBPATH"] = "/root/Documents/HackingTools/fuzzapi/db/development.sqlite3"


@app.route("/scans/all", methods=["GET"])
def get_all_scans():
    return run_db_query(app.config["DBPATH"], "SELECT * FROM SCANS")


if __name__ == "__main__":
    app.run("0.0.0.0", port="80")
