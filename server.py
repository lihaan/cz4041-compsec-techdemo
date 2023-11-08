from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from helpers import import_data_into_db
from apispec import APISpec
import pprint as pp

USER_DATA = {
    "username": "smith",
    "password": "password123"
}

IS_AUTH = False

app = Flask(__name__)
spec = APISpec(
    title="Demo HTTP API server",
    version="0.0.1",
    openapi_version="3.0.2",
    info=dict(description="A minimal API to illustrate how easy it is to crawl and steal data from an unsecured API"),
)

spec.components.schema(
    "getUserInfoByUserid",
    {
        "properties": {
            "userid": {"type": "integer"},
        }
    },
)
spec.path(
    path="/userInfo",
    operations=dict(
        post=dict(
            responses={"200": {"content": {"application/json": {"schema": "getUserInfoByUserid"}}}}
        )
    ),
)
spec_sheet = spec.to_dict()
spec_sheet_html = pp.pformat(spec_sheet).replace("\n", "<br>")


GLOBALS = {
    "users_table": None
}

@app.route("/")



@app.route("/", methods=["GET", "POST"])
def index():
    global IS_AUTH
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == USER_DATA["username"] and password == USER_DATA["password"]:
            IS_AUTH = True
            return redirect("/user_info")
        else:
            return "Invalid username or password. Please try again."
    return render_template('index.html', USER_DATA=USER_DATA)

@app.route("/user_info", methods=["GET"])
def user_info():
    if IS_AUTH:
        with open('user_data.csv', 'r') as file:
            data = file.read()
        return render_template('display_data.html', data=data)
    else:
        return "NOT LOGGED IN"

# @app.route('/userInfo', methods=['GET'])
# def getUserInfo():
#     return f"<p>API for retrieving user information</p><br><p>OpenAPI Specifications:</p><p>{spec_sheet_html}</p>"


@app.route('/userInfo', methods=['POST'])
def getUserInfoByUserid():
    request_data = request.get_json()
    result = handleGetUserInfo(request_data)
    return jsonify(result)


def handleGetUserInfo(request_data):
    userid_query = request_data["userid"]
    print(f"queried for {userid_query}")

    query_result = GLOBALS["users_table"].query(userid_query)
    return query_result


if __name__ == '__main__':
    GLOBALS["users_table"] = import_data_into_db("user_data.csv")
    app.run(host="0.0.0.0", port=5000)
