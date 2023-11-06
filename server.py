from flask import Flask
from flask import request, jsonify
from helpers import import_data_into_db
from apispec import APISpec
import pprint as pp

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
def hello_world():
    return "<p>Private API page! Do not enter!</p>"


@app.route('/userInfo', methods=['GET'])
def getUserInfo():
    return f"<p>API for retrieving user information</p><br><p>OpenAPI Specifications:</p><p>{spec_sheet_html}</p>"


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
