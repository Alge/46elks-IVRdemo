from flask import Flask, request
import json
import urllib

app = Flask(__name__)

numbers = ["+46766861794", "+46766861814", "+46766860003"]

base_url = "https://b2a18090.ngrok.io/"

# Url for static files. change this to the root dir where you store yours
static_url = "http://files.46elks.com/alge/ivr-demo/"


@app.route("/init", methods=["POST", "GET"])
def home():

    next_url = base_url+"next" + "?tried=" + urllib.parse.quote_plus(numbers[0])
    print(next_url)
    j = {
    "play": static_url + "welcome.wav",
        "next": {
            "connect": numbers[0],
            "next": {
                "hangup": "busy"
            },
            "failed": next_url,
            "busy": next_url
        }
    }

    return json.dumps(j)

@app.route("/next", methods=["POST", "GET"])
def next():
    tried =  request.args.get("tried").split(";")
    print(tried)

    next_number = None

    for number in numbers:
        if number not in tried:
            next_number = number
            break


    if not next_number:
        j = {
            "play": static_url + "no_more.wav",
        }

    else:
        tried.append(next_number)
        next_url = base_url+"next" + "?tried=" + urllib.parse.quote_plus(";".join(tried))
        j = {
        "play": static_url + "try_next.wav",
            "next": {
                "connect": next_number,
                "next":{
                    "play": static_url + "thank_you.wav"
                },
                "failed": next_url,
                "busy": next_url
            }
        }

    return json.dumps(j)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
