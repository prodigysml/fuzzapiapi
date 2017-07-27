# coding=utf-8
from flask import Flask
from flask import request
from db import run_db_query
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config["DBPATH"] = "/root/Documents/HackingTools/fuzzapi/db/development.sqlite3"
app.config["FUZZAPI_IP"] = "192.168.33.128"
app.config["FUZZAPI_PORT"] = "3000"


@app.route("/scan/all", methods=["GET"])
def get_all_scans():
    return run_db_query(app.config["DBPATH"], "SELECT * FROM SCANS")


@app.route("/scan/search", methods=["GET"])
def search_all_scans():
    # flag to add where clause to query
    where_clause_present = False

    # base query
    query = "SELECT * FROM SCANS"

    # list of all the columns
    args = ["id", "url", "sid", "parameters", "method", "cookies", "created_at", "updated_at", "json", "user_id", "status"]

    # current params being used
    params = dict()

    # loops through all args and checks if user has entered anything. If so, then appends to query
    for arg in args:
        get_variable = request.args.get(arg)

        # checks if arg is set
        if get_variable is not None:
            if not where_clause_present:
                query += " WHERE"
                where_clause_present = True

            # check to see if logical operator is required
            if len(params) >= 2:
                query += " AND "

            query += " " + arg + " LIKE :" + arg

            params[arg] = get_variable

    return run_db_query(app.config["DBPATH"], query, params)


def extract_authenticity_token(base_url, user, password):

    session = requests.Session()

    r = session.get(base_url + "/users/sign_in")

    soup = BeautifulSoup(r.text, "lxml")

    auth_token = soup.find("meta", {"name": "csrf-token"})["content"]

    params = {
        "authenticity_token": auth_token,
        "user[email]": user,
        "user[password]": password,
        "user[remember_me]": "0",
        "commit": "Sign in"
    }

    r = session.post(base_url + "/users/sign_in", data=params)

    soup = BeautifulSoup(r.text, "lxml")

    return session, soup.find("meta", {"name": "csrf-token"})["content"]


@app.route("/scan/start", methods=["POST"])
def start_scan():
    user = request.form.get("user")

    password = request.form.get("pass")

    headers = request.form.get("headers")

    url = request.form.get("url")

    if headers is None:
        headers = ""

    parameters = request.form.get("params")

    if parameters is None:
        parameters = ""

    base_url = "http://" + app.config["FUZZAPI_IP"] + ":" + app.config["FUZZAPI_PORT"]

    session, auth_token = extract_authenticity_token(base_url, user, password)

    params = {"authenticity_token": auth_token,
              "url": url,
              "method[]": "GET",
              "headers": headers,
              "parameters": parameters}

    r = session.post(base_url + "/scans", data=params)

    soup = BeautifulSoup(r.text, "lxml")

    return "Started the scan! The scan ID is: " + soup.find("div", {"id": "vulnerability-container"})["data-scan"]


@app.route("/scan/results", methods=["GET"])
def scan_results():
    # Search for scans with scan_id (only scan_id initially for the PoC)
    query = "SELECT * FROM VULNERABILITIES"

    scan_id = request.args.get("id")

    if scan_id is not None:
        query += " WHERE scan_id = :id"
        return run_db_query(app.config["DBPATH"], query, {"id": scan_id})

    return run_db_query(app.config["DBPATH"], query)


if __name__ == "__main__":
    app.run("0.0.0.0", port="80")
