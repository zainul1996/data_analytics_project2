# app.py
from flask import jsonify
from typing import Collection
from flask import Flask, request, jsonify, render_template
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient

client = FaunaClient(secret="fnAEJf-GGOACAX3o-v9-biQ7ulrXHokD4mz_Otjz")

app = Flask(__name__)


@app.route("/getUser", methods=["POST"])
def getUser():
    try:
        d = request.json["username"]
        if d:
            userDetails = client.query(
                q.get(q.match(q.index("users_by_username"), d)))
            if userDetails:
                return userDetails["data"]
            else:
                "user doesn't exist"
        else:
            return "no username provided"
    except:
        return "user doesn't exist"


@app.route("/login", methods=["POST"])
def login():
    try:
        d = request.json
        if d["username"] and d["password"]:
            userDetails = client.query(
                q.get(q.match(q.index("users_by_username"), d["username"])))
            if userDetails:
                if userDetails["data"]["username"] == d["username"] and userDetails["data"]["password"] == d["password"]:
                    return jsonify(True)
        return jsonify(False)
    except:
        return jsonify(False)


@app.route("/createUser", methods=["POST"])
def createUser():
    try:
        d = request.json
        if d["firstname"] and d["lastname"] and d["username"] and d["password"] and d["email"]:
            result = client.query(
                q.create(q.collection("users"), {"data": d}))
            if result:
                return jsonify(True)
        return "value missing/incorrect"
    except:
        return "username already exists"


@app.route("/getUserPrefs", methods=["POST"])
def getUserPrefs():
    d = request.json["userid"]
    response = client.query(
        q.map_(q.lambda_("doc", q.select("data", q.get(q.var("doc")))),
               q.paginate(q.match(q.index("prefs_by_userprefs"), str(d)))))
    return jsonify(response["data"])


@app.route("/insertUserPrefs", methods=["POST"])
def insertUserPrefs():
    try:
        d = request.json
        if d["userRefID"] and d["preferences"]["Male"] and d["preferences"]["bald"] and d["preferences"]["big_lips"] and d["preferences"]["big_nose"] and d["preferences"]["black_hair"] and d["preferences"]["eyeglasses"] and d["preferences"]["pale_skin"] and d["preferences"]["straight_hair"] and d["preferences"]["wavy_hair"] and d["preferences"]["young"]:
            result = client.query(
                q.create(q.collection("prefs"), {"data": d}))
            if result:
                return jsonify(True)
        return "values missing/incorrect"
    except:
        return "something went wrong"


@app.route("/get", methods=["GET"])
def get_something():
    # Retrieve the "name" from url parameter
    # If empty, sets "name" as None
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"

    # Return the response in json format
    return jsonify(response)


@app.route("/post/", methods=["POST"])
def post_something():
    param = request.form.get("name")
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify(
            {
                "Message": f"Welcome {name} to our awesome platform!!",
                # Add this option to distinct the POST request
                "METHOD": "POST",
            }
        )
    else:
        return jsonify({"ERROR": "no name found, please send a name."})


# A welcome message to test our server
@app.route("/")
def index():
    return "<h1>Welcome to our server !!</h1>"


# Renders a html file from the templates folder
@app.route("/helloworld")
def helloworld():
    return render_template("index.html")


if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(debug=True, threaded=True, port=5000)
