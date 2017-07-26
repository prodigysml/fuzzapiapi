from flask import Flask
from flask import request
from db import run_db_query
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config["DBPATH"] = "/root/Documents/HackingTools/fuzzapi/db/development.sqlite3"
app.config["FUZZAPI_IP"] = "192.168.33.128"
app.config["FUZZAPI_PORT"] = "3000"


@app.route("/scans/all", methods=["GET"])
def get_all_scans():
    return run_db_query(app.config["DBPATH"], "SELECT * FROM SCANS")


@app.route("/scans/search", methods=["GET"])
def search_all_scans():
    # flag to add where clause to query
    where_clause_present = False

    # base query
    query = "SELECT * FROM SCANS"

    args = ["id", "url", "sid", "parameters", "method", "cookies", "created_at", "updated_at", "json", "user_id", "status"]

    params = dict()

    for arg in args:
        get_variable = request.args.get(arg)

        if get_variable is not None:
            if not where_clause_present:
                query += " WHERE"
                where_clause_present = True

            query += " " + arg + " LIKE :" + arg

            params[arg] = get_variable

    return run_db_query(app.config["DBPATH"], query, params)


def extract_authenticity_token():
    r = requests.get("http://" + app.config["FUZZAPI_IP"] + ":" + app.config["FUZZAPI_PORT"] + "/users/sign_in")

    soup = BeautifulSoup(r.text, "html.parser")

    return soup.find("input", {"name": "authenticity_token"})["value"]


@app.route("/scan/start", methods=["GET"])
def start_scan():
    auth_token = extract_authenticity_token()

    return


if __name__ == "__main__":
    app.run("0.0.0.0", port="80")
