from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    # todo: Add in argument parsing for localhost / or all interfaces
    # todo: Ask about specific ports
    app.run("0.0.0.0", port="80")