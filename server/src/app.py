import flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin

from tweet import rate_tweet
import sys
from access_firebase import check_key, set_key
from generate_string import generate_string


app = flask.Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

print(sys.platform)
if sys.platform == "win32":
    app.config["DEBUG"] = True


@app.route("/", methods=["GET"])
@cross_origin()
def home():

    return "<h1>Rate API</h1><p>This site is a prototype API for rating twiter apis</p>"


# A route to return all of the available entries in our catalog.
@app.route("/api/v1/rate", methods=["GET"])
@cross_origin()
def rate():
    # check uid first
    if "uid" in request.args:
        uid = request.args["uid"]
    else:
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Error: No uid was passed in. Please specify an uid.",
                }
            ),
            400,
        )

    if "key" in request.args:
        key = request.args["key"]
    else:
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Error: No key was passed in. Please specify an uid.",
                }
            ),
            200,
        )

    # approve uid
    if not (check_key(key, uid)):
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Error: The users single use key doesnt match the key doesnt passed in.",
                }
            ),
            200,
        )

    if "tweet_status" in request.args:
        try:
            tweet_status = int(request.args["tweet_status"])
        except ValueError:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Error: Tweet status isnt an integer.",
                    }
                ),
                200,
            )
    else:
        return (
            jsonify(
                {"success": False, "message": "Error: Tweet status wasn't provided",}
            ),
            200,
        )

    pure_score = rate_tweet(tweet_status)

    set_key(generate_string(15), uid)
    return jsonify(
        {
            "tweet_status": tweet_status,
            "word_positivity_rating": pure_score,
            "success": True,
        }
    )


if app.config["DEBUG"]:
    app.run(host="0.0.0.0")
