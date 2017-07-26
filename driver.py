from flask import Flask
from flask import request
from db import run_db_query

app = Flask(__name__)
app.config["DBPATH"] = "/root/Documents/HackingTools/fuzzapi/db/development.sqlite3"


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


if __name__ == "__main__":
    app.run("0.0.0.0", port="80")
